from django.shortcuts import get_object_or_404, render
from .models import Post, Category, Series
from django.views.generic import ListView, DetailView
from .utils import render_markdown, get_youtube_embed_url

class PostListView(ListView):

    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"

    queryset = Post.objects.filter(
        status="published",
        is_featured=False
    ).order_by(
        "-published_date"
    )

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["featured_posts"] = Post.objects.filter(
            status="published",
            is_featured=True
        ).order_by(
            "-published_date"
        )[:3]

        context["categories"] = Category.objects.all()

        return context


# Post Detail View
class PostDetailView(DetailView):

    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    queryset = Post.objects.filter(
        status="published"
    )

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["body_html"] = render_markdown(
            self.object.body)

        context["youtube_embed_url"] = get_youtube_embed_url(
            self.object.youtube_url
        )

     # Previous / next article navigation (across all published posts)

        published_posts = list(
            Post.objects.filter(
                status="published"
            ).order_by(
                "-published_date"
            )
        )

        if self.object in published_posts:

            current = published_posts.index(self.object)

            context["previous_article"] = (
                published_posts[current - 1]
                if current > 0
                else None
            )

            context["next_article"] = (
                published_posts[current + 1]
                if current < len(published_posts) - 1
                else None
            )

     # Series navigation

        if self.object.series:

            series_posts = list(
                self.object.series.posts.filter(
                    status="published"
                ).order_by(
                    "series_order",
                    "published_date",
                )
            )

            if self.object not in series_posts:
                return context

            current_index = series_posts.index(
                self.object
            )

            context["series_posts"] = series_posts

            context["series_position"] = (
                current_index + 1
            )

            context["series_total"] = len(
                series_posts
            )

            context["previous_post"] = (
                series_posts[current_index - 1]
                if current_index > 0
                else None
            )

            context["next_post"] = (
                series_posts[current_index + 1]
                if current_index < len(series_posts) - 1
                else None
            )

        return context

# Category Post List View
class CategoryPostListView(ListView):

    model = Post
    template_name = "blog/category_posts.html"
    context_object_name = "posts"

    def get_queryset(self):

        return Post.objects.filter(
            categories__slug=self.kwargs["slug"],
            status="published"
        ).order_by(
            "-published_date"
        )

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["category"] = Category.objects.get(
            slug=self.kwargs["slug"]
        )

        return context