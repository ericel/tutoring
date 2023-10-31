from django.urls import path
from openaibot.views import ChatBotView
app_name = "openaibot"
# filter_view
urlpatterns = [
    path("", ChatBotView.as_view(), name="home"),
]