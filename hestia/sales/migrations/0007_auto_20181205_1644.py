# Generated by Django 2.1.3 on 2018-12-05 15:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sales', '0006_auto_20181205_1204'),
    ]

    operations = [
        migrations.CreateModel(
            name='Concesio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_concesio', models.DateTimeField(blank=True)),
                ('concesionari', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['data_concesio'],
            },
        ),
        migrations.AddField(
            model_name='peticio',
            name='motiu',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='peticio',
            name='status',
            field=models.CharField(choices=[('t', 'Taller'), ('a', 'Auditori'), ('r', 'Reunió')], default='r', help_text='Disposició de la sala', max_length=1),
        ),
        migrations.AddField(
            model_name='concesio',
            name='peticio_servida',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sales.Peticio'),
        ),
        migrations.AddField(
            model_name='concesio',
            name='sala_donada',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sales.Sala'),
        ),
    ]