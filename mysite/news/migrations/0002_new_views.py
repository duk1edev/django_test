# Generated by Django 3.0.8 on 2020-10-02 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='new',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]
