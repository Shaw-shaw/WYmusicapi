# 导入项目配置文件类(用于获取秘钥, 秘钥的获取可以自定义, 不必须在此类中获取)
from django.conf import settings
# 导入加解密类
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
class DumpLoad:
    def dump(self,*args, **kwargs):
        print(args)
        print(kwargs,type(kwargs))
# # 获取加解密类
# # 参数1: 自定义的秘钥(此处调用的是项目配置生成的KEY)   ,   参数2: 有效时间(秒)
# # serializer = Serializer(settings.SECRET_KEY, 3600)
# serializer = Serializer("secretKey", 3600)
# # 获取加密信息, 最好是字典格式
# info = {"infoKey": "infoContent"}
# # 信息加密
# res = serializer.dumps(info)
# print('二进制加密信息',res)
# # 加密后是二进制的数据, 默认是utf-8的编码
# res = res.decode("utf8")  # 字节类型转为字符串
# print('字符串加密信息',res)
# # 信息解密
# res = serializer.loads(res)
# print('解密后的信息',res)
# infoContent = res["infoKey"]
# print(infoContent)
aa = DumpLoad()
aa.dump('111','222',a='xxx',b='yyy')