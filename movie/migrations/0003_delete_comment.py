# Generated by Django 2.2.4 on 2019-09-16 18:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0002_auto_20190916_1652'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
