# Generated by Django 5.1.1 on 2024-10-26 21:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('country', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Athlete_Bio',
            fields=[
                ('athlete_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('sex', models.CharField(max_length=10)),
                ('born', models.TextField()),
                ('height', models.FloatField()),
                ('weight', models.FloatField()),
                ('description', models.TextField()),
                ('special_notes', models.TextField()),
                ('country', models.TextField(default='Unknown')),
                ('country_noc', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='country.country')),
            ],
        ),
    ]