# Generated by Django 5.1.3 on 2024-11-21 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_site', '0003_alter_tour_options_alter_user_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tour',
            name='tour_type',
        ),
        migrations.AlterField(
            model_name='tour',
            name='image',
            field=models.ImageField(upload_to='static/image/img_tour'),
        ),
    ]
