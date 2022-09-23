# Generated by Django 4.0.3 on 2022-09-15 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0018_alter_event_image_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='latitude',
            field=models.DecimalField(decimal_places=4, max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='longitude',
            field=models.DecimalField(decimal_places=4, max_digits=7, null=True),
        ),
    ]
