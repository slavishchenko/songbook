from django.urls import path
from . import views
from .views import RepertoarUpdateView, RepertoarDeleteView

urlpatterns = [
    path('', views.repertoar, name='repertoar'),
    path('<int:pk>/<str:slug>/', views.repertoar_detail, name='repertoar-detail'),
    path('<int:pk>/<str:slug>/uredi/', RepertoarUpdateView.as_view(), name='repertoar-update'),
    path('<int:pk>/<str:slug>/ukloni/', RepertoarDeleteView.as_view(), name='repertoar-delete'),
    path('<int:pk>/<str:slug>/<int:id>/ukloni-pesmu/', views.ukloni_pesmu, name='ukloni-pesmu'),
    path('dodaj-pesmu/<int:id>', views.dodaj_pesmu, name='dodaj-pesmu')
]
