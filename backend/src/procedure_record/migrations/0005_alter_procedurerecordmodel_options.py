# Generated by Django 5.2.1 on 2025-06-12 18:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('procedure_record', '0004_alter_procedurerecordmodel_table'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='procedurerecordmodel',
            options={'verbose_name': 'Registro Procedimento', 'verbose_name_plural': 'Registros Procedimentos'},
        ),
    ]
