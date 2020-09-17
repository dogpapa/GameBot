from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.paginator import Paginator
from .forms import UploadFileForm
# from .models import Features
from .models import BotData, HistoryData, UploadFileModel
# from .models import HLUserInfo
# from .models import History
# from .models import Document
from django.views.decorators.csrf import csrf_exempt
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from lightgbm import LGBMClassifier
import joblib
from sklearn.metrics import classification_report

global human_list,cond_bot,cond_bot_count
human_list = []

# Create your views here.
UPLOAD_DIR = "../upload_file/"
def main(request):
    return render(request, 'main.html')
def H_L_user_list(request):
    # s = []
    # for f in HLUserInfo.objects.filter(file_name='파일이름'):
    #     s+= str(id) + ':' + f.file_name
    data = 히스토리모델.objects.filter(file_name="파일이름")
    return render(request, 'H_L_user_list.html',{'data':data})

def bot_user_detect(request):
    return render(request, 'bot_user_detect.html') 


# ajax 할때 csrf 토큰을 같이 넘겨줘야 하는거같은데 안돼서 그냥 csrf를 안써버리기  
@csrf_exempt
def upload_file(request):
    if request.method =='POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            result = UploadFileModel.objects.last()
            file_name = str(result.upload_file)
            # 저장된 파일 읽어 오기 
            df = pd.read_csv("./media/" + file_name, index_col='Actor')
            # 학습모델에 맞게 정규화 하기
            scaler = joblib.load('./static/pkl/gamebot_scaler.pkl')
            df_scaled = pd.DataFrame(scaler.transform(df), columns = df.columns)
            df_scaled.set_index(df.index, inplace = True)
            # 모델 -> LGBM 알고리즘(GridsearchCV 하이퍼파라미터 적용)
            model = joblib.load('./static/pkl/gamebot_model.pkl')
            pred = model.predict(df_scaled)
            # 예측
            pred = pd.DataFrame({'Prediction':pred})
            # 결과
            save01 = df[['same_point_connection_rate','Login_day_count','playtime_per_day','avg_money','Item_get_ratio','Exp_get_ratio']].reset_index()
            save02 = pd.concat([save01, pred], axis = 1)
            def change_output(data):
                if data == 0:
                    return 'Human'
                else:
                    return 'Bot'
            save02['Prediction'] = save02['Prediction'].apply(change_output)
            save02.rename(columns = {'same_point_connection_rate':'Same ip Login ratio',
                        'Login_day_count':'Login Day count(max=88)',
                        'playtime_per_day':'Play Time per Day',
                        'avg_money':'Average Money',
                        'Item_get_ratio':'Item Get ratio',
                        'Exp_get_ratio':'Exp. Get ratio',
                        'Prediction':'Type'}, inplace = True)
            # Index는 Unique
            save02.set_index(save02.Actor, inplace = True)
            # 화면(봇 유저만 출력)
            cond = (save02['Type'] == 'Bot')
            
           
            output = save02.loc[cond]


            ##################################################

            df = save02[save02.columns.difference(['Type'])]
            tg = save02[['Type']].reset_index()

            # 정규화 스케일링 작업
            scaler = MinMaxScaler()
            scaler.fit(df)
            df_scaled = pd.DataFrame(scaler.transform(df), columns = df.columns)

            # 데이터프레임 작업
            dftg = pd.concat([df_scaled, tg], axis = 1)
            dftg = dftg.set_index(dftg.iloc[:,0],drop=True)
            # dftg.set_index('Actor')

            # feature importance값 df형태로 나오는 코드
            # FI_df = pd.DataFrame(model.feature_importances_, index = df_scaled.columns, columns = ['Importance']).sort_values(by = 'Importance', ascending = False)
              
            
            # 휴먼 유저
            cond_human = (dftg['Type'] == 'Human')
            human = dftg.loc[cond_human]

            # 봇유저 갯수
            global cond_bot,cond_bot_count
            cond_bot = dftg[dftg['Type'] == 'Bot']
            # cond_bot = (dftg['Type'] == 'Bot')
            # cond_bot = dftg.loc[cond_bot] 
            cond_bot_count = cond_bot['Type'].count()
            
        
            

            # 휴먼 유저 육각형 특성값(중앙값 기준)
            human_money = human['Average Money'].median()
            human_exp = human['Exp. Get ratio'].median()
            human_item = human['Item Get ratio'].median()
            human_login = human['Login Day count(max=88)'].median()
            human_playtime = human['Play Time per Day'].median()
            human_ip = human['Same ip Login ratio'].median()
            
            # 글로벌 변수로 다른 함수에서 사용할 수 있게 함
            global human_list
            human_list.append(human_money)
            human_list.append(human_exp)
            human_list.append(human_item)
            human_list.append(human_login)
            human_list.append(human_playtime)
            human_list.append(human_ip)

         
            
            
