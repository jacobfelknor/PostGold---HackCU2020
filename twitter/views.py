from django.shortcuts import render
from .forms import TwitterSearch
from django.http import HttpResponse
from lib.graphs import get_gen_tweets

# Create your views here.


def search(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = TwitterSearch(request.POST)
        # check whether it's valid:
        if form.is_valid():
            titles = get_gen_tweets(form.cleaned_data["q"])
            ctx = {}
            ctx["results"] = titles
            ctx["handle"] = form.cleaned_data["q"]
            return render(request, "twitter/results.html", context=ctx)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TwitterSearch()

    return render(request, "twitter/search.html", {"form": form})
    # return render(request, "reddit/search.html")
