# Generated by Django 4.0.3 on 2022-10-17 15:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('words', '0011_alter_linkmanager_word'),
    ]

    operations = [
        migrations.AlterField(
            model_name='linkmanager',
            name='word',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video_link',
                                    to='words.word'),
        ),
    ]
