from django.urls import path

from . import views

app_name = "subscriptions"
urlpatterns = [
    path(
        "create",
        view=views.CreateSubscriptionView.as_view(),
        name="subscription_create",
    ),
]
