# Generated by Django 4.2.7 on 2023-11-08 07:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import profiles.models
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('degree', models.CharField(max_length=100)),
                ('additional_info', models.CharField(help_text='GPA, awards, associations etc.', max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('profile_pic', models.ImageField(default='static/default_main_pic.jpg', upload_to=profiles.models.profile_pic_directory_path)),
                ('date_of_birth', models.DateField(default=django.utils.timezone.now)),
                ('description', models.TextField(default='')),
                ('city', models.CharField(default='', max_length=100)),
                ('teaching_since', models.DateField(blank=True, help_text="If the instance is Student's profile then this field must be Null.", null=True)),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('timestamp', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('level', models.IntegerField(choices=[(0, 'Elementary School'), (1, 'Middle School'), (2, 'High School'), (3, "Bachelor's Degree"), (4, "Master's Degree"), (5, 'PhD')], default=0)),
                ('country', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ProfileLanguageList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField(choices=[(0, 'Beginner'), (1, 'Elementary'), (2, 'Intermediate'), (3, 'Upper Intermediate'), (4, 'Advanced'), (5, 'Native')], default=0)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.language')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.profile')),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='languages',
            field=models.ManyToManyField(through='profiles.ProfileLanguageList', to='profiles.language'),
        ),
        migrations.AddField(
            model_name='profile',
            name='schools',
            field=models.ManyToManyField(through='profiles.Education', to='profiles.school'),
        ),
        migrations.CreateModel(
            name='HistoricalProfile',
            fields=[
                ('profile_pic', models.TextField(default='static/default_main_pic.jpg', max_length=100)),
                ('date_of_birth', models.DateField(default=django.utils.timezone.now)),
                ('description', models.TextField(default='')),
                ('city', models.CharField(default='', max_length=100)),
                ('teaching_since', models.DateField(blank=True, help_text="If the instance is Student's profile then this field must be Null.", null=True)),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('timestamp', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical profile',
                'verbose_name_plural': 'historical profiles',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.AddField(
            model_name='education',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.profile'),
        ),
        migrations.AddField(
            model_name='education',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.school'),
        ),
    ]