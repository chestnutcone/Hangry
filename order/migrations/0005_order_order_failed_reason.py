# Generated by Django 3.0.3 on 2020-02-24 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_auto_20200221_0041'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_failed_reason',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
