# Generated by Django 2.0.6 on 2018-06-08 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CDO', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permission',
            field=models.IntegerField(default=2),
        ),
        migrations.AddField(
            model_name='user',
            name='user_surname',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]