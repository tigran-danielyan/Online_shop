# Generated by Django 2.2.8 on 2020-05-22 12:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_orderitem_quantity'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='orderd',
            new_name='ordered',
        ),
    ]
