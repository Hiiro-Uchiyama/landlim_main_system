from django.shortcuts import render, get_object_or_404, redirect

def about_landlim(request):
    return render(request, 'description/about_landlim.html')

def about_landlim_web_edition(request):
    return render(request, 'description/about_landlim_web_edition.html')

def about_landlim_mobile_edition(request):
    return render(request, 'description/about_landlim_mobile_edition.html')

def about_landlim_api_system(request):
    return render(request, 'description/about_landlim_api_system.html')

def about_landlim_network_system(request):
    return render(request, 'description/about_landlim_network_system.html')

def about_landlim_recruitment_system(request):
    return render(request, 'description/about_landlim_recruitment_system.html')