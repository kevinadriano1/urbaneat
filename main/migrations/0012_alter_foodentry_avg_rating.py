# Generated by Django 5.1.2 on 2024-10-26 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20241026_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodentry',
            name='avg_rating',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=3),
        ),
    ]
