from django.db import migrations


VOLUNTEERING_CATEGORIES = [
    "Әлеуметтік волонтерлік",
    "Экологиялық (Эко) волонтерлік",
    "Оқиғалық (Event) волонтерлік",
    "Төтенше жағдай (ТЖ) волонтерлігі",
    "Жануарларға көмек (Зооволонтерлік)",
    "Медициналық волонтерлік",
    "Білім беру волонтерлігі",
]


def add_volunteering_categories(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        for title in VOLUNTEERING_CATEGORIES:
            cursor.execute(
                "SELECT master_id FROM organization_category_translation WHERE title = %s LIMIT 1",
                [title],
            )
            row = cursor.fetchone()

            if row:
                category_id = row[0]
            else:
                cursor.execute("INSERT INTO organization_category DEFAULT VALUES RETURNING id")
                category_id = cursor.fetchone()[0]

            for language_code in ("kk", "ru"):
                cursor.execute(
                    """
                    INSERT INTO organization_category_translation (language_code, title, master_id)
                    SELECT %s, %s, %s
                    WHERE NOT EXISTS (
                        SELECT 1
                        FROM organization_category_translation
                        WHERE master_id = %s AND language_code = %s
                    )
                    """,
                    [language_code, title, category_id, category_id, language_code],
                )


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("organization", "0005_delete_volunteerproject_and_more"),
    ]

    operations = [
        migrations.RunPython(add_volunteering_categories, noop_reverse),
    ]
