from rest_framework.generics import ListAPIView
from rest_framework.generics import DestroyAPIView
from rest_framework.views import APIView
# viewsets
from rest_framework.viewsets import ModelViewSet

from rest_framework.request import Request
from rest_framework.response import Response






from rest_framework.permissions import BasePermission

# Create your views here.
from .serializers import SongMenuModelSerializer
from .serializers import SongMenuDetailModelSerializer
from .serializers import ArtistModelSerializer
from .serializers import ArtistDetailModelSerializer
from .serializers import ArtistDescModelSerializer
from .serializers import ArtistAlbumModelSerializer
from .serializers import AlbumListModelSerializer
from .serializers import MyMusiclistModelSerializer
from .serializers import SongDetailModelSerializer
from .serializers import CreateMenuModelSerializer
from .serializers import CommentModelDerializer
from .serializers import CollectionModelDerializer
from .serializers import AddOrDeleteSongModelDerializer
from .models import SongMenu,Singer,Album,Song
from user.models import User
from rest_framework.response import Response
# 根据条件过滤
from django_filters.rest_framework import DjangoFilterBackend
# from django_filters import rest_framework
from rest_framework.filters import OrderingFilter,SearchFilter
from .utils import PlayListPageNumberPagination
from user.authentications import JSONWebTokenAuthentication
from rest_framework.generics import GenericAPIView

from rest_framework import mixins
from HHHmusicapi.settings import constant

# 重写一些需要给源码方法 传参数的方(不同视图传入不同参数)
class MyBaseMethod:
    # 初步过滤
    def get_home_queryset(self,request,filter_field,model,constant=-1):
        home = request.query_params.get('home')
        if not home:
            queryset = model.objects.all()
        else:
            queryset = model.objects.all().order_by(filter_field)[:constant]
        return queryset
# 一些公用的重写源码方法的方法集合(在不同视图调用方式一样)
class BaseMethod(GenericAPIView):
    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            home = self.request.query_params.get('home')
            if self.pagination_class is None or home:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

# 歌单list
class PlaylistListAPIView(MyBaseMethod,mixins.ListModelMixin,BaseMethod):
    """
    主页请求的话返回固定数目的个单数
    通过重写GenericAPIView下的get_queryset方法实现返回不同的queryset
    """
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    def get_queryset(self):
        queryset = super().get_home_queryset(self.request,'-colnum',SongMenu,constant.SONGMENU_LIMIT_COUNT)
        return queryset
    serializer_class = SongMenuModelSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    # django-filters过滤
    # filter_fields = ['tags', ]
    # 搜索
    # http://example.com/api/song/playlist/?search=于   => 止于唇齿 掩于岁月
    # http://example.com/api/song/playlist/?search=古典   => 止于唇齿
    # search_fields = ['name', '=tags__name']
    search_fields = ['@']
    # 排序
    # ordering_fields = ['id', 'students', 'price']
    # http://example.com/api/song/playlist/?ordering=colnum
    ordering_fields = ['colnum', ]
    # 分页
    pagination_class = PlayListPageNumberPagination


# # home 页的歌单列表8个 和 歌单列表 所有
# class PlaylistAPIView(APIView):
#
#     def get(self,request,*args,**kwargs):
#         home = request.query_params.get('home')
#         if not home:
#             queryset = SongMenu.objects.all().order_by('colnum')
#         else:
#             queryset = SongMenu.objects.all().order_by('colnum')[:1]
#         o_menu = SongMenuModelSerializer(queryset, many=True)
#         return Response(o_menu.data)


# 歌单详情页
# 歌单页
class PlayDetailAPIView(APIView):
    def get(self, request, *args, **kwargs):
        menu_id = request.query_params.get('id')
        try:
            o_menu = SongMenu.objects.get(id=menu_id)
        except:
            return Response("404,歌单不存在")
        user_id = request.query_params.get('uid')
        o_user = None
        if user_id:
            o_user = User.objects.filter(id=user_id).first()
        is_col = False
        if o_user:
            if o_menu in (o_user.songmenus.all() | o_user.mysongmenus.all()):
                is_col = True
        seri_menu = SongMenuDetailModelSerializer(o_menu)
        seri_menu.data['is_col'] = is_col
        print(is_col)
        print(seri_menu.data)
        print(type(seri_menu.data))
        return Response({'data':seri_menu.data,
                         'is_col':is_col})

