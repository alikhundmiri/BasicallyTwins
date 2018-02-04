# Generated by Django 2.0.1 on 2018-02-01 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_auto_20180131_1423'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='claimable',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_name',
            field=models.CharField(default='Reavling', max_length=50),
        ),
        migrations.AlterField(
            model_name='product_catagory',
            name='catagory_name',
            field=models.CharField(default='BlueSkin', max_length=50),
        ),
    ]
