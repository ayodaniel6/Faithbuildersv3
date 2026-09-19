from django.contrib import admin

from .models import (
    SiteSettings,
    AboutPage,
    EmpowermentProgram,
    ContactMessage,
    TeamMember,
)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = (
        "site_name",
        "email",
        "phone",
    )

    def has_add_permission(self, request):
        if SiteSettings.objects.exists():
            return False

        return True


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "role",
        "is_active",
        "display_order",
    )

    list_filter = (
        "role",
        "is_active",
    )

    search_fields = (
        "name",
        "role",
    )

    ordering = (
        "display_order",
    )


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = (
        "heading",
    )

    def has_add_permission(self, request):
        if AboutPage.objects.exists():
            return False

        return True


@admin.register(EmpowermentProgram)
class EmpowermentProgramAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "is_active",
        "display_order",
    )

    list_filter = (
        "is_active",
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "subject",
        "created_at",
    )

    search_fields = (
        "name",
        "email",
        "subject",
    )

    readonly_fields = (
        "created_at",
    )