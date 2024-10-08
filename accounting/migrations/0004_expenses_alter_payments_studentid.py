# Generated by Django 4.1 on 2024-05-30 23:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounting", "0003_payments_delete_appusers"),
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
            ],
        ),
        migrations.AlterField(
            model_name="payments",
            name="studentId",
            field=models.CharField(max_length=6),
        ),
    ]
