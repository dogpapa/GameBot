from django.db import models
#Create your models here.
class UploadFileModel(models.Model):
    upload_file = models.FileField(upload_to='') # null= True, blank= True
    uploaded_time = models.DateTimeField(auto_now_add=True)

class BotData(models.Model):
    bot_id = models.IntegerField()
    file_name = models.CharField(max_length=100)
    same_point_connection_rate = models.FloatField()
    avg_money = models.FloatField()
    Login_day_count = models.IntegerField()
    Item_get_ratio = models.FloatField()
    playtime_per_day = models.FloatField()
    Exp_get_ratio = models.FloatField()

class BotDetailData(models.Model):
    bot_id = models.IntegerField()
    avg_money = models.FloatField()
    Exp_get_ratio = models.FloatField()
    Item_get_ratio = models.FloatField()
    Login_day_count = models.FloatField()
    playtime_per_day = models.FloatField()
    same_point_connection_rate = models.FloatField()
    
class HistoryData(models.Model):
    file_name = models.CharField(max_length=100)
    log_date = models.DateTimeField(auto_now_add=True)
    all_user_count = models.IntegerField()
    bot_user_count = models.IntegerField()

class HLUserList(models.Model):
    user_id = models.IntegerField()
    playtime_per_day = models.FloatField()
    access_rate = models.FloatField()
    abyss_get_count_per_day = models.FloatField()
    Killed_bynpc_count_per_day = models.FloatField()
    Killed_bypc_count_per_day = models.FloatField()
    Teleport_count_per_day = models.FloatField()
    money_get_count_per_day = models.FloatField()
    Max_level = models.IntegerField()
    user_score = models.FloatField()
    h_or_l = models.IntegerField()