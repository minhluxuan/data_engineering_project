# Generated by Django 5.1.1 on 2024-11-09 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='result_description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='result',
            name='result_detail',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='result',
            name='result_format',
            field=models.TextField(null=True),
        ),
    ]
