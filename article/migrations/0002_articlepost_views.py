# Generated by Django 2.2.5 on 2019-10-01 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlepost',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
