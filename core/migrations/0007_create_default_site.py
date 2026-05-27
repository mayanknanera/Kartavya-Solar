from django.db import migrations


def create_default_site(apps, schema_editor):
    Site = apps.get_model("sites", "Site")
    Site.objects.get_or_create(
        id=1,
        defaults={
            "domain": "127.0.0.1:8000",
            "name": "localhost",
        },
    )


def delete_default_site(apps, schema_editor):
    Site = apps.get_model("sites", "Site")
    Site.objects.filter(id=1, domain="127.0.0.1:8000").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0006_alter_product_category"),
        ("sites", "0002_alter_domain_unique"),
    ]

    operations = [
        migrations.RunPython(create_default_site, delete_default_site),
    ]
