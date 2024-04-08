# Generated by Django 5.0.4 on 2024-04-08 21:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(upload_to='uploads/')),
                ('username', models.CharField(max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following_set', to='main_app.profile')),
                ('following', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower_set', to='main_app.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Run',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distance', models.IntegerField()),
                ('starttime', models.DateTimeField()),
                ('endtime', models.DateTimeField()),
                ('timetotal', models.DateTimeField()),
                ('likes', models.ManyToManyField(related_name='liked_runs', through='main_app.Like', to='main_app.profile')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='runs', to='main_app.profile')),
            ],
        ),
        migrations.AddField(
            model_name='like',
            name='run',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.run'),
        ),
        migrations.CreateModel(
            name='Geolocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.CharField(max_length=200)),
                ('longitude', models.CharField(max_length=200)),
                ('elevation', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('run', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.run')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=50)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.profile')),
                ('run', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.run')),
            ],
        ),
    ]
