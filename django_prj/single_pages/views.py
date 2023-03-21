from django.shortcuts import render


def main(request):
    return render(
        request,
        'single_pages/main.html'
    )

# Create your views here.
