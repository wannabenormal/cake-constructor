# Generated by Django 4.0.4 on 2022-05-02 03:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cakeshop', '0005_alter_order_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='referral',
        ),
        migrations.AddField(
            model_name='order',
            name='referral',
            field=models.ForeignKey(blank=True, max_length=255, null=True, on_delete=django.db.models.deletion.CASCADE, to='cakeshop.advertisement', verbose_name='Реклама'),
        ),
    ]
