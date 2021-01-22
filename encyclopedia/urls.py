from django.urls import path
from . import views

urlpatterns = [path("", views.index, name="index"),
               path("wiki/", views.index, name="inicio"),
               path("wiki/<str:name>", views.wiki, name="wiki"),
               path("edit/<str:name>", views.edit, name="edit"),
               path("edit/", views.edit, name="editar"),
               path("random/", views.random, name="random"),
               path("create/", views.create, name="create"),
               path("search", views.search, name="search")]
