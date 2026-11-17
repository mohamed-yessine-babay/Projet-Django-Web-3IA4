from django.http import HttpResponse

def homePage(request):
  return HttpResponse("welcome to home!")

def homePageWithName(request, name):
  return HttpResponse(f"Welcome to y project, {name}")