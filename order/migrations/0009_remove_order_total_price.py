# Generated by Django 5.1.5 on 2025-01-19 22:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0008_remove_order_items_order_items'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='total_price',
        ),
    ]
