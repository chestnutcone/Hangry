# Generated by Django 3.0.3 on 2020-02-21 03:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_remove_order_group'),
        ('user', '0003_auto_20200220_1932'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.Team'),
        ),
    ]
