# Generated by Django 5.0.6 on 2024-05-29 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myform', '0005_purchase_is_confirmed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='confirmed',
        ),
        migrations.AlterField(
            model_name='purchase',
            name='disk_size',
            field=models.CharField(max_length=10),
        ),
    ]
