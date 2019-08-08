from user.serializers import UserModelSerializer
def jwt_response_payload_handler(token, user=None, request=None):
    print()
    return {
        'token': token,

        'user': user.username
    }
    # restful 规范
    # return {
    #     'status': 0,
    #     'msg': 'OK',
    #     'data': {
    #         'token': token,
    #         'username': user.username
    #     }
    # }


from django.contrib.auth.backends import ModelBackend
from user.models import User
import re
class JWTModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        :param request:
        :param username: 前台传入的用户名
        :param password: 前台传入的密码
        :param kwargs:
        :return:
        """
        try:
            if re.match(r'^1[3-9]\d{9}$', username):
                user = User.objects.get(mobile=username)
            elif re.match(r'.*@.*', username):
                user = User.objects.get(email=username)
            else:
                user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None  # 认证失败就返回None即可，jwt就无法删除token
        # 用户存在，密码校验通过，是活着的用户 is_active字段为1
        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user  # 认证通过返回用户，交给jwt生成token