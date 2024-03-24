# Generated by Django 4.2.1 on 2024-03-24 11:16

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('robots', '0007_tagpost_alter_robot_cat_robot_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads_model')),
            ],
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='robot',
            options={'ordering': ['-time_create'], 'verbose_name': 'Робот', 'verbose_name_plural': 'Роботы'},
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(db_index=True, max_length=100, verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='robot',
            name='cat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='posts', to='robots.category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='robot',
            name='content',
            field=models.TextField(blank=True, verbose_name='Статья'),
        ),
        migrations.AlterField(
            model_name='robot',
            name='is_published',
            field=models.BooleanField(choices=[(False, 'Черновик'), (True, 'Опубликовано')], default=1, verbose_name='Публикация'),
        ),
        migrations.AlterField(
            model_name='robot',
            name='slug',
            field=models.SlugField(max_length=255, unique=True, validators=[django.core.validators.MinLengthValidator(5, message='Минимум 5 символов'), django.core.validators.MaxLengthValidator(100, message='Максимум 100 символов')], verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='robot',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='tags', to='robots.tagpost', verbose_name='Тэги'),
        ),
        migrations.AlterField(
            model_name='robot',
            name='time_create',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='robot',
            name='time_update',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата изменения'),
        ),
        migrations.AlterField(
            model_name='robot',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Заголовок'),
        ),
        migrations.AddIndex(
            model_name='robot',
            index=models.Index(fields=['-time_create'], name='robots_robo_time_cr_67e8c9_idx'),
        ),
    ]