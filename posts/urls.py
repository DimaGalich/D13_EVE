from django.urls import path, include

from .views import *


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/create/', PostCreateView.as_view(), name='post_create'),
    path('posts/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('posts/<int:pk>/reply/', reply, name='reply'),
    path('posts/<int:pk>/replied/', replied, name='replied'),
    path('private/', PrivateOfficeView.as_view(), name='private_office'),
    path('private/<int:pk>/', ReplyDetailView.as_view(), name='reply_detail'),
    path('private/<int:pk>/delete/', ReplyDeleteView.as_view(), name='reply_delete'),
    path('private/<int:pk>/approve/', reply_approve, name='reply_approve'),
    path('private/by_post/<int:post_id>/', SortedByPostView.as_view(), name='sorted_by_post'),
    path('subscribe/', subscribe, name='subscribe'),
    path('unsubscribe/', unsubscribe, name='unsubscribe'),
]
