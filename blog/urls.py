from django.urls import path
from . import views

urlpatterns = [
    path('',views.HomeView.as_view(),name="home"),
    path('about/',views.about,name="about"),
    path('post/<int:pk>/',views.PostDetailView.as_view(),name="post_detail"),
    path('post/new/',views.PostCreateView.as_view(),name="post_create"),
    path('post/<int:pk>/update/',views.PostUpdateView.as_view(),name="post_update"),
    path('post/<int:pk>/delete/',views.PostDeleteView.as_view(),name="post_delete"),
    path('drafts/',views.DraftListView.as_view(),name="post_draft_list"),
    path('post/<int:pk>/publish/',views.post_publish,name="post_publish"),
    path('user/category/new/', views.CategoryCreateView.as_view(), name = 'category_create'),
    path('user/tag/new/', views.TagCreateView.as_view(), name = 'tag_create'),
    path('category/<str:n>/',views.post_by_category,name='post_by_category'),
    path('tag/<str:n>/', views.post_by_tag, name = 'post_by_tag'),
    path('user/<int:pk>/',views.user_posts,name="user_posts"),
    path('user/category/list/', views.UserCategoryView.as_view(), name = 'user_category'),
    path('user/tag/list/', views.UserTagView.as_view(), name = 'user_tag'),
    path('feedback/',views.feedback_form,name="feedback"),
    path('post/<int:pk>/comment/',views.add_comment_to_post,name="add_comment_to_post"),
    path('comment/<int:pk>/approve/',views.comment_approve,name="comment_approve"),
    path('comment/<int:pk>/remove/',views.comment_remove,name="comment_remove")
]
# path('user/<int:pk>/',views.UserPostListView.as_view(),name="user_posts"),
#  path('category/<slug:slug>/',views.post_by_category,name='post_by_category'),