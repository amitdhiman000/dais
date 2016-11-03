# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-01 17:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('edited_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('approved', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=100)),
                ('sub_title', models.CharField(max_length=200)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Author')),
            ],
            options={
                'verbose_name': 'post',
                'verbose_name_plural': 'posts',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('edited_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('approved', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Author')),
                ('reply_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Comment')),
            ],
            options={
                'verbose_name': 'post',
                'verbose_name_plural': 'posts',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Topics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic_name', models.CharField(max_length=50)),
                ('topic_desc', models.CharField(blank=True, max_length=100)),
            ],
        ),
    ]