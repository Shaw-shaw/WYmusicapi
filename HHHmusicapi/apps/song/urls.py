
from django.contrib import admin
from django.urls import path,include,re_path
from . import views
urlpatterns = [
    # 用ListAPIView来返回
    path('playlist/', views.PlaylistListAPIView.as_view()),
    # 用APIView来完成自己的根据不同情况的自定义返回 通过重写get_queryset舍弃该方案
    # path('playlist/', views.PlaylistAPIView.as_view()),
    # 根据歌单id返回歌单详情页的所有信息
    path('playdetail/', views.PlayDetailAPIView.as_view()),
    # 歌手页
    path('artist/', views.ArtistAPIView.as_view()),
    # 歌手详情页
    path('artistdetai/', views.ArtistDetailAPIView.as_view()),
    # 歌手简介
    path('artistdesc/', views.ArtistDescAPIView.as_view()),
    # 歌手专辑
    path('artist/album/', views.ArtistAlbumListAPIView.as_view()),
    # 所有专辑
    path('album/', views.AlbumlistListAPIView.as_view()),
    # 我的音乐页
    path('my/music/playlist/', views.MyMusiclistAPIView.as_view()),
    # path('my/music/artist', views.AlbumlistListAPIView.as_view()),
    # 歌曲详情页
    path('', views.SongDetailAPIView.as_view()),
    # 创建歌单加上id就是编辑
    path('my/music/create/', views.CreateMenuAPIView.as_view()),
    # path('my/music/edit/', views.EditMenuAPIView.as_view()),
    # 评论功能
    path('my/comment/', views.CommentMenuAPIView.as_view()),
    # path('comment/music/', views.CommentMusicAPIView.as_view()),
    # 收藏歌单
    path('my/collection/menu/', views.CollectionMenuAPIView.as_view()),
    # 删除歌单
    path('my/delete/menu/', views.DeleteMenuAPIView.as_view()),
    # 收藏歌曲
    path('my/collection/song/', views.CollectionSongAPIView.as_view()),
    # 删除歌单中某歌曲
    path('my/delete/song/', views.DeleteSongAPIView.as_view()),

]
