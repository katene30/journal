from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('entries/', views.EntryListView.as_view(), name='entry_list'),
    path('entries/new/', views.EntryCreateView.as_view(), name='entry_create'),
    path('entries/<int:pk>/', views.EntryDetailView.as_view(), name='entry_detail'),
    path('entries/<int:pk>/edit/', views.EntryUpdateView.as_view(), name='entry_update'),
    path('entries/<int:pk>/delete/', views.EntryDeleteView.as_view(), name='entry_delete'),
    path('summary/', views.summary, name='summary'),
]
