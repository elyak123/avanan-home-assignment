from django.urls import path
from avanan.slack import views

app_name = "slack"

urlpatterns = [
    path("events/", views.event_view, name="slack_verification"),
    path("delete-message/", views.delete_message_view)
]
