# Generated by Django 4.0.4 on 2022-06-03 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pesmarica', '0004_remove_pesma_za_pocetnike_pesma_tezina'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pesma',
            name='tezina',
        ),
        migrations.AddField(
            model_name='pesma',
            name='za_pocetnike',
            field=models.BooleanField(default=False),
        ),
    ]
