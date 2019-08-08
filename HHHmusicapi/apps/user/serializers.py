from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import User
from song.serializers import SongMenuModelSerializer

# 用户反序列化器 注册用
class UserModelDerializer(ModelSerializer):
    # password = serializers.CharField(min_length=3,required=True)
    # username = serializers.CharField(max_length=6, required=True)
    # email = serializers.EmailField(max_length=254, required=True)
    # mobile = serializers.CharField(min_length=11, required=True)
    class Meta:
        model = User
        fields = ["username", "mobile", 'email','password']

# home 页用
class UserModelSerializer(ModelSerializer):
    addmenu = SongMenuModelSerializer(many=True)
    createdmenu = SongMenuModelSerializer(many=True)
    class Meta:
        model = User
        fields = ["username", "follows", 'fans', 'addmenu','createdmenu']
        order_by = 'create_time'
