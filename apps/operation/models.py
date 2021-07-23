from django.db import models


# Create your models here.

class Base(models.Model):
    t_created = models.DateTimeField(auto_now_add=True)
    t_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserFavorite(Base):
    '''用户收藏'''
    FAV_TYPE = (
        (1, '项目'),
        (2, '课程'),
    )

    user_id = models.IntegerField("用户id")
    fav_id = models.IntegerField('项目或课程id', default=0)
    fav_type = models.IntegerField(verbose_name='收藏类型', choices=FAV_TYPE, default=1)

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name


class Resource(Base):
    name = models.CharField("资料名称", max_length=64)
    img = models.ImageField("资料展示图片", upload_to="resource/image/%Y%m", null=True, blank=True, max_length=128,help_text="690*360")
    download = models.FileField("资源文件", upload_to="resource/download/%Y%m", max_length=128, null=True, blank=True)
    index = models.IntegerField('顺序', default=100)
    is_on_shelf = models.BooleanField("是否展示", default=True)

    class Meta:
        verbose_name = '资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class RDUser(Base):
    user_id = models.IntegerField("用户id")
    name = models.CharField("姓名", max_length=32)
    contact_info = models.CharField("联系方式", max_length=32)
    email = models.CharField("邮箱地址", max_length=32)
    is_subscribe = models.BooleanField("是否订阅westbank西岸集团邮件", default=True)

    class Meta:
        verbose_name = '资料下载表单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Appointment(Base):
    user_id = models.IntegerField("用户id")
    name = models.CharField("姓名", max_length=32)
    contact_info = models.CharField("联系方式", max_length=32)
    email = models.CharField("邮箱地址", max_length=32)
    city = models.CharField("预约品鉴城市", max_length=16)
    msg = models.CharField("用户留言", max_length=128, null=True, blank=True)
    is_subscribe = models.BooleanField("是否订阅westbank西岸集团邮件", default=True)

    class Meta:
        verbose_name = '预约品鉴'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
