from django.shortcuts import render
from django.views.generic import ListView
from home.models import League


# delete after implementing views for particular leagues
def dummy_view(request):
    return render(request, "home/dummy.html", {"leagues": League.objects.all()})


class HomeView(ListView):
    model = League
    template_name = "home/home.html"
    context_object_name = "leagues"
