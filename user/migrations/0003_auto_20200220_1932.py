# Generated by Django 3.0.3 on 2020-02-21 03:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0003_auto_20200218_1707'),
        ('order', '0002_remove_order_group'),
        ('user', '0002_group_vendors'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='group',
        ),
        migrations.DeleteModel(
            name='Group',
        ),
        migrations.AddField(
            model_name='team',
            name='executor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='team_executor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='team',
            name='vendors',
            field=models.ManyToManyField(to='vendor.Vendor'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.Team'),
        ),
    ]
