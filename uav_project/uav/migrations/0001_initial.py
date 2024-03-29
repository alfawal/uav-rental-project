# Generated by Django 4.2.3 on 2023-07-15 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UAVModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('brand', models.CharField(help_text='The name of the UAV (e.g. Bayraktar).', max_length=128)),
                ('model', models.CharField(help_text='The model of the UAV (e.g. TB2, Akinci, Kizilelma (MIUS), DIHA).', max_length=128)),
                ('weight', models.DecimalField(decimal_places=2, help_text='The weight of the UAV in kilograms.', max_digits=10)),
                ('category', models.CharField(help_text='The category of the UAV (e.g. Tactical, MALE, HALE).', max_length=128)),
                ('description', models.TextField(blank=True, help_text='A very detailed description of the UAV.', max_length=1024, null=True)),
                ('daily_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='uav_photos')),
                ('data', models.JSONField(blank=True, default=None, help_text='Additional properties of the UAV (e.g. speed, endurance, etc.).', null=True)),
            ],
            options={
                'verbose_name': 'Unmanned Aerial Vehicle',
                'verbose_name_plural': 'Unmanned Aerial Vehicles',
            },
        ),
    ]
