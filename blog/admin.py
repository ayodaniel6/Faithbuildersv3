from django.contrib import admin

from .models import (
    Category,
    Series,
    Post,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "created_at",
    )

    search_fields = (
        "name",
    )



@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "created_at",
        "slug",
    )

    search_fields = (
        "title",
        "description",
    )

    prepopulated_fields = {
        "slug": ("title",)
    }



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "status",
        "is_featured",
        "published_date",
        "created_at",
        "author",
        "series",
        "series_order",
    )

    list_filter = (
        "status",
        "is_featured",
        "categories",
        "created_at",
        "series",
    )

    search_fields = (
        "title",
        "body",
        "seo_description",
    )

    ordering = (
        "-created_at",
    )

    # prepopulated_fields = {
    #     "slug": ("title",)
    # }

    readonly_fields = (
        "slug",
        "created_at",
        "updated_at",
    )

    fieldsets = (

        (
            "Article Information",
            {
                "fields": (
                    "title",
                    "slug",
                    "excerpt",
                    "youtube_url",
                    "body",
                    "featured_image",
                )
            }
        ),

        (
            "Organization",
            {
                "fields": (
                    "categories",
                    "series",
                    "series_order",
                    "author",
                )
            }
        ),

        (
            "Publishing",
            {
                "fields": (
                    "status",
                    "published_date",
                    "is_featured",
                    "featured_order",
                )
            }
        ),

        (
            "SEO",
            {
                "fields": (
                    "seo_title",
                    "seo_description",
                )
            }
        ),

    )