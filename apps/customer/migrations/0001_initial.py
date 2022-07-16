# Generated by Django 4.0 on 2022-07-16 12:04

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('brand', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerGoal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('selected_amount', models.IntegerField(choices=[(1, 9), (2, 19), (3, 29), (4, 39), (5, 49), (6, 59)], default=1)),
                ('selected_tenure', models.IntegerField(choices=[(1, 1), (2, 3), (3, 6), (4, 9), (5, 12), (6, 18)], default=1)),
                ('benefit_type', models.IntegerField(choices=[(1, 'CASHBACK'), (2, 'EXTRA_CASHBACK'), (3, 'WALLET_POINT')], default=1)),
                ('benefit_percentage', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)])),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('deposit_amount', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(1000000), django.core.validators.MinValueValidator(0)])),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='brand.plan')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='goals', to='auth.user')),
            ],
            options={
                'db_table': 'customer_goals',
            },
        ),
    ]
