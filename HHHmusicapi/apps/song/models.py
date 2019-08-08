from HHHmusicapi.utils.models import BaseModel
from django.db import models
from user.models import User
# Create your models here.
from django.db.models import Count
class SingerCategory(BaseModel):
    name = models.CharField(max_length=128, verbose_name="分类名")
    class Meta:
        db_table = "music_singer_category"
        verbose_name = "歌手分类"
        verbose_name_plural = verbose_name
    def __str__(self):
        return "%s" % self.name

class SongMenuTag(BaseModel):
    name = models.CharField(max_length=128, verbose_name="歌单标签名称")
    # languages={
    #
    # }
    # language = models.CharField()

    class Meta:
        db_table = "music_menu_tag"
        verbose_name = "歌单标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s" % self.name


class Singer(BaseModel):
    name = models.CharField(max_length=128, verbose_name="歌手名称")
    introduction = models.CharField(max_length=256, verbose_name="歌手简介")
    avatar = models.ImageField(upload_to='avatar/', verbose_name='歌手海报', null=True, blank=True, help_text="头像图片的大小规格：256x256，或者对应的比例的图片",default='/avatar/20161202101543717.jpg')
    category = models.ForeignKey("SingerCategory", related_name='singers', on_delete=models.DO_NOTHING,
                               db_constraint=False,verbose_name="分类")
    user = models.OneToOneField(User, related_name='singer', on_delete=models.DO_NOTHING,
                               db_constraint=False,verbose_name="用户",null=True)
    def song_list(self):
        '''
        根据该歌手的歌曲热度对歌曲排序
        还可以取可定数目
        :return:
        '''
        return self.songs.all().order_by('heat')

    def album_list(self):
        return self.albums.all().order_by('-create_time')

    class Meta:
        db_table = "music_singer"
        verbose_name = "歌手"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s" % self.name
class Album(BaseModel):
    name = models.CharField(max_length=128, verbose_name="专辑名称")
    introduction = models.CharField(max_length=256, verbose_name="专辑简介")
    singer = models.ForeignKey("Singer", related_name='albums', on_delete=models.CASCADE,
                                verbose_name="所属歌手")
    album_img = models.ImageField(upload_to='album/', verbose_name='歌手海报', null=True, blank=True, help_text="头像图片的大小规格：256x256，或者对应的比例的图片",default='/album/20190723123036845750.jpg')

    def singer_info(self):
        return {'name': self.singer.name,
                'id': self.singer.id
                }

    class Meta:
        db_table = "music_album"
        verbose_name = "专辑"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s" % self.name


class SongMenu(BaseModel):
    name = models.CharField(max_length=128, verbose_name="歌单名称")
    introduction = models.CharField(max_length=256, verbose_name="歌单简介", null=True, blank=True)
    creator = models.ForeignKey(User, related_name='mysongmenus', on_delete=models.CASCADE,
                                  verbose_name="所属用户")
    user = models.ManyToManyField(User, related_name='songmenus', db_constraint=False,
                                  verbose_name="收藏用户",null=True, blank=True)
    menu_img = models.ImageField(upload_to='songmenu/', verbose_name='歌单图片', null=True, blank=True, help_text="头像图片的大小规格：256x256，或者对应的比例的图片",default='/songmenu/20190722170752290043.jpg')
    colnum = models.IntegerField(null=True, default=0, blank=True)
    tags= models.ManyToManyField(to="SongMenuTag", related_name='songmenus', db_constraint=False,
                                  verbose_name="标签",default='华语',blank=True)

    def songs_list(self):
        query_songs = self.songs.all()
        return query_songs

    def comment(self):
        return self.comments.all()

    def creator_info(self):
        return {'username': self.creator.username,'id': self.creator.id}

    def tag(self):
        tag_info_dic = []
        query_tag = self.tags.all()
        print(query_tag)
        if query_tag:
            for tag in query_tag:
                info = {}
                info['name'] = tag.name
                info['id'] = tag.id
                tag_info_dic.append(info)
        return tag_info_dic

    def tag_name(self):
        tag_name = []
        query_tag = self.tags.all()
        if query_tag:
            for tag in query_tag:
                info = {}
                info['name'] = tag.name
                tag_name.append(info)
        return tag_name


    class Meta:
        db_table = "music_song_menu"
        verbose_name = "歌单"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s" % self.name


class Song(BaseModel):
    name = models.CharField(max_length=128, verbose_name="歌曲标题")
    singer = models.ForeignKey("Singer", related_name='songs', on_delete=models.CASCADE,
                                  verbose_name="所属歌手")
    length = models.CharField(max_length=32, verbose_name="时长")
    img = models.ImageField(upload_to='img/', verbose_name='歌曲海报', null=True, blank=True, help_text="头像图",default='/img/radio_1.jpg')
    songmenu = models.ManyToManyField("SongMenu", related_name='songs', db_constraint=False,
                               verbose_name="所属歌单", null=True, blank=True)
    album = models.ForeignKey("Album", related_name='songs', on_delete=models.CASCADE,db_constraint=False,
                              verbose_name="所属专辑",null=True)
    heat = models.CharField(max_length=128, verbose_name="歌曲收藏数", default=None)

    def singer_info(self):
        return {'id':self.singer.id,'name':self.singer.name}

    def album_info(self):
        return {'id': self.album.id, 'name': self.album.name}

    def comment_list(self):
        return self.comments.all()

    def menu_user_id(self):
        return self.songmenu.creator.id

    class Meta:
        db_table = "music_song"
        verbose_name = "歌曲"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s" % self.name

class Comment(BaseModel):
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(to=User, related_name='comments', verbose_name='评论者', on_delete=models.DO_NOTHING, db_constraint=False)
    song = models.ForeignKey(to='Song', related_name='comments', verbose_name='被评论歌曲', on_delete=models.DO_NOTHING,db_constraint=False, null=True, blank=True)
    menu = models.ForeignKey(to='SongMenu', related_name='comments', verbose_name='被评论歌单', on_delete=models.DO_NOTHING,db_constraint=False, null=True, blank=True)
    content = models.CharField(max_length=256, null=False)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    parent_comment = models.ForeignKey(to='self', null=True, blank=True, on_delete=models.DO_NOTHING,db_constraint=False)

    def user_info(self):
        return {'id': self.user.id, 'name': self.user.username,'avatar':self.user.avatar.url}

    def parent_comment_info(self):
        if self.parent_comment:
            return {'id': self.parent_comment.user.id,
                    'name': self.parent_comment.user.username,
                    'parent_comment_content':self.parent_comment.content}
        return None

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = verbose_name



