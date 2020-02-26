# Generated by Django 3.0.3 on 2020-02-21 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_order_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='notes',
            field=models.CharField(default='', max_length=300),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='ordered',
            field=models.BooleanField(default=False),
        ),
    ]