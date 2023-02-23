from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', ''),
    ]

    operations = [
        migrations.UpdateField(
            model_name='customuser',
            name='email',
            field=models.BooleanField(default=False),
        ),
    ]