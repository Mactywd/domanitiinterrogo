# Generated by Django 4.2.5 on 2023-11-01 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interrogazioni', '0003_materia_url_name_alter_lastinterrogation_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='lastinterrogation',
            name='color',
            field=models.CharField(default='red', max_length=50),
        ),
        migrations.AddField(
            model_name='lastinterrogation',
            name='formatted_date',
            field=models.CharField(default='mai', max_length=50),
        ),
    ]
