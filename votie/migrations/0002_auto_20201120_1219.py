# Generated by Django 2.2.7 on 2020-11-20 08:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('votie', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='choice',
            old_name='choie_image',
            new_name='choice_image',
        ),
        migrations.AlterField(
            model_name='candidate',
            name='image',
            field=models.ImageField(blank=True, default='default-avatar.png', null=True, upload_to='user/'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_voter',
            field=models.BooleanField(default=True, verbose_name='voter'),
        ),
        migrations.CreateModel(
            name='Voter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
