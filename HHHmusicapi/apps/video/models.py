from django.db import models

# Create your models here.
from user.models import User
from HHHmusicapi.utils.models import BaseModel
class VideoTag(BaseModel):
    name = models.CharField(max_length=256,verbose_name='名称')
    class Meta:
        db_table = "video_video_tag"
        verbose_name = "MV_tag"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s" % self.name


class MusicVideo(BaseModel):
    video_resolution = (
        (0, '高清'),
        (1, '超清'),
        (2, '1080P')
    )
    title = models.CharField(max_length=256,verbose_name='标题')
    artist = models.ForeignKey(to=User,related_name='videos', on_delete=models.DO_NOTHING, verbose_name='歌手', db_constraint=False)
    video_img = models.ImageField(upload_to='video_img/', verbose_name='mv图片', null=True, blank=True, help_text="头像图片的大小规格：256x256，或者对应的比例的图片",default='/video_img/20161202101543717.jpg')
    length = models.CharField(max_length=32, verbose_name="时长")
    video_tag = models.ForeignKey(to='VideoTag',max_length=256,verbose_name='video标签',on_delete=models.DO_NOTHING)
    video_id = models.CharField(max_length=256,verbose_name='video外链id')
    video_resolution = models.SmallIntegerField(choices=video_resolution, default=0, verbose_name="高清")
    class Meta:
        db_table = "video_videos"
        verbose_name = "MV"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s" % self.title




