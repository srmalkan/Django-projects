from django.urls import path
from . import views
from .views import postList,postDetail,postCreateView,postUpdateView,postDeleteView,publishView,postshareFormView
app_name='blog'
urlpatterns = [
    path('',postList.as_view(),name='post_list'),
    path('tag/<slug:tag_slug>/',postList.as_view(),name='post_list_tag'),
    path('update/<pk>/'
        ,postUpdateView.as_view(),name='update_post'),
    path('delete/<pk>/'
        ,postDeleteView.as_view(),name='delete_post'),
    path('publish/<pk>/'
        ,publishView.as_view(),name='publish_post'),
    path('add/',postCreateView.as_view(),name='addPost'),
    path('<pk>/'
        ,postDetail.as_view(),name='post_detail'),
    path('<int:post_id>/share/',postshareFormView.as_view,name='share_post'),
    
]