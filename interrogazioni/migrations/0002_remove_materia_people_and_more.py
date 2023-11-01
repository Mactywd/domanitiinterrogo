# Generated by Django 4.2.5 on 2023-11-01 18:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('interrogazioni', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='materia',
            name='people',
        ),
        migrations.RemoveField(
            model_name='persona',
            name='last_interrogation',
        ),
        migrations.CreateModel(
            name='LastInterrogation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='interrogazioni.persona')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='interrogazioni.materia')),
            ],
        ),
    ]