# Generated by Django 5.1.6 on 2025-05-09 16:17
# pylint: skip-file

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("gigwork", "0005_rename_user_gig_handler_rename_user_posting_author_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="gig",
            old_name="handler",
            new_name="owner",
        ),
        migrations.RenameField(
            model_name="posting",
            old_name="author",
            new_name="owner",
        ),
    ]
