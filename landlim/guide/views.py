from django.shortcuts import render

def landlim_guide(request):
    return render(request, 'guide/landlim_guide.html')

def landlim_faqs(request):
    return render(request, 'guide/landlim_faqs.html')

def landlim_about(request):
    return render(request, 'guide/landlim_about.html')