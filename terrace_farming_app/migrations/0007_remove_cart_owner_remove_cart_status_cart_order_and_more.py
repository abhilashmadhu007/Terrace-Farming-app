# Generated by Django 5.0.3 on 2025-01-07 16:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('terrace_farming_app', '0006_alter_product_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='status',
        ),
        migrations.AddField(
            model_name='cart',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='terrace_farming_app.orders'),
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(null=True)),
                ('status', models.CharField(max_length=100, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='terrace_farming_app.users')),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='terrace_farming_app.worker')),
            ],
        ),
    ]
