# Generated by Django 2.1 on 2019-05-12 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20190512_2232'),
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=256)),
                ('session_key', models.CharField(max_length=64)),
                ('userid', models.IntegerField()),
                ('t_expiration', models.DateTimeField()),
            ],
        ),
    ]
