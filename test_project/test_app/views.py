from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from .forms import UploadFileForm
# 최재호 수정
from .models import BotData, HistoryData, UploadFileModel,HLUserList, BotDetailData

import os
import pandas as pd
import numpy as np
import joblib
import re

from lightgbm import LGBMClassifier
from sklearn.metrics import classification_report
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn.preprocessing import MinMaxScaler


global human_list
human_list = []

# Create your views here.
UPLOAD_DIR = "../upload_file/"
def main(request):
    return render(request, 'main.html')
def H_L_user_list(request):
    # s = []
    # for f in HLUserInfo.objects.filter(file_name='파일이름'):
    #     s+= str(id) + ':' + f.file_name
    # data = 히스토리모델.objects.filter(file_name="파일이름")

    # Heavy Light 유저 구분 모델 적용

    # DB에서 전에 있던 값 불러옴

    # DB에서 불러온 값과 이번 파일에서 구한 값을 비교 해서 상위 100개만 뽑음

    # DB에 원래 있던 것 다 지우고 이거 저장
    # DB에 원래 있던 것과 비교해서 있는건 놔두고 새거만 추가?
    
    # 이거 나온거 뿌려주기 
    # 결과값 리스트로 뿌려주기 위해 페이지네이션
    bot_data_list = HLUserList.objects.filter(h_or_l=1)
    paginator = Paginator(bot_data_list,15)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    bot_data_list2 = HLUserList.objects.filter(h_or_l=2)
    paginator2 = Paginator(bot_data_list2,15)
    page2 = request.GET.get('page2')
    posts2 = paginator2.get_page(page2)
    header = []
    # for e in HLUserList.objects.all() :
    #     header.append(e.headline)
    return render(request, 'H_L_user_list.html',{"posts": posts, "posts2" : posts2})


def bot_user_detect(request):
    return render(request, 'bot_user_detect.html') 

# ajax 할때 csrf 토큰을 같이 넘겨줘야 하는거같은데 안돼서 그냥 csrf를 안써버리기  
@csrf_exempt
def upload_file(request):
    if request.POST['page_num'] == '0':
        if request.method =='POST':
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                result = UploadFileModel.objects.last()
                file_name = str(result.upload_file)
                # 저장된 파일 읽어 오기 
                df = pd.read_csv("./media/" + file_name, index_col='Actor')
                # Copy dataframe for clustering
                df01 = df.copy()
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

                # 이거 주석안해야 밑의 코드 실행됨
                save02.drop(columns = 'Actor', inplace = True)

                df02 = pd.concat([df01, save02[['Type']]], axis = 1)
                # 화면(봇 유저만 출력)
                cond = (save02['Type'] == 'Bot')
                output = save02.loc[cond]
                # 군집 분석(휴먼)
                cond02 = (df02['Type'] == 'Human')
                output02 = df02.loc[cond02]

                # 게임 봇 검출 확률 코드
                global gamebot_prob
                gamebot_prob = ((len(output) / (len(output) + len(output02)))*100)
                gamebot_prob = round(gamebot_prob)
                
