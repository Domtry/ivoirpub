# Generated by Django 3.0.3 on 2020-04-25 10:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=120)),
                ('email', models.EmailField(max_length=150, unique=True)),
                ('password', models.CharField(max_length=120)),
                ('create_date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Campagne',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80)),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
                ('state', models.BooleanField(default=False)),
                ('start_date', models.DateField()),
                ('close_date', models.DateField()),
                ('create_date', models.DateField(auto_now_add=True)),
                ('modify', models.DateField(auto_now_add=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Account')),
            ],
        ),
        migrations.CreateModel(
            name='FacebookUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=20, unique=True)),
                ('access_token', models.CharField(max_length=1000)),
                ('expires_in', models.IntegerField()),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80)),
                ('message', models.TextField(blank=True, max_length=500, null=True)),
                ('poste_date', models.DateField()),
                ('poste_heure', models.TimeField()),
                ('data_file', models.FileField(blank=True, null=True, upload_to='uploads')),
                ('is_publish', models.BooleanField(default=False)),
                ('used_file', models.BooleanField(default=False)),
                ('pages_posted', models.CharField(blank=True, max_length=150, null=True)),
                ('campagne', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Campagne')),
            ],
        ),
        migrations.CreateModel(
            name='FPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_id', models.CharField(max_length=20, unique=True)),
                ('access_token', models.TextField(max_length=1000)),
                ('name', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=70)),
                ('expires_in', models.IntegerField()),
                ('fb_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.FacebookUser')),
            ],
        ),
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aut_generate', models.BooleanField(default=True)),
                ('default_page', models.CharField(max_length=30)),
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Account')),
            ],
        ),
    ]
