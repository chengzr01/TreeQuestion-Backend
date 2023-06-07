from . import views
from . import cache
from django.urls import path

urlpatterns = [
    path("create_knowledge_component",
         views.create_knowledge_component,
         name="create_knowledge_component"),
    path("create_knowledge_graph",
         views.create_knowledge_graph,
         name="create_knowledge_graph"),
    path("create_key_statement",
         views.create_key_statement,
         name="create_key_statement"),
    path("create_distractor_statement",
         views.create_distractor_statement,
         name="create_distractor_statement"),
    path("create_question", views.create_question, name="create_question"),
    path("create_tree", views.create_tree, name="create_tree"),
    path("read_tree", views.read_tree, name="read_tree"),
    path("delete_tree", views.delete_tree, name="delete_tree"),
    path("delete_cache", cache.delete_cache, name="delete_cache"),
    path("refresh_cache", cache.refresh_cache, name="refresh_cache")
]