# Generated by Django 5.1.2 on 2024-11-03 03:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0003_rename_message_messages_rename_topic_topics'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messages',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='my_app.room'),
        ),
    ]
