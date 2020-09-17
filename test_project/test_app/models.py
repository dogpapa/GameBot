from django.db import models
#Create your models here.
class UploadFileModel(models.Model):
    upload_file = models.FileField(upload_to='') # null= True, blank= True
    uploaded_time = models.DateTimeField(auto_now_add=True)

class BotData(models.Model):
    bot_id = models.IntegerField()
    file_name = models.CharField(max_length=100)
    same_point_connection_rate = models.IntegerField()
    avg_money = models.IntegerField()
    Login_day_count = models.IntegerField()
    Item_get_ratio = models.IntegerField()
    playtime_per_day = models.IntegerField()
    Exp_get_ratio = models.IntegerField()

class HistoryData(models.Model):
    file_name = models.CharField(max_length=100)
    log_date = models.DateTimeField(auto_now_add=True)
    all_user_count = models.BigIntegerField()
    bot_user_count = models.BigIntegerField()

