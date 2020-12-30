# Generated by Django 3.1.2 on 2020-12-30 14:56

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('indicadores', '0002_auto_20201230_1051'),
    ]

    operations = [
        migrations.CreateModel(
            name='ValoresMercadoActual',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio', models.DecimalField(decimal_places=2, max_digits=19)),
                ('tipo_mercado', models.CharField(choices=[('N', 'NACIONAL'), ('I', 'INTERNACIONAL')], db_index=True, default='N', max_length=1)),
                ('par', models.CharField(choices=[('BS/USD', 'BS/USD'), ('BS/EUR', 'BS/EUR'), ('BS/PTR', 'BS/PTR'), ('BS/BTC', 'BS/BTC'), ('USD/PTR', 'USD/PTR'), ('EUR/PTR', 'EUR/PTR'), ('USD/G', 'USD/G'), ('USD/T', 'USD/T'), ('USD/QQ', 'USD/QQ'), ('USD/L', 'USD/L'), ('USD/L', 'USD/L'), ('USD/BARRIL', 'USD/BARRIL'), ('USD/BTC', 'USD/BTC')], db_index=True, max_length=20)),
                ('fecha', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('movilidad', models.DecimalField(decimal_places=2, default=0, max_digits=19)),
                ('mercado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='indicadores.commodities')),
            ],
        ),
    ]
