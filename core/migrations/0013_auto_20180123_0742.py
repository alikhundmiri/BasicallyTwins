# Generated by Django 2.0.1 on 2018-01-23 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20180123_0633'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_pitch',
            field=models.TextField(blank=True, default='Our revolutionary product will change the world', max_length=280, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_name',
            field=models.CharField(default='BlueSkin', max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='twin',
            field=models.ManyToManyField(blank=True, to='core.product'),
        ),
    ]
