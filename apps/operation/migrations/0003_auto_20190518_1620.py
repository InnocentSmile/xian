# Generated by Django 2.1 on 2019-05-18 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0002_auto_20190512_2232'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='index',
            field=models.IntegerField(default=100, verbose_name='顺序'),
        ),
        migrations.AddField(
            model_name='resource',
            name='is_on_shelf',
            field=models.BooleanField(default=True, verbose_name='是否展示'),
        ),
        migrations.AlterField(
            model_name='userfavorite',
            name='fav_id',
            field=models.IntegerField(default=0, verbose_name='项目或课程id'),
        ),
    ]
