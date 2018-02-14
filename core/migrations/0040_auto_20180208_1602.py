# Generated by Django 2.0.1 on 2018-02-08 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0039_auto_20180208_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_name',
            field=models.CharField(default='Stick ship', max_length=50),
        ),
        migrations.AlterField(
            model_name='product_catagory',
            name='catagory_name',
            field=models.CharField(default='Glowing Bulb', max_length=50),
        ),
        migrations.AlterField(
            model_name='product_catagory',
            name='slug',
            field=models.SlugField(max_length=60, unique=True),
        ),
    ]