from django.views.generic import TemplateView

from blog.models import Post
from .models import TeamMember


class HomeView(TemplateView):
    """The public landing page.

    Pulls together the pieces shown on the homepage: the featured post
    strip, the latest posts, and the founder profile.
    """

    template_name = "core/home.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["featured_posts"] = Post.objects.filter(
            status="published",
            is_featured=True
        ).order_by(
            "-published_date"
        )[:3]

        context["latest_posts"] = Post.objects.filter(
            status="published"
        ).order_by(
            "-published_date"
        )[:5]

        context["founder"] = TeamMember.objects.filter(
            role="Founder",
            is_active=True
        ).first()

        return context