from django.db import models
from django.utils.text import slugify


class TimeStampedModel(models.Model):

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )


    class Meta:
        abstract = True



class Category(TimeStampedModel):

    name = models.CharField(
        max_length=100
    )

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name




class Series(TimeStampedModel):

    title = models.CharField(
        max_length=200
    )

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    image = models.ImageField(
        upload_to="series/",
        blank=True
    )

    class Meta:
        verbose_name = "Series"
        verbose_name_plural = "Series"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)


    def __str__(self):
        return self.title



class Post(TimeStampedModel):

    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
    )


    title = models.CharField(
        max_length=200
    )

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    excerpt = models.TextField(
        blank=True
    )

    body = models.TextField()


    featured_image = models.ImageField(
        upload_to="posts/",
        blank=True
    )


    categories = models.ManyToManyField(
    Category,
    related_name="posts"
    )


    series = models.ForeignKey(
        Series,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    series_order = models.PositiveIntegerField(
        null=True,
        blank=True
    )


    author = models.ForeignKey(
        "core.TeamMember",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )


    youtube_url = models.URLField(
        blank=True
    )

    is_featured = models.BooleanField(
        default=False
    )

    featured_order = models.PositiveIntegerField(
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft"
    )


    published_date = models.DateTimeField(
        null=True,
        blank=True
    )


    seo_title = models.CharField(
        max_length=200,
        blank=True
    )


    seo_description = models.TextField(
        blank=True
    )

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

        constraints = [
        models.UniqueConstraint(
            fields=[
                "series",
                "series_order",
            ],
            name="unique_series_post_order",
        )
    ]

    def reading_time(self):
        words = len(self.body.split())
        minutes = words // 200

        return max(1, minutes)


    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)


    def __str__(self):
        return self.title