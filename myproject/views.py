from django.shortcuts import render

def homePage(request):
  return render(request, "home.html")

def homePageWithName(request, name):
  return render(request, "home.html", {"name": name})