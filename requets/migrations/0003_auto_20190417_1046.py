# Generated by Django 2.2 on 2019-04-17 08:46

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('requets', '0002_requet_pub_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='requet',
            name='aprove_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='requet',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 17, 8, 46, 37, 219347, tzinfo=utc)),
        ),
    ]
