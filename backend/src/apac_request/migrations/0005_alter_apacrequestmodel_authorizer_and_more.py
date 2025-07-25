# Generated by Django 5.2.1 on 2025-06-12 18:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apac_request', '0004_alter_apacrequestmodel_options'),
        ('establishment', '0005_alter_establishmentmodel_city_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='apacrequestmodel',
            name='authorizer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='authorizer', to=settings.AUTH_USER_MODEL, verbose_name='Autorizador'),
        ),
        migrations.AlterField(
            model_name='apacrequestmodel',
            name='establishment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='establishment.establishmentmodel', verbose_name='Estabelecimento'),
        ),
        migrations.AlterField(
            model_name='apacrequestmodel',
            name='justification',
            field=models.TextField(blank=True, null=True, verbose_name='Justificativa'),
        ),
        migrations.AlterField(
            model_name='apacrequestmodel',
            name='request_date',
            field=models.DateField(auto_now_add=True, verbose_name='Data da solicitação'),
        ),
        migrations.AlterField(
            model_name='apacrequestmodel',
            name='requester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='request', to=settings.AUTH_USER_MODEL, verbose_name='Solicitante'),
        ),
        migrations.AlterField(
            model_name='apacrequestmodel',
            name='review_date',
            field=models.DateField(blank=True, null=True, verbose_name='Data da análise'),
        ),
        migrations.AlterField(
            model_name='apacrequestmodel',
            name='status',
            field=models.CharField(blank=True, choices=[('pending', 'Pendente'), ('approved', 'Aprovada'), ('rejected', 'Rejeitada')], default='pending', max_length=20, null=True, verbose_name='Status da solicitação'),
        ),
        migrations.AlterField(
            model_name='apacrequestmodel',
            name='updated_at',
            field=models.DateField(auto_now_add=True, verbose_name='Data de atualização'),
        ),
    ]
