# Generated by Django 4.0.3 on 2022-12-24 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0019_event_country_event_social_media_links'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='timezone',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]