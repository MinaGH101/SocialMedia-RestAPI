# Generated by Django 4.1.2 on 2023-02-07 07:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(model_name="mymodel", old_name="name", new_name="esm",),
    ]
