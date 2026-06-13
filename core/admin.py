from django.contrib import admin
from .models import (
    Interim,
    Leader,
    Member,
    RecruitmentApplication,
    Rule,
    TeamSettings,
)

admin.site.register(TeamSettings)
admin.site.register(Leader)
admin.site.register(Interim)
admin.site.register(Member)
admin.site.register(Rule)


@admin.register(RecruitmentApplication)
class RecruitmentApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "pseudo",
        "full_name",
        "free_fire_uid",
        "level",
        "status",
        "created_at",
        "reviewed_at",
    )
    list_filter = ("status", "level", "created_at")
    search_fields = ("pseudo", "full_name", "free_fire_uid")
