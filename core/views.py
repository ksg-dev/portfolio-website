from django.shortcuts import render


def home(request):
    return render(request, "core/index.html")


def about(request):
    return render(request, "core/about.html")


def contact(request):
    return render(request, "core/contact.html")


def privacy(request):
    return render(request, "core/privacy.html")


def terms(request):
    return render(request, "core/terms.html")
