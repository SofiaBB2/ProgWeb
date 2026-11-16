from django.db import migrations, models
import django.db.models.deletion


def associar_residuos_existentes(apps, schema_editor):
    ArmazenamentoResiduo = apps.get_model('tasks', 'Armazenamento_Residuo')
    Residuo = apps.get_model('tasks', 'Residuo')

    for armazenamento in ArmazenamentoResiduo.objects.select_related(
        'id_gerado__id_residuo'
    ).iterator():
        Residuo.objects.filter(
            pk=armazenamento.id_gerado.id_residuo_id,
            criado_por__isnull=True,
        ).update(criado_por_id=armazenamento.id_usuario_id)


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='residuo',
            name='criado_por',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='residuos_criados',
                to='tasks.usuario',
            ),
        ),
        migrations.RunPython(
            associar_residuos_existentes,
            migrations.RunPython.noop,
        ),
    ]