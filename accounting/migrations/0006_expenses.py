# Generated by Django 4.1 on 2024-05-31 00:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounting", "0005_delete_expenses"),
    ]

    operations = [
        migrations.CreateModel(
            name="Expenses",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField()),
                ("fuel", models.FloatField()),
                ("stationery", models.FloatField()),
                ("bills", models.FloatField()),
                ("salaries", models.FloatField()),
            ],
        ),
    ]
