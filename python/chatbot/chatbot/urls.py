"""chatbot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from core.account.api.views import AuthenticateViewSocial
from core.account.views import HomeListView, Logout

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomeListView.as_view(), name="home"),
    path("account/logout/", Logout, name="auth_logout"),
    path("api/account/auth2/", AuthenticateViewSocial.as_view(), name="auth-view"),
    path("openaibot", include("openaibot.urls"))
]
if settings.DEBUG:
    # test mode
    from django.conf.urls.static import static

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
