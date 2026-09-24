from django.contrib.auth.hashers import make_password
from django.db import migrations


def create_admin(apps, schema_editor):
    apps.get_model('api', 'User').objects.create(
        email='admin@shop.com', password=make_password('shop2015'), is_staff=True, is_superuser=True
    )


class Migration(migrations.Migration):
    dependencies = [('api', '0001_initial')]
    operations = [migrations.RunPython(create_admin)]
