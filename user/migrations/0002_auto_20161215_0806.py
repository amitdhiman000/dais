# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-15 08:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='author',
        ),
        migrations.RemoveField(
            model_name='articlecomment',
            name='article',
        ),
        migrations.RemoveField(
            model_name='articlecomment',
            name='author',
        ),
        migrations.RemoveField(
            model_name='articlereaction',
            name='article',
        ),
        migrations.RemoveField(
            model_name='articlereaction',
            name='user',
        ),
        migrations.RemoveField(
            model_name='commentreaction',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='commentreaction',
            name='user',
        ),
        migrations.RemoveField(
            model_name='replycomment',
            name='author',
        ),
        migrations.RemoveField(
            model_name='replycomment',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='replycommentreaction',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='replycommentreaction',
            name='user',
        ),
        migrations.RemoveField(
            model_name='topic',
            name='topic_author',
        ),
        migrations.RemoveField(
            model_name='topicfollower',
            name='topic',
        ),
        migrations.RemoveField(
            model_name='topicfollower',
            name='user',
        ),
        migrations.DeleteModel(
            name='Article',
        ),
        migrations.DeleteModel(
            name='ArticleComment',
        ),
        migrations.DeleteModel(
            name='ArticleReaction',
        ),
        migrations.DeleteModel(
            name='CommentReaction',
        ),
        migrations.DeleteModel(
            name='ReplyComment',
        ),
        migrations.DeleteModel(
            name='ReplyCommentReaction',
        ),
        migrations.DeleteModel(
            name='Topic',
        ),
        migrations.DeleteModel(
            name='TopicFollower',
        ),
    ]
