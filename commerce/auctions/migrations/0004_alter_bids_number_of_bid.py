# Generated by Django 4.2.6 on 2023-10-28 14:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0003_listing_watchlist"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bids",
            name="number_of_bid",
            field=models.IntegerField(default=0),
        ),
    ]
