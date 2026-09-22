from django.db import models


class SiteSettings(models.Model):
    """
    Stores general website information.
    Only one record should exist.
    """

    site_name = models.CharField(max_length=100)

    logo = models.ImageField(
        upload_to="site/"
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=20
    )

    address = models.TextField(
        blank=True
    )

    facebook = models.URLField(
        blank=True
    )

    instagram = models.URLField(
        blank=True
    )

    youtube = models.URLField(
        blank=True
    )

    footer_text = models.CharField(
        max_length=255,
        blank=True
    )

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"


    def save(self, *args, **kwargs):
        # Enforce a single settings row: ignore attempts to create a
        # second one while still allowing the existing row to be updated.
        if SiteSettings.objects.exists() and not self.pk:
            return

        super().save(*args, **kwargs)


    def __str__(self):
        return self.site_name



class TeamMember(models.Model):
    """
    Represents people serving in the ministry.
    Example:
    Founder
    Secretary
    Youth Coordinator
    Counselling Lead
    """

    name = models.CharField(
        max_length=100
    )

    role = models.CharField(
        max_length=100
    )

    photo = models.ImageField(
        upload_to="team/"
    )

    biography = models.TextField(
        blank=True
    )

    favorite_scripture = models.TextField(
        blank=True
    )

    quote = models.TextField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    display_order = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"


    def __str__(self):
        return f"{self.name} - {self.role}"



class AboutPage(models.Model):
    """
    Main about section content.
    """

    heading = models.CharField(
        max_length=200
    )

    content = models.TextField()

    mission = models.TextField(
        blank=True
    )

    vision = models.TextField(
        blank=True
    )

    class Meta:
        verbose_name = "About Page"
        verbose_name_plural = "About Page"


    def __str__(self):
        return self.heading



class EmpowermentProgram(models.Model):
    """An outreach / empowerment initiative people can register for."""

    title = models.CharField(
        max_length=150
    )

    description = models.TextField()

    image = models.ImageField(
        upload_to="empowerment/",
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    registration_link = models.URLField(
        blank=True
    )

    display_order = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        verbose_name = "Empowerment Program"
        verbose_name_plural = "Empowerment Programs"


    def __str__(self):
        return self.title



class ContactMessage(models.Model):
    """
    Stores messages sent from visitors.
    """

    name = models.CharField(
        max_length=100
    )

    email = models.EmailField()

    subject = models.CharField(
        max_length=150
    )

    message = models.TextField()


    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"{self.name} - {self.subject}"