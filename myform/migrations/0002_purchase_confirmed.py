# Generated by Django 5.0.6 on 2024-05-26 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myform', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='confirmed',
            field=models.BooleanField(default=False),
        ),
    ]
