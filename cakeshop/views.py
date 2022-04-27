from django.shortcuts import render


def view(request):
    context = {}
    return render(request, 'index.html', context)
