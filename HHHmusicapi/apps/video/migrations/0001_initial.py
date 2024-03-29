# Generated by Django 2.2.3 on 2019-07-30 10:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_show', models.BooleanField(default=True, verbose_name='是否上架')),
                ('is_delete', models.BooleanField(default=False, verbose_name='逻辑删除')),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('name', models.CharField(max_length=256, verbose_name='名称')),
            ],
            options={
                'verbose_name': 'MV_tag',
                'verbose_name_plural': 'MV_tag',
                'db_table': 'video_video_tag',
            },
        ),
        migrations.CreateModel(
            name='MusicVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_show', models.BooleanField(default=True, verbose_name='是否上架')),
                ('is_delete', models.BooleanField(default=False, verbose_name='逻辑删除')),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('title', models.CharField(max_length=256, verbose_name='标题')),
                ('video_img', models.ImageField(blank=True, default='/video_img/20161202101543717.jpg', help_text='头像图片的大小规格：256x256，或者对应的比例的图片', null=True, upload_to='video_img/', verbose_name='mv图片')),
                ('length', models.CharField(max_length=32, verbose_name='时长')),
                ('video_id', models.CharField(max_length=256, verbose_name='video外链id')),
                ('video_resolution', models.SmallIntegerField(choices=[(0, '高清'), (1, '超清'), (2, '1080P')], default=0, verbose_name='高清')),
                ('artist', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='videos', to=settings.AUTH_USER_MODEL, verbose_name='歌手')),
                ('video_tag', models.ForeignKey(max_length=256, on_delete=django.db.models.deletion.DO_NOTHING, to='video.VideoTag', verbose_name='video标签')),
            ],
            options={
                'verbose_name': 'MV',
                'verbose_name_plural': 'MV',
                'db_table': 'video_videos',
            },
        ),
    ]
