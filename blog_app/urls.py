from django.urls import path
from .views import RegisterView,LoginAuthor, AuthorDetailView,AuthorListView, AuthorUpdateView, AuthorDeleteView, CreateBlogView, BlogListView,BlogDetailView, BlogDeleteView, BlogUpdateView

urlpatterns = [
    path('authors/create/', RegisterView.as_view()),
    path('authors/login/', LoginAuthor.as_view()),
    path('authors/all/', AuthorListView.as_view()),
    path('authors/<int:id>/', AuthorDetailView.as_view()),
    path('authors/update/<int:id>/', AuthorUpdateView.as_view()),
    path('authors/delete/<int:pk>', AuthorDeleteView.as_view()),
    path('authors/', AuthorListView.as_view()),
    path('blogs/create/', CreateBlogView.as_view()),
    path('blogs/', BlogListView.as_view()),
    path('blogs/<int:blog_id>/', BlogDetailView.as_view()),
    path('blogs/delete/<int:blog_id>', BlogDeleteView.as_view()),
    path('blogs/update/<int:blog_id>',BlogUpdateView.as_view())
]
