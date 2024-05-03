from django.urls import path
from hello import views
from hello.models import LogMessage, ChatMessage
from django.contrib.auth import views as auth_views

home_list_view = views.HomeListView.as_view(
    queryset=LogMessage.objects.order_by("-log_date")[:5],  # :5 limits the results to the five most recent
    context_object_name="message_list",
    template_name="hello/home.html",
)

blog_list_view = views.BlogListView.as_view(
    queryset=ChatMessage.objects.order_by("-log_date")[:5],  # :5 limits the results to the five most recent
    context_object_name="message_list",
    template_name="hello/blog.html",
)

urlpatterns = [
    path("", home_list_view, name="home"),
    path("projects/", views.projects, name="projects"),
    path("about/", views.about, name="about"),
    path("blog/", blog_list_view, name="blog"),
    path("post/", views.blog, name="post"),
    path("login/", views.login_view, name="login" ),
    path("logout/", views.logout_view, name="logout" ),
    path("register/", views.register_user, name="register"),
    path("change-password/", auth_views.PasswordChangeView.as_view()),
]