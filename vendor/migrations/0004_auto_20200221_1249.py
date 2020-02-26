# Generated by Django 3.0.3 on 2020-02-21 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0003_auto_20200218_1707'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendor',
            name='address',
        ),
        migrations.AddField(
            model_name='location',
            name='street_address',
            field=models.CharField(default='default street address', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='location',
            name='city',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]