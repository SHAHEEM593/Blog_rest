from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='user-registration'),
    path('login/', views.UserLoginView.as_view(), name='user-login'),
    path('blogposts/', views.BlogListCreateView.as_view(), name='blog-list-create'),
    path('blogposts/<int:pk>/', views.BlogDetailView.as_view(), name='blog-detail'),
    path('comments/', views.CommentListCreateView.as_view(), name='comment-list'),
    path('comments/<int:pk>/', views.CommentDetailView.as_view(), name='comment-detail'),
    path('blogposts/admin/', views.AdminBlogPostList.as_view(), name='admin_blogpost_list'),
    path('blogposts/admin/<int:pk>/', views.AdminBlogPostDetailView.as_view(), name='admin_blogpost_detail'),
    path('comments/admin/', views.AdminCommentList.as_view(), name='admin_comment_list'),
    path('comments/admin/<int:pk>/', views.AdminCommentDetailView.as_view(), name='admin_comment_detail'),
    path('register/admin/', views.AdminUserRegistrationView.as_view(), name='admin-user-registration'),

]