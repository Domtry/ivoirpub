# Generated by Django 3.0.3 on 2020-07-07 00:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_post_fb_post_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='username',
        ),
    ]