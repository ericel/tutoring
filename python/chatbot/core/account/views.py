
from django.views.generic import TemplateView
from django.contrib.auth import logout
from django.shortcuts import redirect

class HomeListView(TemplateView):
    """Handles home view"""
    template_name = "home.html"

# Log out view
def Logout(request):
    logout(request)
    # Redirect to a success page.
    return redirect("/")