# 歌手list
class ArtistAPIView(MyBaseMethod,mixins.ListModelMixin,GenericAPIView):
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    def get_queryset(self):
        queryset = super().get_home_queryset(self.request,'user__fans_count',Singer)
        return queryset
    serializer_class = ArtistModelSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    # django-filters过滤
    # filter_fields = ['tags', ]
    # 搜索
    # http://example.com/api/song/playlist/?search=于   => 止于唇齿 掩于岁月
    # http://example.com/api/song/playlist/?search=古典   => 止于唇齿
    search_fields = ['name', 'category__name']
    # 排序
    # ordering_fields = ['id', 'students', 'price']
    # http://example.com/api/song/playlist/?ordering=colnum
    # ordering_fields = ['colnum', ]
    # 分页
    pagination_class = PlayListPageNumberPagination

# 歌手页
class ArtistDetailAPIView(APIView):
    def get(self, request, *args, **kwargs):
        artist_id = request.query_params.get('id')
        try:
            o_artist = Singer.objects.get(id=artist_id)
        except:
            return Response("404,歌单不存在")

        seri_artist = ArtistDetailModelSerializer(o_artist)
        return Response(seri_artist.data)

# 歌手简介
class ArtistDescAPIView(APIView):
    def get(self, request, *args, **kwargs):
        artist_id = request.query_params.get('id')
        try:
            o_artist = Singer.objects.get(id=artist_id)
        except:
            return Response("404,歌手不存在")
        seri_artist = ArtistDescModelSerializer(o_artist)
        return Response(seri_artist.data)


# 歌手所属专辑
class ArtistAlbumListAPIView(ListAPIView):
    def get_queryset(self):
        artist_id = self.request.query_params.get('id')
        queryset = Singer.objects.filter(id=artist_id)
        if not queryset:
            return Response("404,歌手不存在")
        return queryset
    serializer_class = ArtistAlbumModelSerializer
    pagination_class = PlayListPageNumberPagination

class aa(ListAPIView):
    pass
# 专辑list
Stock=12
StockListPageNumberPagination=22


class StockListAPIView(MyBaseMethod, mixins.ListModelMixin, BaseMethod):

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_home_queryset(self.request, '-create_time', Stock, constant.STOCK_LIMIT_COUNT)
        return queryset

    serializer_class = AlbumListModelSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ['symbol', 'symbol_category']
    ordering_fields = ['create_time']
    pagination_class = StockListPageNumberPagination


# 我的音乐页
class MyMusiclistAPIView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    def get(self, request, *args, **kwargs ):
        o_user = self.request.user
        seri_menu = MyMusiclistModelSerializer(o_user)
        return Response(seri_menu.data)


class SongDetailAPIView(APIView):
    def get(self, request, *args, **kwargs ):
        song_id = self.request.query_params.get('id')
        if not song_id:
            return Response('404该歌曲不存在')
        try:
            o_song = Song.objects.get(id=song_id)
        except:
            return Response('404该歌曲不存在')
        seri_song = SongDetailModelSerializer(o_song)
        return Response(seri_song.data)

# 创建歌单POST  编辑歌单详情 get  post（携带歌单id）
class CreateMenuAPIView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]

    def check_menu_id(self,request):
        menu_id = self.request.query_params.get('id')
        if not menu_id:
            return False
        try:
            o_menu = SongMenu.objects.get(id=menu_id,creator=request.user)
        except:
            return False
        return o_menu

    def get(self,request,*args,**kwargs):
        o_menu = self.check_menu_id(request)
        if not o_menu:
            return Response('404')
        sseri_menu = CreateMenuModelSerializer(o_menu)
        return Response(sseri_menu.data)

    def post(self,request, *args, **kwargs):
        o_user = request.user
        o_menu = self.check_menu_id(request)
        request.data['creator'] = o_user.id
        # 新建歌单
        if not o_menu:
            o_seri = CreateMenuModelSerializer(data=request.data)
            if o_seri.is_valid(raise_exception=True):
                a=o_seri.validated_data
                o_menu = o_seri.save()
                return Response({'menu_id': o_menu.id,
                                 'name': o_menu.name,
                                 'menu_img': o_menu.menu_img.url})
            else:
                return Response('输入信息有误')
        # 编辑歌单
        o_seri = CreateMenuModelSerializer(data=request.data, instance=o_menu)
        if o_seri.is_valid(raise_exception=True):
            # o_menu = o_seri.update(o_menu,o_seri.validated_data)
            o_menu = o_seri.save()
            return Response({'menu_id':o_menu.id,
                            'name':o_menu.name,
                             'menu_img':o_menu.menu_img.url})


