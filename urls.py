from django.urls import path
from notes_app import views

urlpatterns = [
    path('', views.login_view),
    path('register/', views.register),
    path('login/', views.login_view),
    path('logout/', views.logout_view),
    path('notes/', views.notes_view),
    path('notes/add/', views.add_note),
    path('notes/<int:note_id>/', views.view_note),
    path('search/', views.search),
]