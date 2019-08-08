# Generated by Django 2.2.3 on 2019-07-30 10:43

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('mobile', models.CharField(max_length=15, unique=True, verbose_name='手机号码')),
                ('avatar', models.ImageField(blank=True, default='/avatar/20190728153034.jpg', help_text='头像图片的大小规格：256x256，或者对应的比例的图片', null=True, upload_to='avatar', verbose_name='用户头像')),
                ('follows_count', models.IntegerField(default=0)),
                ('fans_count', models.IntegerField(default=0)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
                'db_table': 'music_user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_show', models.BooleanField(default=True, verbose_name='是否上架')),
                ('is_delete', models.BooleanField(default=False, verbose_name='逻辑删除')),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('followed_artist', models.ForeignKey(blank=True, db_constraint=False, max_length=256, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='followed_artist', to=settings.AUTH_USER_MODEL, verbose_name='关注歌手')),
                ('followed_user', models.ForeignKey(blank=True, db_constraint=False, max_length=256, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='followed', to=settings.AUTH_USER_MODEL, verbose_name='关注的人')),
                ('user', models.ForeignKey(blank=True, db_constraint=False, max_length=256, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='userfollow', to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Fan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_show', models.BooleanField(default=True, verbose_name='是否上架')),
                ('is_delete', models.BooleanField(default=False, verbose_name='逻辑删除')),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('fans', models.ForeignKey(blank=True, db_constraint=False, max_length=256, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='fan', to=settings.AUTH_USER_MODEL, verbose_name='粉丝')),
                ('user', models.ForeignKey(blank=True, db_constraint=False, max_length=256, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='userfan', to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
