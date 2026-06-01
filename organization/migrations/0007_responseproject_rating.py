from django.db import migrations, models


def recalculate_existing_user_ratings(apps, schema_editor):
    ResponseProject = apps.get_model("organization", "ResponseProject")
    CustomUser = apps.get_model("account", "CustomUser")

    for user in CustomUser.objects.all():
        total = 0
        for response in ResponseProject.objects.filter(user_id=user.id):
            total += response.rating
        CustomUser.objects.filter(id=user.id).update(rating=total)


class Migration(migrations.Migration):

    dependencies = [
        ("organization", "0006_add_volunteering_categories"),
    ]

    operations = [
        migrations.AddField(
            model_name="responseproject",
            name="rating",
            field=models.IntegerField(default=0),
        ),
        migrations.RunPython(recalculate_existing_user_ratings, migrations.RunPython.noop),
    ]
