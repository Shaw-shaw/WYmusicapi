from django.db import models
from HHHmusicapi.utils.models import BaseModel
# Create your models here.
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    mobile = models.CharField(verbose_name="手机号码", max_length=15, unique=True)
    avatar = models.ImageField(upload_to='avatar', verbose_name='用户头像', null=True, blank=True, help_text="头像图片的大小规格：256x256，或者对应的比例的图片",default='/avatar/20190728153034.jpg')
    follows_count = models.IntegerField(default=0)
    fans_count = models.IntegerField(default=0)

    def follows(self):
        query_follow = self.followed.all()
        return [follow.id for follow in query_follow]

    def fans(self):
        query_fan = self.fan.all()
        return [fan.id for fan in query_fan]

    def addmenu(self):
        query_menu = self.songmenus.all()
        return query_menu

    def createdmenu(self):
        query_createdmenu = self.mysongmenus.all()
        return query_createdmenu

    def my_singers(self):
        my_artist = self.userfollow.all().filter(is_artist=True)
        print(my_artist)
        artist_list = []
        if not my_artist:
            return
        for artist in my_artist:
            artist_list.append(artist.followed_user.singer)
        print(artist_list)
        return artist_list


    class Meta:
        db_table = 'music_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name


class Fan(BaseModel):
    user = models.ForeignKey(to='User',  related_name='userfan', verbose_name="用户", max_length=256, null=True, blank=True, db_constraint=False, on_delete=models.DO_NOTHING)
    fans = models.ForeignKey(to='User',  related_name='fan', verbose_name="粉丝", max_length=256, null=True, blank=True, db_constraint=False, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = '粉丝'
        verbose_name_plural = verbose_name
    def __str__(self):
        return "%s" % self.fans.username

class Follow(BaseModel):
    user = models.ForeignKey(to='User',  related_name='userfollow', verbose_name="用户", max_length=256, null=True, blank=True, db_constraint=False, on_delete=models.DO_NOTHING)
    followed_user = models.ForeignKey(to='User', related_name='followed', verbose_name="关注的人", max_length=256, null=True, blank=True, db_constraint=False, on_delete=models.DO_NOTHING)
    is_artist = models.BooleanField(default=0, verbose_name="是否是歌手")

    class Meta:
        verbose_name = '关注的人'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s" % self.followed_user.username