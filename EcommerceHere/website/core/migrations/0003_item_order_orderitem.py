# Generated by Django 3.0.5 on 2020-07-09 19:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0002_auto_20200710_0030'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('itemName', models.CharField(max_length=100)),
                ('itemPrice', models.FloatField()),
                ('itemDiscountedPrice', models.FloatField(blank=True, null=True)),
                ('itemCategory', models.CharField(choices=[('cl', 'Clothing'), ('el', 'Electronics'), ('sp', 'Sports,Books & More'), ('hf', 'Home & Furniture')], max_length=2)),
                ('itemRating', models.FloatField()),
                ('itemRatingNumber', models.IntegerField()),
                ('itemSlug', models.SlugField()),
                ('itemDescription', models.TextField()),
                ('itemImage', models.ImageField(upload_to='')),
                ('itemPurchases', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Item',
                'verbose_name_plural': 'Items',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Item')),
            ],
            options={
                'verbose_name': 'OrderItem',
                'verbose_name_plural': 'OrderItems',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('ordered_date', models.DateTimeField()),
                ('ordered', models.BooleanField(default=False)),
                ('items', models.ManyToManyField(to='core.OrderItem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
        ),
    ]
