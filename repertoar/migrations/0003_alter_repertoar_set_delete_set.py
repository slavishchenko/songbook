# Generated by Django 4.0.4 on 2022-05-28 10:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pesmarica', '0002_alter_pesma_drugo_alter_pesma_predrefren'),
        ('repertoar', '0002_rename_pesma_repertoar_set'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repertoar',
            name='set',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='pesmarica.pesma'),
        ),
        migrations.DeleteModel(
            name='Set',
        ),
    ]
