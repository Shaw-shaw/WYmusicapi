import jwt
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_jwt.authentication import jwt_decode_handler
from rest_framework_jwt.authentication import get_authorization_header
from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication
class JSONWebTokenAuthentication(BaseJSONWebTokenAuthentication):
        def authenticate(self, request):
            # 采用drf获取token的手段 - HTTP_AUTHORIZATION - Authorization
            token = get_authorization_header(request)
            if not token:
                raise AuthenticationFailed('Authorization 字段是必须的')
            # 可以添加反扒措施：原功能是token有前缀

            # drf-jwt认证校验算法
            try:
                payload = jwt_decode_handler(token)
            except jwt.ExpiredSignature:
                raise AuthenticationFailed('签名过期')
            except jwt.InvalidTokenError:
                raise AuthenticationFailed('非法用户')
            user = self.authenticate_credentials(payload)
            # 将认证结果丢该drf
            return user, token


# 短信频率认证
from rest_framework.throttling import SimpleRateThrottle
class SMSRateThrottle(SimpleRateThrottle):
    scope = 'sms'
    def get_cache_key(self, request, view):
        mobile = request.query_params.get('mobile')
        return 'Throttle:%s' % mobile