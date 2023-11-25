# Generated by Django 4.2.7 on 2023-11-25 00:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_adchange_price_relation'),
    ]

    operations = [
        migrations.AddField(
            model_name='parking',
            name='location_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='api.location'),
            preserve_default=False,
        ),
    ]
