# Generated by Django 4.0.3 on 2022-07-25 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_event_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='image_file',
            field=models.FileField(blank=True, null=True, upload_to='image_files'),
        ),
    ]