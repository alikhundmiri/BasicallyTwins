# Generated by Django 2.0.1 on 2018-01-30 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_auto_20180131_0101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_name',
            field=models.CharField(default='Reavling', max_length=50),
        ),
        migrations.AlterField(
            model_name='product_catagory',
            name='catagory_name',
            field=models.CharField(default='Trackin', max_length=50),
        ),
    ]