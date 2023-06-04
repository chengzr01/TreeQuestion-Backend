from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
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
    path("read_tree", views.read_tree, name="read_tree")
]