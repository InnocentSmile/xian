# Generated by Django 2.1 on 2019-05-24 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='desc',
            field=models.TextField(blank=True, null=True, verbose_name='课程描述'),
        ),
    ]
