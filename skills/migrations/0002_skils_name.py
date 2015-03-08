# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('skills', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='skils',
            name='name',
            field=models.CharField(default=189, max_length=300),
            preserve_default=False,
        ),
    ]
