import os

from django.http import HttpResponse
from django.shortcuts import render
from lib.graphs import gen_speech

# Create your views here.


def pick(request):
    return render(request, "speeches/pick.html")
    # return render(request, "reddit/search.html")


def obama(request):
    files = [
        "Obama - 20080603.txt",
        "Obama - 20080828.txt",
        "Obama - 20081103.txt",
        "Obama - 20081104.txt",
        "Obama - 20090120.txt",
    ]
    contents = []
    for filename in files:
        with open(os.path.join(os.path.dirname(__file__), f"obama/{filename}")) as f:
            for x in f.read().split("\n\n"):
                contents.append(x)

    # with open(os.path.join(os.path.dirname(__file__), "obama/Obama - 20080603.txt")) as f, open(
    #     os.path.join(os.path.dirname(__file__), "obama/Obama - 20080828.txt")
    # ) as g:

    #     contents = f.read().split("\n\n")
    #     for g in g.read().split("\n\n"):
    #         contents.append(g)
    contents = [x.split() for x in contents]
    speech = gen_speech(contents)
    speech = " ".join([x for x in speech])
    # print(contents)
    ctx = {}
    ctx["speech"] = speech
    ctx["name"] = "Obama"
    return render(request, "speeches/read.html", context=ctx)


def lincoln(request):
    files = ["lincoln1.txt", "lincoln2.txt", "lincoln3.txt", "lincoln4.txt"]
    contents = []
    for filename in files:
        with open(os.path.join(os.path.dirname(__file__), f"lincoln/{filename}")) as f:
            for x in f.read().split("\n\n"):
                contents.append(x)

    # with open(os.path.join(os.path.dirname(__file__), "obama/Obama - 20080603.txt")) as f, open(
    #     os.path.join(os.path.dirname(__file__), "obama/Obama - 20080828.txt")
    # ) as g:

    #     contents = f.read().split("\n\n")
    #     for g in g.read().split("\n\n"):
    #         contents.append(g)
    contents = [x.split() for x in contents]
    speech = gen_speech(contents)
    speech = " ".join([x for x in speech])
    # print(contents)
    ctx = {}
    ctx["speech"] = speech
    ctx["name"] = "Lincoln"
    return render(request, "speeches/read.html", context=ctx)
