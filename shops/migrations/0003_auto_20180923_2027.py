# Generated by Django 2.1.1 on 2018-09-23 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0002_auto_20180923_0425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_num',
            field=models.CharField(default='1537-734435-6337', max_length=16),
        ),
    ]
