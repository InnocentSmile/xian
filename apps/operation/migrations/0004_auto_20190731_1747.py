# Generated by Django 2.1 on 2019-07-31 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0003_auto_20190518_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='img',
            field=models.ImageField(blank=True, help_text='690*360', max_length=128, null=True, upload_to='resource/image/%Y%m', verbose_name='资料展示图片'),
        ),
    ]
