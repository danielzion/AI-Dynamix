# Generated by Django 4.2.7 on 2023-11-20 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0002_room_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='description',
            field=models.TextField(default='hi'),
            preserve_default=False,
        ),
    ]
