# Generated by Django 5.0.4 on 2024-04-18 11:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carapp', '0003_showroomlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='carlist',
            name='showroom',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Showroom', to='carapp.showroomlist'),
        ),
    ]