################################################################################
            # History DB 저장
            # fb = HistoryData.objects.all()
            # fb.delete()
            # fb = HistoryData.objects.get(all_user_count=123)
            # fb.delete()
            
            file_name_route = './media/'+file_name
            hd = HistoryData(
                file_name = file_name_route,
                all_user_count = dftg['Type'].count(),
                bot_user_count = cond_bot_count
            )
            hd.save()
            

            # 업로드받은 csv 의 Human 평균을 계산

            # 나온 결과값(bot_list)을 DB에 저장하고
            bulk_bot = []
            for i in range(len(output)):
                fb = BotData(bot_id = output.iloc[i,0],
                    file_name = file_name_route,
                    same_point_connection_rate = output.iloc[i,1], 
                    Login_day_count = output.iloc[i,2],
                    playtime_per_day = output.iloc[i,3],
                    avg_money = output.iloc[i,4],
                    Item_get_ratio = output.iloc[i,5],
                    Exp_get_ratio = output.iloc[i,6])
                bulk_bot.append(fb)
            BotData.objects.bulk_create(bulk_bot)
            # 업로드된 csv 파일에서 Heavy / Light 유저 별로 구하는 알고리즘 적용 

            # 결과값 리스트로 뿌려주기 위해 페이지네이션
            bot_data_list = BotData.objects.filter(file_name=file_name_route)
            paginator = Paginator(bot_data_list,5)
            page = request.GET.get('page')
            posts = paginator.get_page(page)
            
            print("여기까지 오면 ajax_detect_result.html로 이동됨")
            return render(request, 'ajax_detect_result.html', {'header': output.columns.tolist(),"posts": posts})
    else:
        form = UploadFileForm()
    return HttpResponse("실패")


@csrf_exempt
def gamebotdetail(request):
    global cond_bot,cond_bot_count
    user_id = request.GET['bot_id']
    bot_percentage = '95%' #해야함
    features = ['Average Money','Exp. Get ratio','Item Get ratio','Login Day count(max=88)','Play Time per Day','Same ip Login ratio']
    
    human_data = human_list
    # 샘플 데이터 (448753 <- 확인하고자 하는 데이터의 인덱스 입력)
    if cond_bot[cond_bot.iloc[:,7] == int(user_id)]['Type'].count():
        print("if문에서의 user_id")
        cond_bot = cond_bot[cond_bot.iloc[:,7] == int(user_id)]
        bot_money = cond_bot['Average Money'].median()
        bot_exp = cond_bot['Exp. Get ratio'].median()
        bot_item = cond_bot['Item Get ratio'].median()
        bot_login = cond_bot['Login Day count(max=88)'].median()
        bot_playtime = cond_bot['Play Time per Day'].median()
        bot_ip = cond_bot['Same ip Login ratio'].median()   
        print("완료")
    else:
        print("오류")
    bot_data = [bot_money,bot_exp,bot_item,bot_login,bot_playtime,bot_ip]
    return render(request,'game_bot_detail.html',{"user_id":user_id,"bot_percentage":bot_percentage,"features":features,"human_data":human_data,"bot_data":bot_data})

def gamebothistory(request):
    page = request.GET.get('page',1)
    history_list = HistoryData.objects.all()
    paginator = Paginator(history_list,10)
    total_page=len(history_list)
    history = paginator.get_page(page)
    return render(request,'game_bot_history.html',{"history_list":history_list,"history":history})
