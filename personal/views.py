from django.shortcuts import render



def temp(request):
	context = {}
	return render(request, "personal/temp1.html", context)



def dashboard(request):
	context = {}
	return render(request, "personal/dashboard.html", context)

def home_proj(request):
	context = {}
	return render(request, "personal/home.html", context)


def home_screen_view(request):
	context = {}
	return render(request, "personal/home2.html", context)
