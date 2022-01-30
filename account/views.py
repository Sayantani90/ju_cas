from http.client import REQUEST_ENTITY_TOO_LARGE
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.conf import settings
from account.models import Account

from account.forms import RegistrationForm,AccountAuthenticationForm,AccountUpdateForm
from account.forms import AccountCasForm


def register_view(request, *args, **kwargs):
	user = request.user
	if user.is_authenticated: 
		return HttpResponse("You are already authenticated as " + str(user.email))

	context = {}
	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email').lower()
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(email=email, password=raw_password)
			login(request, account)
   		    # destination = get_redirect_if_exists(request)
			destination = kwargs.get("next")
   
			if destination:
				return redirect(destination)
			return redirect('home')
		else:
			context['registration_form'] = form

	else:
		form = RegistrationForm()
		context['registration_form'] = form
	return render(request, 'account/register.html', context)

def logout_view(request):
	logout(request)
	return redirect("login")

def login_view(request, *args, **kwargs):
	context = {}
	
	user = request.user
	if user.is_authenticated: 
		return redirect("account:cas", user_id=request.user.id)

	destination = get_redirect_if_exists(request)
	print("destination: " + str(destination))

	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)

			if user:
				login(request, user)
				if destination:
					return redirect(destination)
				return redirect("account:cas", user_id=request.user.id)

	else:
		form = AccountAuthenticationForm()
	
 
	context['login_form'] = form
    
	return render(request, "account/login.html", context)


def get_redirect_if_exists(request):
	redirect = None
	if request.GET:
		if request.GET.get("next"):
			redirect = str(request.GET.get("next"))
	return redirect

def account_view(request, *args, **kwargs):
	"""
	- Logic here is kind of tricky
		is_self (boolean)
			is_friend (boolean)
				-1: NO_REQUEST_SENT
				0: THEM_SENT_TO_YOU
				1: YOU_SENT_TO_THEM
	"""
	context = {}
	user_id = kwargs.get("user_id")
	try:
		account = Account.objects.get(pk=user_id)
	except:
		return HttpResponse("Something went wrong.")
	if account:
		context['id'] = account.id
		context['username'] = account.username
		context['email'] = account.email
		context['profile_image'] = account.profile_image.url
		context['hide_email']    = account.hide_email
		context['last_login']  = account.last_login
		context['Department']  = account.Department
		context['Designation'] = account.get_Designation_display
		context['pan_no'] 	   = account.pan_no
		context['highest_quali']  = account.highest_quali
		context['gender']  = account.get_gender_display
		context['dt_ob']  = account.dt_ob
		context['date_joined']  = account.date_joined
		context['quali_year']  = account.quali_year
		context['tot_experience']  = account.tot_experience
		

		# Define template variables
		is_self = True
		is_friend = False
		user = request.user
		if user.is_authenticated and user != account:
			is_self = False
		elif not user.is_authenticated:
			is_self = False
			
		# Set the template variables to the values
		context['is_self'] = is_self
		context['is_friend'] = is_friend
		context['BASE_URL'] = settings.BASE_URL
		return render(request, "account/account.html", context)

    
def edit_account_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login")
    user_id = kwargs.get("user_id")    
    account = Account.objects.get(pk=user_id)
    
    if request.method == "GET":
        if user_id == 0:
            form = AccountUpdateForm()
        else:
            account = Account.objects.get(pk=user_id)            
            form = AccountUpdateForm(instance=account)
        return render(request, "account/edit2_account.html", {'form': form})
		
    else:
        if user_id == 0:
            form = AccountUpdateForm(request.POST)
        else:
            account = Account.objects.get(pk=user_id)
            form = AccountUpdateForm(request.POST,instance= account)
        if form.is_valid():
            form.save()
        # return redirect("account:view", pk=account.id)
        return redirect("account:view", user_id=account.pk)
    
                  
def cas_view(request,*args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login")
    user_id = kwargs.get("user_id")    
    account = Account.objects.get(pk=user_id)
    
    if request.method == "GET":
        if user_id == 0:
            form = AccountCasForm()
        else:
            account = Account.objects.get(pk=user_id)            
            form = AccountCasForm(instance=account)
        return render(request, "account/cas_register.html", {'form': form})
		
    else:
        if user_id == 0:
            form = AccountCasForm(request.POST)
        else:
            account = Account.objects.get(pk=user_id)
            form = AccountCasForm(request.POST,instance= account)
        if form.is_valid():
            form.save()
        # return redirect("account:view", pk=account.id)
        return redirect("home")
    
    
    
    
    
    
        
        return render(request, "account/cas_register.html", context)
  