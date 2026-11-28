# Adds the "DST INSPIRE Fellow" and "Ramanujan Fellow" faculty designations.
#
# Choices are not stored in the database, so this migration only updates
# Django's model state. On SQLite a plain AlterField would rebuild the whole
# mechweb_facultypage table; SeparateDatabaseAndState with no database
# operations avoids touching the live schema at all.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mechweb', '0153_auto_20250509_0531'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterField(
                    model_name='facultypage',
                    name='designation',
                    field=models.CharField(choices=[('0', 'HAG'), ('1', 'Professor'), ('3', 'Associate Professor'), ('2', 'Assistant Professor'), ('4', 'Visiting Professor'), ('5', 'Honorary Professor'), ('6', 'DST INSPIRE Fellow'), ('7', 'Ramanujan Fellow')], default='3', max_length=2),
                ),
            ],
            database_operations=[],
        ),
    ]
