# Generated by Django 5.0.7 on 2024-07-30 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auctionlistings_bid_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlistings',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
