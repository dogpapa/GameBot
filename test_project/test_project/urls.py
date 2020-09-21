"""test_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
import test_app.views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',test_app.views.main, name='main'),
    path('bot_user_detect/',test_app.views.bot_user_detect, name='bot_user_detect'),
    path('upload_file/',test_app.views.upload_file, name='upload_file'),
    path('H_L_user_info/',test_app.views.H_L_user_list, name='H_L_user_list'),
    path('game_bot_detail/', test_app.views.gamebotdetail, name='gamebotdetail'),
    path('game_bot_history/', test_app.views.gamebothistory, name='gamebothistory'),
    path('pagenation_bot_user_detect_list/',test_app.views.pagenation_bot_user_detect_list, name="pagenation_bot_user_detect_list")
] 
if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)