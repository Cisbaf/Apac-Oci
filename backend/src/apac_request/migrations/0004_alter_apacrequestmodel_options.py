# Generated by Django 5.2.1 on 2025-06-12 18:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apac_request', '0003_alter_apacrequestmodel_table'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='apacrequestmodel',
            options={'verbose_name': 'Solicitação Apac', 'verbose_name_plural': 'Solicitações Apac'},
        ),
    ]
