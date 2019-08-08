from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import SongMenu,Song,Comment,Singer,Album
from user.models import User


# playlist时歌单序列化器
class SongMenuModelSerializer(ModelSerializer):
    class Meta:
        model = SongMenu
        fields = ["name", "menu_img", 'colnum', 'id']

# 评论序列化操作
class CommentModelSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['nid', 'user_info', 'content', 'create_time','parent_comment_info']
        # fields = '__all__'

class CommentModelDerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['user', 'song', 'menu', 'content', 'parent_comment']
# 歌曲序列化操作 list 展示时用
class SongModelSerializer(ModelSerializer):
    class Meta:
        model = Song
        fields = ['id','name','length','singer_info','album_info']


# 歌曲详情序列化操作 带评论的那页
class SongDetailModelSerializer(ModelSerializer):
    comment_list = CommentModelSerializer(many=True)
    class Meta:
        model = Song
        fields = ['id','name','singer_info','album_info','comment_list']




# 歌单详情页
class SongMenuDetailModelSerializer(ModelSerializer):
    songs_list = SongModelSerializer(many=True)
    comment = CommentModelSerializer(many=True)

    class Meta:
        model = SongMenu
        fields = ['name', 'introduction', 'tag', 'creator_info','colnum','menu_img','songs_list','comment']


class ArtistModelSerializer(ModelSerializer):
    class Meta:
        model = Singer
        fields = ['name', 'avatar', 'id']


class ArtistDetailModelSerializer(ModelSerializer):
    song_list = SongModelSerializer(many=True)
    class Meta:
        model = Singer
        fields = ['name', 'avatar', 'song_list']

#歌手详情
class ArtistDescModelSerializer(ModelSerializer):
    # my_singers = ArtistModelSerializer(many=True)
    class Meta:
        model = Singer
        fields = ['introduction']


# 专辑序列化(歌手页用)
class AlbumModelSerializer(ModelSerializer):
    class Meta:
        model = Album
        fields = ['id', 'name','album_img','create_time']


# 专辑序列化所有专辑
class AlbumListModelSerializer(ModelSerializer):
    class Meta:
        model = Album
        fields = ['id', 'name', 'album_img', 'singer_info']


# 歌手所有专辑
class ArtistAlbumModelSerializer(ModelSerializer):
    album_list = AlbumModelSerializer(many=True)

    class Meta:
        model = Singer
        fields = ['album_list']


# 我的音乐页
class MyMusiclistModelSerializer(ModelSerializer):
    songmenus = SongMenuModelSerializer(many=True)
    mysongmenus = SongMenuModelSerializer(many=True)
    my_singers = ArtistModelSerializer(many=True)

    class Meta:
        model = User
        fields = ['my_singers', 'mysongmenus', 'songmenus']


# 创建编辑歌单的  序列化器
class CreateMenuModelSerializer(ModelSerializer):
    # name = serializers.CharField()
    # def get_creator(self, creator):
    #     return creator.id
    class Meta:
        model = SongMenu
        # fields = ['name', 'creator', 'introduction', 'tags', 'menu_img']
        fields = ['name', 'introduction', 'tags', 'menu_img','creator']
        # write_only_fields = ['creator']
        # read_only_fields = ['name','introduction', 'tags','menu_img']


# 收藏歌单反序列化
class CollectionModelDerializer(ModelSerializer):
    class Meta:
        model = SongMenu
        fields = ['user', 'id']
# 添加歌曲到某歌单反序列化
class AddOrDeleteSongModelDerializer(ModelSerializer):
    class Meta:
        model = SongMenu
        fields = ['id', 'creator','songs']







