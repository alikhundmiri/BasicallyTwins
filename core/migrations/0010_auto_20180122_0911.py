# Generated by Django 2.0.1 on 2018-01-22 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20180122_0816'),
    ]

    operations = [
        migrations.RenameField(
            model_name='adverts',
            old_name='product',
            new_name='customer',
        ),
        migrations.AlterField(
            model_name='product',
            name='product_name',
            field=models.CharField(default='Vortex Ship', max_length=50),
        ),
    ]