# Generated by Django 3.0.3 on 2021-12-26 09:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('genedata', '0006_taxalinkprotein'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taxalinkprotein',
            name='protein_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='protein', to='genedata.Protein'),
        ),
        migrations.AlterField(
            model_name='taxalinkprotein',
            name='taxa_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='taxa', to='genedata.Taxonomy'),
        ),
    ]