class CommentMenuAPIView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    def post(self,request,*args,**kwargs):
        seri_comment = CommentModelDerializer(data=request.data)
        if seri_comment.is_valid():
            seri_comment.save()
            print(seri_comment.validated_data)
        return Response("ok")

# 收藏歌单
class CollectionMenuAPIView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    def post(self,request,*args,**kwargs):
        seri_coll = CollectionModelDerializer(data=request.data)
        id = request.data.get('id')
        o_menu = SongMenu.objects.filter(id=id).first()
        if not o_menu:
            return Response('404')
        user_id = request.data.get('user')
        o_user = User.objects.filter(id=user_id).first()
        if o_menu in (o_user.songmenus.all() | o_user.mysongmenus.all()):
            return Response('404,自己的或已经收藏过得歌单')
        user_lis_pk = []
        for user in o_menu.user.all():
            user_lis_pk.append(user.pk)
        user_lis_pk.append(user_id)

        request.data['user'] = user_lis_pk
        if seri_coll.is_valid(raise_exception=True):
            a=seri_coll.update(instance=o_menu,validated_data=seri_coll.validated_data)
            o_menu.colnum +=1
            o_menu.save()
            print(a)
            # seri_coll.save()
            print(seri_coll.validated_data)
        return Response("ok")


# 前端传 menu_id song_id 自己有 user_id    歌单'id', 'creator', 'songs'
class CollectionSongAPIView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]

    def post(self,request,*args,**kwargs):
        menu_user_id = request.user.id
        add_song_id = request.data.get('song_id')
        menu_id = request.data.get('menu_id')
        o_menu = SongMenu.objects.filter(id=menu_id).first()
        self.request.data['creator']=menu_user_id
        song_lis_pk = []
        for song in o_menu.songs.all():
            song_lis_pk.append(song.pk)
        if add_song_id in song_lis_pk:
            return Response('改歌单已经有该歌曲')
        song_lis_pk.append(add_song_id)
        self.request.data['songs'] = song_lis_pk
        seri_menu = AddOrDeleteSongModelDerializer(data=request.data)
        if seri_menu.is_valid(raise_exception=True):
            # seri_menu.validated_data
            a = seri_menu.update(instance=o_menu, validated_data=seri_menu.validated_data)
            o_song = Song.objects.filter(id=add_song_id).first()
            heat = int(o_song.heat)+1
            o_song.heat = str(heat)
            o_song.save()
            return Response('ok')
        return Response('no')
# 前端传个来menu_id  song_id   jwt认证通过可以获取user_id
# 去
class DeleteSongAPIView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = AddOrDeleteSongModelDerializer

    def post(self, request, *args, **kwargs):
        menu_user_id = request.user.id
        add_song_id = request.data.get('song_id')
        menu_id = request.data.get('menu_id')
        o_menu = SongMenu.objects.filter(id=menu_id).first()
        self.request.data['creator'] = menu_user_id
        song_lis_pk = []
        for song in o_menu.songs.all():
            song_lis_pk.append(song.pk)
        if add_song_id not in song_lis_pk:
            return Response('输入有误')
        song_lis_pk.remove(add_song_id)
        self.request.data['songs'] = song_lis_pk
        seri_menu = AddOrDeleteSongModelDerializer(data=request.data)
        if seri_menu.is_valid(raise_exception=True):
            # seri_menu.validated_data
            a = seri_menu.update(instance=o_menu, validated_data=seri_menu.validated_data)
            o_song = Song.objects.filter(id=add_song_id).first()
            heat = int(o_song.heat) - 1
            o_song.heat = str(heat)
            o_song.save()
            return Response('ok')
        return Response('no')


class DeleteMenuAPIView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]

    def check_menu_id(self,request):
        menu_id = self.request.data.get('menu_id')
        if not menu_id:
            return False
        try:
            query_menu = SongMenu.objects.filter(id=menu_id,creator=request.user)
        except:
            return False
        return query_menu

    def post(self,request, *args, **kwargs):
        print(request.user)
        query_menu = self.check_menu_id(request)
        if not query_menu:
            return Response('歌单不存在')
        query_menu.delete()
        return Response('删除成功')