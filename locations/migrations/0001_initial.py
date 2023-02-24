# Generated by Django 4.0 on 2023-02-09 10:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gate_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Terminal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('terminal_name', models.CharField(max_length=50)),
                ('iata_code', models.CharField(default='unset', max_length=10)),
                ('icao_code', models.CharField(default='unset', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Stand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stand_name', models.CharField(max_length=50)),
                ('gate_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locations.gate')),
            ],
        ),
        migrations.CreateModel(
            name='Pbb',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pbb_name', models.CharField(max_length=50)),
                ('stand_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locations.stand')),
            ],
        ),
        migrations.AddField(
            model_name='gate',
            name='terminal_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locations.terminal'),
        ),
    ]
