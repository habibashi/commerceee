# Generated by Django 2.2.12 on 2022-07-29 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0021_auto_20220728_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='winner',
            field=models.CharField(max_length=40, null=True),
        ),
    ]