# print("게임 봇 검출 확률:",gamebot_prob,"%")
    ####################################################################################################
    # 2020 09 18    10시 50분 양로가 바꾼 내용 
    # # 변수 중요도 데이터프레임 생성(1*6 데이터 프레임 사이즈 맞추기)
                FI_df = pd.DataFrame(model.feature_importances_, index = df_scaled.columns, columns = ['Importance']).sort_values(by = 'Importance', ascending = False).reset_index()
                FI = FI_df.loc[[0,1,2,5,6,10],:].reset_index(drop = True)
                FI = FI.T.reset_index(drop = True)

                # 변수 중요도 데이터프레임 -> df
                df = FI.iloc[1:].reset_index(drop = True)
                df.columns = ['Average Money', 'Same ip Login ratio', 'Item Get ratio', 'Exp. Get ratio', 'Play Time per Day', 'Login Day count(max=88)']

                # 특성별 가중치 그래프 값 글로벌 변수 저장
                global bar_features, bar_data
                bar_features = []
                bar_data = []
                for i in range(len(df.columns)):
                    bar_features.append(df.columns[i])
                    bar_data.append(df.iloc[0,i]) 

    ####################################################################################################
                # 정규화 작업
                df = save02[save02.columns.difference(['Type'])]
                tg = save02[['Type']].reset_index()

                # 정규화 스케일링 작업(MinMaxScaler)
                scaler = MinMaxScaler()
                scaler.fit(df)
                df_scaled = pd.DataFrame(scaler.transform(df), columns = df.columns)

                # 데이터프레임 작업(병합)
                dftg = pd.concat([df_scaled, tg], axis = 1)
                # dftg = dftg.set_index(dftg.iloc[:,0],drop=True)
                dftg = dftg.set_index('Actor')
                # feature importance값 df형태로 나오는 코드
                # FI_df = pd.DataFrame(model.feature_importances_, index = df_scaled.columns, columns = ['Importance']).sort_values(by = 'Importance', ascending = False)
                
                
                # 휴먼 유저 추출
                cond_human = (dftg['Type'] == 'Human')
                human = dftg.loc[cond_human]

                # radar에 들어갈 정규화한 봇 데이터
                cond_bot = (dftg['Type'] == 'Bot')
                # cond_bot = dftg[dftg['Type'] == 'Bot']
                bot = dftg.loc[cond_bot]
                cond_bot_count = bot['Type'].count()

                # 데이터 비우고 시작
                dt = BotDetailData.objects.all()
                if range(len(dt)) != 0:
                    dt.delete()
                
                # radar에 들어갈 정규화한 봇 데이터 저장 
                bulk_bot_detail = []
                for i in range(len(bot)):
                    dt = BotDetailData(
                        bot_id = bot.index[i],
                        avg_money = bot.iloc[i,0],
                        Exp_get_ratio = bot.iloc[i,1], 
                        Item_get_ratio = bot.iloc[i,2],
                        Login_day_count = bot.iloc[i,3],
                        playtime_per_day = bot.iloc[i,4],
                        same_point_connection_rate = bot.iloc[i,5])
                    bulk_bot_detail.append(dt)
                BotDetailData.objects.bulk_create(bulk_bot_detail)
                                    
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
                file_name_route = './media/'+file_name
                hd = HistoryData(
                    file_name = file_name_route,
                    all_user_count = dftg['Type'].count(),
                    bot_user_count = cond_bot_count
                )
                hd.save()
                
                # print(type(output.index), type(output.iloc[1,1]),"한글한글한글")
                # actor = pd.to_numeric(output.index)  
                # 업로드받은 csv 의 Human 평균을 계산
                # 나온 결과값(bot_list)을 DB에 저장하고
            
                bulk_bot = []
                for i in range(len(output)):
                    fb = BotData(
                        bot_id = output.index[i],
                        file_name = file_name_route,
                        same_point_connection_rate = round(output.iloc[i,0],1), 
                        Login_day_count = round(output.iloc[i,1],1),
                        playtime_per_day = round(output.iloc[i,2],1),
                        avg_money = round(output.iloc[i,3],1),
                        Item_get_ratio = round(output.iloc[i,4],1),
                        Exp_get_ratio = round(output.iloc[i,5],1))
                    bulk_bot.append(fb)
                BotData.objects.bulk_create(bulk_bot)
                
                
    ################################################################################

                # 업로드된 csv 파일에서 Heavy / Light 유저 별로 구하는 알고리즘 적용 
                # 클러스터링 및 Heavy/Light 유저 구분하기 위한 주요 변수들 추출
                cluster01 = output02[['playtime_per_day','access_rate',
                                    'abyss_get_count_per_day','Killed_bynpc_count_per_day','Killed_bypc_count_per_day','Teleport_count_per_day','money_get_count_per_day','Max_level',
                                    'Type']]
                # 이변수 추출
                cluster02  = cluster01[['playtime_per_day','access_rate']]
                # 추출된 이변수에 대한 스케일링 진행
                scaler = MinMaxScaler()
                scaler.fit(cluster02)
                cluster02_scaled = pd.DataFrame(scaler.transform(cluster02), columns = cluster02.columns)
                # 샘플 데이터 생성
                # case01 = cluster01.copy()
                case02 = cluster01.copy()
                model02 = KMeans(n_clusters = 5, max_iter = 500, random_state = 1)
                num_of_cluster_5 = model02.fit_predict(cluster02_scaled)
                case02['cluster'] = num_of_cluster_5
                case02['cluster'].value_counts(normalize = True).round(2)

                # heavy_user, light_user 조건 설정 -> heavy_user는 군집4, light_user는 군집3
                cond_heavy = (case02['cluster'] == 4)
                cond_light = (case02['cluster'] == 3)

                # heavy_user, light_user 데이터프레임 형태로 설정
                heavy_user = case02.loc[cond_heavy].round(2)
                heavy_user.drop(columns = ['Type','cluster'], inplace = True)

                light_user = case02.loc[cond_light].round(2)
                light_user.drop(columns = ['Type','cluster'], inplace = True)
                # score column 추가하고 
                heavy_user["score"] = (heavy_user["playtime_per_day"] + heavy_user["access_rate"] + heavy_user["abyss_get_count_per_day"] +
                                        heavy_user["Killed_bynpc_count_per_day"] +heavy_user["Killed_bypc_count_per_day"] +heavy_user["Teleport_count_per_day"] +
                                        heavy_user["money_get_count_per_day"] +heavy_user["Max_level"] )
                light_user["score"] = (light_user["playtime_per_day"] + light_user["access_rate"] + light_user["abyss_get_count_per_day"] +
                                        light_user["Killed_bynpc_count_per_day"] +light_user["Killed_bypc_count_per_day"] +light_user["Teleport_count_per_day"] +
                                        light_user["money_get_count_per_day"] +light_user["Max_level"] )                                    
                # H_or_L column 추가
                heavy_user['H_or_L'] = 1
                light_user['H_or_L'] = 2
                # heavy light DB 불러오고 
                # H_L_user_DB_select = HLUserList.objects.all()
                # print(H_L_user_DB_select, " \t DB에서 받아온 값 타입은?")
                # # return HttpResponse(H_L_user_DB_select)
                # # DB에 저장된 값이 있는가 확인 
                # print(H_L_user_DB_select == None, H_L_user_DB_select == 'null', H_L_user_DB_select == '', '값은?',HLUserList.DoesNotExist == True)
                # if HLUserList.DoesNotExist :
                #     pass
                # else :
                #     # DB 불러오는 타입 확인하고 DataFrame으로 변경 
                #     DB_heavy_list = pd.DataFrame.from_records(H_L_user_DB_select,
                #         columns=['playtime_per_day','access_rate','abyss_get_count_per_day',
                #         'Killed_bynpc_count_per_day','Killed_bypc_count_per_day','Teleport_count_per_day',
                #         'money_get_count_per_day','Max_level'],
                #         index = H_L_user_DB_select.user_id)

                #     # 데이터프레임 두개 합치고
                #     DB_heavy_list = H_L_user_DB_select.h_or_l == 1
                #     DB_light_list = H_L_user_DB_select.h_or_l == 2
                #     heavy_user = pd.concat([heavy_user, DB_heavy_list], axis=1)
                #     light_user = pd.concat([light_user, DB_light_list], axis=1)
                # return HttpResponse(H_L_user_DB_select)
                delete_all_hluserlist_in_db = HLUserList.objects.all()
                delete_all_hluserlist_in_db.delete()
                
                # 정렬하고 중복 짜르고 
                heavy_user["Actor"] = heavy_user.index
                light_user["Actor"] = light_user.index
                heavy_user.sort_values(by=['score'], axis=0, ascending=False, inplace=True)
                light_user.sort_values(by=['score'], axis=0, ascending=True, inplace=True)
                heavy_user.drop_duplicates('Actor', keep="first", inplace=True)
                light_user.drop_duplicates('Actor', keep="first", inplace=True)
                # DB에 저장된 Heavy Light 유저 값을 받아와서 점수를 비교하여 상위 100명만 다시 저장한다 
                bulk_h_l_user = []
                for i in range(len(heavy_user)):
                    heavy = HLUserList(
                        user_id = heavy_user.iloc[i,10],
                        playtime_per_day = heavy_user.iloc[i,0], 
                        access_rate = heavy_user.iloc[i,1], 
                        abyss_get_count_per_day = heavy_user.iloc[i,2], 
                        Killed_bynpc_count_per_day = heavy_user.iloc[i,3], 
                        Killed_bypc_count_per_day = heavy_user.iloc[i,4], 
                        Teleport_count_per_day = heavy_user.iloc[i,5], 
                        money_get_count_per_day = heavy_user.iloc[i,6], 
                        Max_level = heavy_user.iloc[i,7], 
                        user_score = heavy_user.iloc[i,8],
                        h_or_l = heavy_user.iloc[i,9],
                        )
                    bulk_h_l_user.append(heavy)
                    if i == 99: break
                    
                for i in range(len(light_user)):
                    light = HLUserList(
                        user_id = light_user.iloc[i,10],
                        playtime_per_day = light_user.iloc[i,0], 
                        access_rate = light_user.iloc[i,1], 
                        abyss_get_count_per_day = light_user.iloc[i,2], 
                        Killed_bynpc_count_per_day = light_user.iloc[i,3], 
                        Killed_bypc_count_per_day = light_user.iloc[i,4], 
                        Teleport_count_per_day = light_user.iloc[i,5], 
                        money_get_count_per_day = light_user.iloc[i,6], 
                        Max_level = light_user.iloc[i,7], 
                        user_score = light_user.iloc[i,8],
                        h_or_l = light_user.iloc[i,9],
                        )
                    bulk_h_l_user.append(light)
                    if i == 99: break

                    
                HLUserList.objects.bulk_create(bulk_h_l_user)

    ################################################################################
                # 결과값 리스트로 뿌려주기 위해 페이지네이션
                bot_data_list = BotData.objects.filter(file_name=file_name_route)
                paginator = Paginator(bot_data_list,15)
                page = request.GET.get('page')
                posts = paginator.get_page(page)
                index = "Actor"
                header = output.columns.tolist()
                header.insert(0,index) 
                
                
                return render(request, 'ajax_detect_result.html', {'header': header,"posts": posts,"file_name": file_name_route})
            else:
                form = UploadFileForm()
                return HttpResponse("실패")
    else:
        file_name_route = request.POST['file_name']
        bot_data_list = BotData.objects.filter(file_name=file_name_route)
        paginator = Paginator(bot_data_list,15)
        page = request.POST['page_num']
        posts = paginator.get_page(page)
        header_request = request.POST['header']
        # header = re.match("\'(.*?)\'", header_request)
        # p = re.compile("\'(.*?)\'")
        header = re.findall("\'(.*?)\'", header_request)
    return render(request, 'ajax_detect_result.html', {'header': header,"posts": posts,"file_name": file_name_route})

