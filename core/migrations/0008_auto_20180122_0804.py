# Generated by Django 2.0.1 on 2018-01-22 08:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0007_auto_20180111_1533'),
    ]

    operations = [
        migrations.CreateModel(
            name='adverts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('advert_status', models.CharField(choices=[('Unpaid', 'unpaid'), ('Paid', 'paid'), ('Displaying', 'displaying'), ('Completed', 'completed')], default='Unpaid', max_length=10)),
                ('max_clicks', models.IntegerField(default=10)),
                ('current_clicks', models.IntegerField(default=0)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='product_name',
            field=models.CharField(default='Rings of Bong', max_length=50),
        ),
        migrations.AddField(
            model_name='adverts',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_advert', to='core.product'),
        ),
        migrations.AddField(
            model_name='adverts',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
