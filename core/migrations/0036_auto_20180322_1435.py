# Generated by Django 2.0.1 on 2018-03-22 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0035_auto_20180223_2013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_name',
            field=models.CharField(default='Bit Moment', max_length=50),
        ),
        migrations.AlterField(
            model_name='product_catagory',
            name='catagory_name',
            field=models.CharField(default='Rock anne Role', max_length=50),
        ),
    ]
