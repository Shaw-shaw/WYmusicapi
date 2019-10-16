from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from HHHmusicapi.settings import constant
from HHHmusicapi.libs.yuntongxun import send_sms

from rest_framework.generics import GenericAPIView




from . import models
from rest_framework_jwt.utils import jwt_payload_handler
from rest_framework_jwt.utils import jwt_encode_handler
from rest_framework_jwt.utils import jwt_response_payload_handler
import re
# from HHHmusicapi.utils.smtp import QqEmail
# Create your views here.
from .serializers import UserModelDerializer
from .serializers import UserModelSerializer
from django_redis import get_redis_connection
from celery_task.send_email_task import send
conn = get_redis_connection()
# send_email = QqEmail()
# 短信验证码
from .authentications import SMSRateThrottle
import random
from django.core.cache import cache
class SMSAPIView(APIView):
    throttle_classes = [SMSRateThrottle]
    def get(self, request, *args, **kwargs):
        mobile = request.query_params.get('mobile')
        # 字段必须
        if not mobile:
            return Response({
                "status": 2,
                "msg": "mobile参数是必须的"
            })
        # 后台要多mobile数据进行安全校验
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return Response({
                'status': 2,
                'msg': '手机号有误',
            })
        # 生成验证码
        code = ""
        for i in range(6):
            code += str(random.randint(0, 9))

        # redis存储
        cache.set(mobile, code, constant.SMS_EXPIRE_TIME)

        # 调用短信第三方
        result = send_sms(mobile, (code, constant.SMS_EXPIRE_TIME // 60), 1)

        # 响应前台：发生成功或失败
        if not result:
            return Response({
                'status': 1,
                'result': '短信发生失败'
            })
        return Response({
            'status': 0,
            'result': '短信发生成功'
        })


class RegisterAPIView(APIView):

    def post(self, request, *args, **kwargs):
        mobile = request.data.get('mobile')
        code = request.data.get('sms')
        # 校验验证码：从redis取出旧的验证码
        old_code = cache.get(mobile)
        if not old_code:
            return Response({
                'result': '验证码失效'
            })
        if code != old_code:
            return Response({
                'result': '验证码错误'
            })
        email = request.data.get('email')
        bac_dic = {'status': 0, 'msg': ''}
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            bac_dic['msg'] = '请输入有效手机号'
            bac_dic['status'] = 2
        if not re.match(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', email):
            bac_dic['msg'] = '请输入邮箱有效'
            bac_dic['status'] = 2
        # 将注册数据存到数据库
        try:
            serializer_user = UserModelDerializer(data=request.data)
            if serializer_user.is_valid(raise_exception=True):
                print(serializer_user.validated_data)
                obj = serializer_user.save()  # type: models.User
                obj.set_password(obj.password)
                obj.is_active=0
                obj.save()
                username = request.data.get('username')
                conn.setnx(username, 1)
        except Exception as e:
            bac_dic['msg'] = '输入数据异常%s'%e
            bac_dic['status'] = 4
        # 未激活的用户数据存到数据库后 发送邮件 请求激活
        else:
            # suffix = get_suffix()
            username = request.data.get('username')
            try:
                conn.setnx(username,1)
                # conn.expire(username, 300)
                recv = request.data.get('email')
                url = 'http://127.0.0.1:8000/user/register/?username=' + username
                content = ('<html><body><h1>Hello, Welcome Join Us</h1>' +
                         '<p><a href=%s>请点击激活账户</a>...</p>'%url +
                         '</body></html>', 'HTML', 'utf-8')
                result = send.delay(recv, content)
                # send_email.send(recv, content)
                print(result.id)
            except Exception as e:
                bac_dic['msg'] = '网络异常%s'%e
                bac_dic['status'] = 5
            else:
                bac_dic['msg'] = '请前往邮箱进行账号激活'
        return Response(bac_dic)

    def get(self,request,*args,**kwargs):
        username = request.GET.get('username')
        print(username)
        if not username:
            return Response('404')
        if not conn.exists(username):
            return Response('异常')
        user_o = models.User.objects.filter(username=username).first()
        user_o.is_active = 1
        user_o.save()
        return Response({'status':0, 'msg':'激活成功'})


class HomeAPIView(APIView):
    # authentication_classes = [JSONWebTokenAuthentication]
    def get(self,request, *args, **kwargs):
        res_dic = {'status': 100, 'msg': ''}
        user_id = request.query_params.get('id')
        # 验证url的合法性
        if not user_id:
            res_dic['status'] = 101
            res_dic['msg'] = '访问页面不存在'
            return Response(res_dic)
        # 验证用户id的合法性
        o_user = models.User.objects.filter(id=user_id).first()
        if not o_user:
            res_dic['status'] = 101
            res_dic['msg'] = '访问页面不存在'
            return Response(res_dic)
        # 通过校验就需要返回用户信息  以及创建的歌单和收藏的歌单
        res = UserModelSerializer(o_user)
        return Response(res.data)




# 校验用户名
class CheckUserNameAPIView(APIView):
    def get(self, request, *args, **kwargs):
        username = request.query_params.get('username')
        if not username:
            return Response({
                "status": 2,
                "msg": "username参数是必须的"
            })

        # 安全校验
        if len(username) > 8 or len(username) == 0:
            return Response({
                'status': 2,
                'msg': '用户名格式有误',
            })

        try:
            models.User.objects.get(username=username)
        except:
            return Response({
                "status": 0,
                "msg": "用户名未注册"
            })
        return Response({
            "status": 1,
            "msg": "用户名已注册"
        })


# 校验用户名
class CheckEmailAPIView(APIView):
    def get(self, request, *args, **kwargs):
        email = request.query_params.get('email')
        if not email:
            return Response({
                "status": 2,
                "msg": "email参数是必须的"
            })

        # 安全校验
        if re.match(r'^[a-zA-Z0-9_-]@[a-zA-Z0-9_-](\.[a-zA-Z0-9_-]+)$',email):
            return Response({
                'status': 2,
                'msg': '邮箱格式有误',
            })

        try:
            models.User.objects.get(email=email)
        except:
            return Response({
                "status": 0,
                "msg": "该邮箱未注册可用"
            })
        return Response({
            "status": 1,
            "msg": "该邮箱已注册"
        })