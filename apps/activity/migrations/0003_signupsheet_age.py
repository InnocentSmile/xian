# Generated by Django 2.1 on 2020-01-04 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0002_signupsheet_activity_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='signupsheet',
            name='age',
            field=models.IntegerField(default=1, verbose_name='年龄'),
            preserve_default=False,
        ),
    ]
