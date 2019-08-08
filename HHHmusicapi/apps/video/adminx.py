# xadmin全局配置
import xadmin
from . import models
# 注册
xadmin.site.register(models.MusicVideo)
xadmin.site.register(models.VideoTag)
