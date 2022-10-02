# Generated by Django 4.1.1 on 2022-10-02 12:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import products.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('date_ordered', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Ordered', 'Ordered'), ('Shipped', 'Shipped'), ('Refunded', 'Refunded')], default='Ordered', max_length=10)),
                ('customer', models.ForeignKey(on_delete=models.SET(products.models.get_deleted_user), related_name='placed_orders', to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='products.product')),
                ('seller', models.ForeignKey(on_delete=models.SET(products.models.get_deleted_user), related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
