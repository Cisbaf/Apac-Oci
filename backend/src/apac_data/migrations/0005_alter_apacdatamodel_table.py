# Generated by Django 5.2.1 on 2025-06-11 16:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apac_data', '0004_rename_mediccbo_apacdatamodel_medic_cbo_and_more'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='apacdatamodel',
            table='dados_apac',
        ),
    ]
