# Generated by Django 4.2.1 on 2024-03-11 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('robots', '0002_robot_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='robot',
            name='slug',
            field=models.SlugField(max_length=255, unique=True),
        ),
    ]