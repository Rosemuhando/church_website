from django.db import migrations


PASTORS = (
    {
        'slug': 'reverend-anthony',
        'name': 'Reverend Anthony',
        'title': 'Reverend',
        'biography': (
            "Pastor Anthony serves as a spiritual leader of Full Gospel "
            "Churches of Kenya - Njiru, guiding the congregation through "
            "God's Word and prayer."
        ),
        'display_order': 1,
    },
    {
        'slug': 'pastor-judy',
        'name': 'Pastor Judy',
        'title': 'Pastor',
        'biography': (
            'Pastor Judy serves alongside the church leadership, supporting '
            'the congregation and ministry with love, wisdom and dedication.'
        ),
        'display_order': 2,
    },
    {
        'slug': 'pastor-michael',
        'name': 'Pastor Michael',
        'title': 'Pastor',
        'biography': (
            "Pastor Michael is part of the church's leadership team, serving "
            'the congregation with faith and dedication.'
        ),
        'display_order': 3,
    },
)


def seed_pastors(apps, schema_editor):
    pastor_model = apps.get_model('website', 'PastorProfile')
    for pastor in PASTORS:
        pastor_model.objects.get_or_create(
            slug=pastor['slug'],
            defaults=pastor,
        )


def remove_seeded_pastors(apps, schema_editor):
    pastor_model = apps.get_model('website', 'PastorProfile')
    pastor_model.objects.filter(
        slug__in=[pastor['slug'] for pastor in PASTORS],
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_alter_galleryphoto_image_alter_pastorprofile_photo_and_more'),
    ]

    operations = [
        migrations.RunPython(seed_pastors, remove_seeded_pastors),
    ]
