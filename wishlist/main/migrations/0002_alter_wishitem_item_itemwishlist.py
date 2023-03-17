# Generated by Django 4.1.7 on 2023-03-16 18:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="wishitem",
            name="item",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="wishlists",
                to="main.item",
                unique=True,
            ),
        ),
        migrations.CreateModel(
            name="ItemWishList",
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
                ("name", models.CharField(max_length=255)),
                (
                    "items",
                    models.ManyToManyField(related_name="wish_lists", to="main.item"),
                ),
            ],
        ),
    ]
