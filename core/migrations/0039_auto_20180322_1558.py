# Generated by Django 2.0.1 on 2018-03-22 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0038_auto_20180322_1446'),
    ]

    operations = [
        migrations.AddField(
            model_name='list_items',
            name='public_view',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='list_items',
            name='suitable_for',
            field=models.CharField(choices=[('Painter', 'Painter'), ('Writers', 'Writers'), ('Educator', 'Educator'), ('Programmer', 'Programmer'), ('Music Creator', 'Music Creator'), ('Video Creator', 'Video Creator'), ('Internet Entrepreneur', 'internet Entrepreneur')], default='Painter', max_length=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_name',
            field=models.CharField(default='Phone Smith', max_length=50),
        ),
        migrations.AlterField(
            model_name='product_catagory',
            name='catagory_name',
            field=models.CharField(default='Measurant', max_length=50),
        ),
    ]