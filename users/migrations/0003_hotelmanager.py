# Generated by Django 4.0 on 2022-01-03 20:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('city', '0003_alter_city_slug'),
        ('users', '0002_rename_is_hotel_manger_user_is_hotel_manager'),
    ]

    operations = [
        migrations.CreateModel(
            name='HotelManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='managers', to='city.city')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='hotel_manager', to='users.user')),
            ],
        ),
    ]
