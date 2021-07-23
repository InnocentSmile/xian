from django.db import models
from DjangoUeditor.models import UEditorField


# Create your models here.
class Base(models.Model):
    t_created = models.DateTimeField(auto_now_add=True)
    t_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Country(Base):
    name = models.CharField("国家名字", max_length=32)

    class Meta:
        verbose_name = '项目国家分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Project(Base):
    logo_img = models.ImageField('项目logo图片', upload_to='project/logo/%Y%m%d', null=True, blank=True, max_length=128,
                                 help_text="250*100")
    name = models.CharField("项目名称", max_length=128)
    city = models.CharField("城市", max_length=64, null=True, blank=True)
    designer = models.CharField("设计师", max_length=32, null=True, blank=True)
    longitude = models.CharField("经度", max_length=128, null=True, blank=True)
    latitude = models.CharField("纬度", max_length=128, null=True, blank=True)
    start_time = models.CharField("起始时间", max_length=32, null=True, blank=True)
    finish_time = models.CharField("完工时间", max_length=32, null=True, blank=True)
    pro_website_url = models.CharField("项目网站", max_length=32, null=True, blank=True)
    pro_simple_desc = models.CharField("项目简单介绍", null=True, blank=True, max_length=128)
    pro_description = UEditorField(verbose_name='项目详细介绍 ', width=600, height=300,
                                   imagePath="project/ueditor/", filePath="project/ueditor/", null=True, blank=True)
    gif_img = models.ImageField('项目gif图片', upload_to='project/gif/%Y%m%d', null=True, blank=True, max_length=128,
                                help_text="690*360")
    country = models.ForeignKey(Country, "项目国家")
    index = models.IntegerField('顺序', default=10)
    is_on_shelf = models.BooleanField("是否上架", default=True)
    is_index_recommend = models.BooleanField("是否首页推荐", default=False)
    is_detail_recommend = models.BooleanField("是否详情页推荐", default=False)

    class Meta:
        verbose_name = '项目'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 项目户型
class ProApartment(Base):
    project = models.ForeignKey(Project, verbose_name="所属项目", on_delete=models.CASCADE)
    name = models.CharField("户型名字", max_length=64)
    apartment_img = models.FileField("户型图片", upload_to="project/apartment/%Y%m%d", null=True, blank=True,
                                     max_length=128, help_text="690*240")
    url = models.CharField('图片地址(图片第三方链接)', max_length=200, null=True, blank=True)
    index = models.IntegerField('顺序', default=100)
    house_area = models.CharField("房间面积", max_length=64)

    class Meta:
        verbose_name = '户型'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 项目轮播图
class ProBanner(Base):
    project = models.ForeignKey(Project, verbose_name="所属项目", on_delete=models.CASCADE)
    name = models.CharField("图片标记", max_length=64)
    img = models.ImageField("项目轮播图片", upload_to="project/banner/%Y%m%d", null=True, blank=True, max_length=128,
                            help_text="690*360")
    index = models.IntegerField('顺序', default=10)
    url = models.CharField('访问地址(图片第三方链接)', max_length=256, null=True, blank=True)

    class Meta:
        verbose_name = '项目轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 项目视频
class ProVideo(Base):
    project = models.ForeignKey(Project, verbose_name="所属项目", on_delete=models.CASCADE)
    name = models.CharField("视频名", max_length=100)
    video = models.FileField("视频", upload_to="project/video/%Y%m%d", null=True, blank=True, max_length=128)
    url = models.CharField('访问地址(视频第三方链接)', max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
