from django.contrib import admin

from .models import Sermon


@admin.register(Sermon)
class SermonAdmin(admin.ModelAdmin):
    list_display = ('title', 'preacher', 'date')
    search_fields = ('title', 'preacher', 'bible_verse')
    list_filter = ('date',)
