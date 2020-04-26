from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('chats/', views.chats_test, name='chats'),
    path('questionnaire/', views.survey, name='chats'),
    path('account/', views.account, name='account'),
    path('survey/', views.survey, name='survey'),
    path('chat_members/<id>/', views.chat_members, name='chat_members'),
    path('chats_moderator/', views.chats_moderator, name='chats_moderator'),
    path('account_moderator/', views.account_moderator, name='account_moderator'),
    path('reviews/<id>/', views.reviews, name='reviews'),
]