# Generated by Django 5.0.7 on 2024-07-30 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_alter_auctionlistings_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlistings',
            name='description',
            field=models.CharField(max_length=300),
        ),
    ]
