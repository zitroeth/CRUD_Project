# Generated by Django 5.0.6 on 2024-05-13 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0002_sentimentanalysis'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sentimentanalysis',
            name='negative',
        ),
        migrations.RemoveField(
            model_name='sentimentanalysis',
            name='positive',
        ),
        migrations.AddField(
            model_name='sentimentanalysis',
            name='score',
            field=models.DecimalField(decimal_places=3, default=0.0, editable=False, max_digits=4),
        ),
        migrations.AddField(
            model_name='sentimentanalysis',
            name='sentiment',
            field=models.CharField(default='', max_length=10),
        ),
    ]
