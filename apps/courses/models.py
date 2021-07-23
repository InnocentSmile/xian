from django.db import models


# Create your models here.

class Base(models.Model):
    t_created = models.DateTimeField(auto_now_add=True)
    t_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


COURSE_TIME_TYPE = (
    ("最新课程", "最新课程"),
    ("往期课程", "往期课程"),
)


class Course(Base):
    time_type = models.CharField("课程时间类型", choices=COURSE_TIME_TYPE, max_length=16)
    name = models.CharField("课程名称", max_length=64)
    video = models.FileField("课程视频", upload_to="course/video/%Y%m%d", null=True, blank=True, max_length=128)
    img = models.ImageField("课程图片", upload_to="course/image/%Y%m%d", null=True, blank=True, max_length=128,help_text="690*360")
    audio = models.FileField("课程音频", upload_to="course/audio/%Y%m%d", null=True, blank=True, max_length=128)
    desc = models.TextField("课程描述", null=True, blank=True)
    is_on_shelf = models.BooleanField("是否上架", default=True)
    is_index_recommend = models.BooleanField("是否首页推荐", default=False)
    is_detail_recommend = models.BooleanField("是否详情页推荐", default=False)

    class Meta:
        verbose_name = '课程信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
