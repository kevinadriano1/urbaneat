from django.db import migrations
from django.core.management import call_command


class Migration(migrations.Migration):
    def load_my_initial_data(apps, schema_editor):
        call_command("loaddata", "main/fixtures/food_database.json")

    dependencies = [
        ('main', '0010_alter_foodentry_number_of_reviews'),
    ]

    operations = [
        migrations.RunPython(load_my_initial_data),
    ]
