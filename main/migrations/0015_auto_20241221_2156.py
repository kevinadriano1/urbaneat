from django.db import migrations
from django.core.management import call_command

class Migration(migrations.Migration):
    def load_updated_data(apps, schema_editor):
        call_command("loaddata", "main/fixtures/food_database.json")

    dependencies = [
        ('main', '0014_alter_foodentry_avg_rating'), 
    ]

    operations = [
        migrations.RunPython(load_updated_data),
    ]
