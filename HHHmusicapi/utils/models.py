from django.db import models

# 作为基类的Model
class BaseModel(models.Model):
    is_show=models.BooleanField(verbose_name="是否上架",default=True)
    is_delete=models.BooleanField(verbose_name="逻辑删除",default=False)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', null=True, blank=True)
    class Meta:
        # 在基类的model中添加，代表数据库迁移时不会形成一张独立的表
        abstract = True



