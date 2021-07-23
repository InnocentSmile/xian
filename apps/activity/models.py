from django.db import models


class Base(models.Model):
    t_created = models.DateTimeField(auto_now_add=True)
    t_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Activity(Base):
    name = models.CharField("活动名称", max_length=64)
    into_img = models.ImageField("入口图片", upload_to="activity/image/%Y%m%d", null=True, blank=True, max_length=128)
    master_img = models.ImageField("活动主图", upload_to="activity/image/%Y%m%d", null=True, blank=True, max_length=128)
    is_on_shelf = models.BooleanField("是否上架", default=True)

    class Meta:
        verbose_name = '活动'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Signupsheet(Base):
    user_id = models.IntegerField("用户id")
    activity_id = models.IntegerField("活动id")
    name = models.CharField("姓名", max_length=32)
    contact_info = models.CharField("联系方式", max_length=32)
    age = models.IntegerField("年龄")
    email = models.CharField("邮箱地址", max_length=32,null=True, blank=True)

    class Meta:
        verbose_name = '活动报名表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name