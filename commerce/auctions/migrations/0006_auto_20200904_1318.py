# Generated by Django 3.1.1 on 2020-09-04 11:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20200904_1305'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='price',
            new_name='currprice',
        ),
    ]