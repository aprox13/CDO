# Generated by Django 2.0.6 on 2018-06-08 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_login', models.CharField(max_length=40)),
                ('user_password', models.CharField(max_length=100)),
            ],
            options={
                'managed': True,
            },
        ),
    ]
