# Generated by Django 2.0.1 on 2018-02-02 14:21

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_auto_20180202_1950'),
    ]

    operations = [
        migrations.AddField(
            model_name='anon_user_detail',
            name='new_string_uuid',
            field=models.CharField(default=uuid.uuid4, max_length=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_name',
            field=models.CharField(default='Rings of Bong', max_length=50),
        ),
        migrations.AlterField(
            model_name='product_catagory',
            name='catagory_name',
            field=models.CharField(default='Cube box', max_length=50),
        ),
    ]