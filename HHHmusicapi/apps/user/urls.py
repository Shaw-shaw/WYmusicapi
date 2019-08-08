

from django.urls import path,re_path
from . import views
from rest_framework_jwt.views import obtain_jwt_token
urlpatterns = [
    path('login/', obtain_jwt_token),
    path('register/', views.RegisterAPIView.as_view(),),
    path('home/', views.HomeAPIView.as_view(),),
    # 短信验证码
    path('sms/', views.SMSAPIView.as_view()),
    path('username/', views.CheckUserNameAPIView.as_view()),
    path('email/', views.CheckEmailAPIView.as_view()),

]
