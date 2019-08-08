# xadmin全局配置
import xadmin
from xadmin import views

class GlobalSettings(object):
    """xadmin的全局配置"""
    site_title = "音你太美"  # 设置站点标题
    site_footer = "用歌声释放你我"  # 设置站点的页脚
    # menu_style = "accordion"  # 设置菜单折叠

xadmin.site.register(views.CommAdminView, GlobalSettings)


from . import models
# 注册
xadmin.site.register(models.SongMenu)
xadmin.site.register(models.Song)
xadmin.site.register(models.Album)
xadmin.site.register(models.Comment)
xadmin.site.register(models.Singer)
xadmin.site.register(models.SingerCategory)
xadmin.site.register(models.SongMenuTag)
