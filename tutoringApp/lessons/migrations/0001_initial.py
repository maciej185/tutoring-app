# Generated by Django 4.2.7 on 2023-12-21 10:23

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tutors', '0002_service_only_default_services_with_1_session'),
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('subject', models.CharField(max_length=250)),
                ('subject_details', models.CharField(max_length=250)),
                ('title', models.CharField(max_length=250)),
                ('status', models.IntegerField(choices=[(0, 'Have not taken place'), (1, 'Currently taking place'), (2, 'Took place already')], default=0)),
                ('absence', models.BooleanField(default=False, help_text='Indiciates whether Student showed up for the session or not.')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(0, 'Solution pending'), (1, 'Solution uploaded'), (2, 'Done'), (3, 'Solution dismissed')], default=0)),
                ('title', models.CharField(max_length=250)),
                ('description', models.TextField(max_length=1000)),
                ('due_date', models.DateTimeField()),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lessons.lesson')),
            ],
        ),
        migrations.CreateModel(
            name='Solution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('solution', models.FileField(upload_to='')),
                ('upload_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lessons.task')),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('file', models.FileField(upload_to='')),
                ('upload_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lessons.lesson')),
            ],
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_student', models.BooleanField(default=True)),
                ('text', models.TextField(max_length=1000)),
                ('publish_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lessons.lesson')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('availability', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tutors.availability')),
                ('lesson_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lessons.lesson')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.profile')),
            ],
        ),
    ]
