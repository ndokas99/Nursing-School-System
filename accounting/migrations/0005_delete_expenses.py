# Generated by Django 4.1 on 2024-05-31 00:19

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("accounting", "0004_expenses_alter_payments_studentid"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Expenses",
        ),
    ]
