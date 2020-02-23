from django.shortcuts import render
from .forms import RedditSearch
from django.http import HttpResponse
from lib.graphs import get_sentences, top_reddit_words

# Create your views here.


def search(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = RedditSearch(request.POST)
        # check whether it's valid:
        if form.is_valid():
            titles = get_sentences(form.cleaned_data["q"])
            top_words = top_reddit_words(form.cleaned_data["q"])
            ctx = {}
            ctx["results"] = titles
            ctx["subreddit"] = form.cleaned_data["q"]
            ctx["top_words"] = top_words

            return render(request, "reddit/results.html", context=ctx)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RedditSearch()

    return render(request, "reddit/search.html", {"form": form})
    # return render(request, "reddit/search.html")
