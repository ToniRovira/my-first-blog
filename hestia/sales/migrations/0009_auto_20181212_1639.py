# Generated by Django 2.1.3 on 2018-12-12 15:39

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0008_auto_20181212_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='peticio',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, help_text='ID únic per aquesta petició', primary_key=True, serialize=False),
        ),
    ]