@csrf_exempt
def pagenation_bot_user_detect_list(request):
    header = request.GET.get('header')
    file_name_route = request.GET.get('file_name')

    bot_data_list = BotData.objects.filter(file_name=file_name_route)
    paginator = Paginator(bot_data_list,5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'ajax_detect_result.html', {'header': header,"posts": posts})

@csrf_exempt
def gamebotdetail(request):
    global bar_features, bar_data,gamebot_prob
    user_id = request.GET['bot_id']
    bot_detail_row = BotDetailData.objects.get(bot_id=int(user_id))
    bot_percentage = str(gamebot_prob)+"%"
    features = ['Average Money','Exp. Get ratio','Item Get ratio','Login Day count(max=88)','Play Time per Day','Same ip Login ratio']
    human_data = human_list
    bot_data = [bot_detail_row.avg_money, bot_detail_row.Exp_get_ratio, bot_detail_row.Item_get_ratio, bot_detail_row.Login_day_count, bot_detail_row.playtime_per_day, bot_detail_row.same_point_connection_rate]
    return render(request,'game_bot_detail.html',{"user_id":user_id,"bot_percentage":bot_percentage,"features":features,"human_data":human_data,"bot_data":bot_data,"bar_features":bar_features,"bar_data":bar_data})
  
def gamebothistory(request):

    page = request.GET.get('page',1)
    history_list = HistoryData.objects.all()
    paginator = Paginator(history_list,10)
    total_page=len(history_list)
    history = paginator.get_page(page)

    page_numbers_range = 5
    max_index = len(paginator.page_range)
    current_page = int(page) if page else 1
    start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
    end_index = start_index + page_numbers_range
    
    # [4]
    if end_index >= max_index:
        end_index = max_index
    paginator_range = paginator.page_range[start_index:end_index]

    
    return render(request,'game_bot_history.html',{"history_list":history_list,"history":history,"paginator_range":paginator_range})
