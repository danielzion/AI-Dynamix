# Generated by Django 4.2.7 on 2023-11-20 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_openaicommand_response'),
    ]

    operations = [
        migrations.AlterField(
            model_name='openaicommand',
            name='response',
            field=models.TextField(default='hi'),
            preserve_default=False,
        ),
    ]
