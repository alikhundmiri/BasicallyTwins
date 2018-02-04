# Generated by Django 2.0.1 on 2018-01-30 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_auto_20180129_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_name',
            field=models.CharField(default='Wild flips', max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='revenue_info_source',
            field=models.CharField(choices=[('from the Internet, unverified.', 'internet, unverified'), ('from the Internet, Admin Verified.', 'internet, admin verified'), ('verified by the Maker.', 'maker verified'), ('not for Public Viewing', 'Not for public viewing')], default='from the Internet, unverified.', max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='website',
            field=models.URLField(help_text='Your Landing page URL. When you choose to advert, your advert will divert to this URL.', max_length=1000),
        ),
        migrations.AlterField(
            model_name='product_catagory',
            name='catagory_name',
            field=models.CharField(default='Thin Gap', max_length=50),
        ),
        migrations.AlterField(
            model_name='revenue_source',
            name='source',
            field=models.CharField(choices=[('------', '------'), ('Advertisments', 'Ads'), ('Subscription', 'subscription'), ('One time Payment', 'entry fees'), ('eCommence', 'eCommence'), ('Service sales', 'service sales'), ('Digital Product sales', 'digital product sales'), ('Digital Service sales', 'digital service sales'), ('Affiliate Marketing', 'Affiliate Marketing')], default='------', max_length=50),
        ),
    ]
