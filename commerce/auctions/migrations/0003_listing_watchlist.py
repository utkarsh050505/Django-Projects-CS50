# Generated by Django 4.2.6 on 2023-10-10 10:27

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0002_bids"),
    ]

    operations = [
        migrations.AddField(
            model_name="listing",
            name="watchlist",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="watch_list",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
