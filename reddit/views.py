from django.shortcuts import render
from .forms import RedditSearch
from django.http import HttpResponse

# Create your views here.


def search(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = RedditSearch(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponse(form.cleaned_data["q"])

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RedditSearch()

    return render(request, "reddit/search.html", {"form": form})
    # return render(request, "reddit/search.html")
