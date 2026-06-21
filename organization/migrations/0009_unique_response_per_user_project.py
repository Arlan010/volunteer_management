from django.db import migrations, models
from django.db.models import Count, Sum


def deduplicate_responses(apps, schema_editor):
    ResponseProject = apps.get_model('organization', 'ResponseProject')
    CustomUser = apps.get_model('account', 'CustomUser')

    duplicate_groups = (
        ResponseProject.objects.values('user_id', 'project_id')
        .annotate(total=Count('id'))
        .filter(total__gt=1)
    )

    for group in duplicate_groups:
        responses = list(
            ResponseProject.objects.filter(
                user_id=group['user_id'],
                project_id=group['project_id'],
            ).order_by('-id')
        )
        keeper = next(
            (
                response
                for response in responses
                if response.rating != 0 or response.attendance_status != 'pending'
            ),
            responses[0],
        )
        ResponseProject.objects.filter(
            user_id=group['user_id'],
            project_id=group['project_id'],
        ).exclude(id=keeper.id).delete()

    CustomUser.objects.update(rating=0)

    user_totals = (
        ResponseProject.objects.values('user_id')
        .annotate(total_rating=Sum('rating'))
    )
    for user_total in user_totals:
        CustomUser.objects.filter(id=user_total['user_id']).update(
            rating=user_total['total_rating'] or 0
        )


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0008_responseproject_attendance_status'),
    ]

    operations = [
        migrations.RunPython(deduplicate_responses, migrations.RunPython.noop),
        migrations.AddConstraint(
            model_name='responseproject',
            constraint=models.UniqueConstraint(
                fields=('user', 'project'),
                name='unique_response_per_user_project',
            ),
        ),
    ]
