# Generated by Django 5.0.3 on 2025-01-06 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('terrace_farming_app', '0002_remove_seller_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='password',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
