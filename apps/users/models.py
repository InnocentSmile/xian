import json

from django.db import models
from DjangoUeditor.models import UEditorField

# Create your models here.

GENDER = (
    (1, "男"),
    (2, "女"),
    (0, "未知"),
)


class Base(models.Model):
    t_created = models.DateTimeField(auto_now_add=True)
    t_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(Base):
    wx_openid = models.CharField(max_length=64, unique=True)
    avatarUrl = models.CharField("微信头像", max_length=256, null=True, blank=True)
    nickName = models.CharField("微信昵称", max_length=64, null=True, blank=True)
    gender = models.IntegerField("性别", choices=GENDER, null=True, blank=True)
    city = models.CharField("城市", max_length=64, null=True, blank=True)
    country = models.CharField("国家", max_length=64, null=True, blank=True)
    province = models.CharField("省份", max_length=64, null=True, blank=True)

    class Meta:
        verbose_name = '用户基本信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.wx_openid


class Banner(Base):
    title = models.CharField('标题', max_length=64)
    image = models.ImageField('轮播图', upload_to='index/banner/%Y%m%d', max_length=128,null=True, blank=True,help_text="750*1100")
    url = models.URLField('访问地址', max_length=256, null=True, blank=True)
    index = models.IntegerField('顺序', default=100)
    is_on_shelf = models.BooleanField("是否上架", default=True)
    project_id = models.IntegerField('项目id', null=True, blank=True)

    class Meta:
        verbose_name = '首页轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Company(Base):
    logo_img = models.ImageField('公司logo图片', upload_to='company/logo/%Y%m%d', max_length=128, null=True, blank=True)
    video = models.FileField("公司视频", upload_to="company/video/%Y%m%d", max_length=128, null=True, blank=True)
    description = UEditorField(verbose_name='公司详情 ', width=600, height=300,
                               imagePath="company/ueditor/", filePath="company/ueditor/", null=True, blank=True)
    bottom = models.TextField("公司底部信息", default=json.dumps({}))

    class Meta:
        verbose_name = '公司介绍'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.description[:20]


class Session(models.Model):
    token = models.CharField(max_length=256)
    session_key = models.CharField(max_length=64)
    userid = models.IntegerField()
    t_expiration = models.DateTimeField()


# class WxForm(models.Model):
#     userid = models.IntegerField()
#     form_id = models.CharField(max_length=64)
#     source = models.CharField(max_length=64, null=True, blank=True)
#     isUsed = models.BooleanField("是否可用", default=True)
#     t_created = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         unique_together = ("userid", "form_id")
