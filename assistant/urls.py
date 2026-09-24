from django.urls import path
from . import views

urlpatterns = [
    path("documents/", views.document_list, name="document-list"),
    path("documents/<int:document_id>/", views.document_delete, name="document-delete"),
    path("ask/", views.ask_question, name="ask-question"),
    path("conversations/", views.conversation_create, name="conversation-create"),
    path("conversations/<int:conversation_id>/", views.conversation_detail, name="conversation-detail"),
    path("conversations/<int:conversation_id>/ask/", views.conversation_ask, name="conversation-ask"),
]