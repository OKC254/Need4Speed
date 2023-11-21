# Generated by Django 4.2.7 on 2023-11-19 10:52

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VideoUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('videofile', cloudinary.models.CloudinaryField(max_length=255, verbose_name='videos')),
                ('speedlimit', models.IntegerField(max_length=20)),
            ],
        ),
    ]