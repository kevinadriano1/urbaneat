# Generated by Django 5.1.1 on 2024-10-26 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_remove_foodentry_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodentry',
            name='avg_rating',
            field=models.FloatField(default=0.0),
        ),
    ]