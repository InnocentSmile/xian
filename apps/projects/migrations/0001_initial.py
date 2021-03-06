# Generated by Django 2.1 on 2019-05-11 22:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('t_created', models.DateTimeField(auto_now_add=True)),
                ('t_modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=32, verbose_name='项目国家')),
            ],
            options={
                'verbose_name': '项目国家分类',
                'verbose_name_plural': '项目国家分类',
            },
        ),
        migrations.CreateModel(
            name='ProApartment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('t_created', models.DateTimeField(auto_now_add=True)),
                ('t_modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=64, verbose_name='户型名字')),
                ('apartment_img', models.FileField(blank=True, max_length=128, null=True, upload_to='project/apartment/%Y%m%d', verbose_name='户型图片')),
                ('url', models.CharField(blank=True, max_length=200, null=True, verbose_name='访问地址(图片第三方链接)')),
                ('house_area', models.CharField(max_length=64, verbose_name='房间面积')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProBanner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('t_created', models.DateTimeField(auto_now_add=True)),
                ('t_modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=64, verbose_name='图片标记')),
                ('img', models.ImageField(blank=True, max_length=128, null=True, upload_to='project/banner/%Y%m%d', verbose_name='项目轮播图片')),
                ('url', models.CharField(blank=True, max_length=256, null=True, verbose_name='访问地址(图片第三方链接)')),
            ],
            options={
                'verbose_name': '轮播课程',
                'verbose_name_plural': '轮播课程',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('t_created', models.DateTimeField(auto_now_add=True)),
                ('t_modified', models.DateTimeField(auto_now=True)),
                ('logo_img', models.ImageField(blank=True, max_length=128, null=True, upload_to='project/logo/%Y%m', verbose_name='项目logo图片')),
                ('name', models.CharField(max_length=128, verbose_name='项目名称')),
                ('city', models.CharField(blank=True, max_length=64, null=True, verbose_name='城市')),
                ('address', models.CharField(blank=True, max_length=128, null=True, verbose_name='地址')),
                ('designer', models.CharField(blank=True, max_length=32, null=True, verbose_name='设计师')),
                ('start_time', models.CharField(blank=True, max_length=32, null=True, verbose_name='起始时间')),
                ('finish_time', models.CharField(blank=True, max_length=32, null=True, verbose_name='完工时间')),
                ('pro_website_url', models.CharField(blank=True, max_length=32, null=True, verbose_name='项目网站')),
                ('pro_simple_desc', models.TextField(blank=True, null=True, verbose_name='项目简单介绍')),
                ('pro_description', models.TextField(blank=True, null=True, verbose_name='项目详细介绍')),
                ('pro_img', models.ImageField(upload_to='project/%Y%m%d', verbose_name='项目列表页图片(gif或者静图)')),
                ('is_on_shelf', models.BooleanField(default=True, verbose_name='是否上架')),
                ('is_index_recommend', models.BooleanField(default=False, verbose_name='是否首页推荐')),
                ('is_detail_recommend', models.BooleanField(default=False, verbose_name='是否详情页推荐')),
                ('country', models.ForeignKey(on_delete='项目国家', to='projects.Country')),
            ],
            options={
                'verbose_name': '项目',
                'verbose_name_plural': '项目',
            },
        ),
        migrations.CreateModel(
            name='ProVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('t_created', models.DateTimeField(auto_now_add=True)),
                ('t_modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, verbose_name='视频名')),
                ('video', models.FileField(blank=True, max_length=128, null=True, upload_to='project/video/%Y%m%d', verbose_name='视频')),
                ('url', models.CharField(blank=True, max_length=200, null=True, verbose_name='访问地址(视频第三方链接)')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Project', verbose_name='所属项目')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='probanner',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Project', verbose_name='所属项目'),
        ),
        migrations.AddField(
            model_name='proapartment',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Project', verbose_name='所属项目'),
        ),
    ]
