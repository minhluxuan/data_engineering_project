# Generated by Django 5.1.1 on 2024-09-21 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("country", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="game",
            name="competition_end_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="game",
            name="competition_start_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="game",
            name="end_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="game",
            name="start_date",
            field=models.DateField(blank=True, null=True),
        ),
    ]