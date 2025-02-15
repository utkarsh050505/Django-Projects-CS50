# Generated by Django 4.2.6 on 2023-11-18 09:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0006_bids_highest_bid_bids_number_of_bid"),
    ]

    operations = [
        migrations.AddField(
            model_name="listing",
            name="winner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="winner",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
