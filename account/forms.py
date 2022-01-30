from django import forms
from django.forms import Form, ModelForm, DateField, widgets
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.forms import ModelChoiceField
import uuid
from account.models import Account,Department




class RegistrationForm(UserCreationForm):
	# email = forms.EmailField(max_length=60, help_text='Required. Add a valid email address.')

	class Meta:
		model = Account
		fields = ('username','Department','Designation','email','post','gender','password1','password2')
    

		widgets =  {            
            'username'    : widgets.TextInput(attrs={'style':'width:330px;height:40px'}),
            'Department'  : widgets.Select(attrs={'style': 'width:330px;height:40px'}),
            'Designation' : widgets.Select(attrs={'style': 'width:330px;height:40px'}),
            'email'       : widgets.TextInput(attrs={'style': 'width:330px;height:40px'}),
            'post'        : widgets.Select(attrs={'style': 'width:330px;height:40px'}),
            'gender'      : widgets.Select(attrs={'style': 'width:330px;height:40px'}),
        }
   
		labels =  {
            'username':'Full Name',
            'email' : 'Email account',
            'Department':'Name of the Department',
            'post':'Post applied for',
            'gender': 'Gender',
            'Designation' : 'Designation',
        }
          
  
            
	def clean_email(self):
		email = self.cleaned_data['email'].lower()
		try:
			account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
		except Account.DoesNotExist:
			return email
		raise forms.ValidationError('Email "%s" is already in use.' % account)

	def clean_username(self):
		username = self.cleaned_data['username'].capitalize()
  
		try:
			account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
		except Account.DoesNotExist:
			return username
		raise forms.ValidationError('Username "%s" is already in use.' % username)
		
	def __init__(self, *args, **kwargs):
            super(RegistrationForm,self).__init__(*args, **kwargs)            
            self.fields['Department'].empty_label = "Select"
            self.fields['Department'].required = True            
            self.fields['Designation'].required = True
            self.fields['email'].widget.attrs['placeholder'] = 'Enter email' 
            self.fields['username'].widget.attrs['placeholder'] = 'Enter full name'       
            self.fields['username'].widget.attrs['autofocus'] = True
            self.fields['post'].required = True
            self.fields['gender'].required = True


class AccountAuthenticationForm(forms.ModelForm):
	# email = forms.EmailField(max_length = 60, widget=forms.TextInput(attrs={'placeholder': 'Ime'}))
    email = forms.EmailField(max_length = 60, widget=forms.TextInput(attrs={'placeholder': 'Ime'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    
    class Meta:
        model = Account
        fields = ('email', 'password')
        
    def clean(self):
     if self.is_valid():
         email = self.cleaned_data['email']
         password = self.cleaned_data['password']
         if not authenticate(email=email, password=password):
             raise forms.ValidationError("Invalid login(email or pwd")

class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        # fields = "__all__"
        fields = ('username', 'email', 'Department', 'Designation',
                  'highest_quali', 'pan_no','gender','highest_quali',
                  'dt_ob','date_joined','quali_year','tot_experience'
                  
                  )
        
        widgets = {
            'username' :widgets.TextInput(attrs={'size':'30'}),
            'Department' : widgets.Select(attrs={'style': 'width:330px'}),
            'Designation' : widgets.Select(attrs={'style': 'width:330px'}),            
            'dt_ob': widgets.DateInput(attrs={'type': 'date'}),
            'date_joined': widgets.DateInput(attrs={'type': 'date'}),
            'email': widgets.TextInput(attrs={'size':'30'}),            
            'pan_no': widgets.TextInput(attrs={'size':'12'}),
            'highest_quali':widgets.TextInput(attrs={'size':'33'}),
            'quali_year' : widgets.TextInput(attrs={'size':'4'}), 
            'tot_experience':widgets.TextInput(attrs={'size':'2'}),
        }
        
        labels = {
            'username':'Full Name',
            'email' : 'Email account',
            'Department':'Name of the Department',
            'pan_no' :'PAN No.',
            'gender' : 'Gender',
            'Designation' : 'Designation',
            'highest_quali' : 'Highest Qualification',
            'dt_ob' : 'Date of Birth',
            'date_joined' : 'Date of joining',
            'quali_year' : 'Qualifying Year',
            'tot_experience' : 'Experiences'
            
        }
        
    def __init__(self, *args, **kwargs):
        super(AccountUpdateForm,self).__init__(*args, **kwargs)
        self.fields['Department'].empty_label = "Select"
        self.fields['Department'].required = True
        self.fields['Designation'].empty_label = "Select"
        self.fields['Designation'].required = True        
        self.fields['gender'].required = True
        self.fields['email'].widget.attrs['readonly'] = True

class AccountCasForm(forms.ModelForm):
    class Meta:
        model = Account
        # fields = "__all__"
        fields = ('username', 'parent', 'dt_ob', 'catg','Department','Designation',
                  'agp', 'dt_last_promo','dt_eligibility','addr_corres', 'addr_perm',
                  'mobile','email', 'from_dsg', 'to_dsg'
                  
                  )
        prepopulated_fields = {'addr_perm':('addr_corres',)}
        
        widgets = {
            'username'      : widgets.TextInput(attrs={'style': 'width:400px;text-transform:uppercase'}),                        
            'parent'        : widgets.TextInput(attrs={'style': 'width:400px;text-transform:uppercase'}),
            'dt_ob'         : widgets.DateInput(attrs={'type': 'date'}),
            'Department'    : widgets.Select(attrs={'style': 'width:400px;height:35px;text-transform:uppercase'}),
            'Designation'   : widgets.Select(attrs={'style': 'width:400px;height:35px;text-transform:uppercase'}),
            'catg'          : widgets.Select(attrs={'style': 'height:35px'}),
            'addr_corres'   : widgets.Textarea(attrs={'class': 'form-control', 'rows': 3,'style': 'text-transform:uppercase' }),            
            'addr_perm'     : widgets.Textarea(attrs={'class': 'form-control', 'rows': 3,'style': 'text-transform:uppercase' }),
            'agp'           : widgets.Select(attrs={'style': 'height:35px'}),
            'dt_last_promo' : widgets.DateInput(attrs={'type': 'date'}),
            'dt_eligibility': widgets.DateInput(attrs={'type': 'date'}),
            
            'mobile'        : widgets.NumberInput(attrs={'max': '10', 'required': True, 'type': 'number',}),
            'email'        : widgets.TextInput(attrs={'style': 'width:400px'}),
        }
        
        labels = {
            'username':'Name (in Block letter)',
            'parent' : "Father's Name/Mother's Name (in Uppercase)",
            'dt_ob':'Date of Birth',
            'catg' :'Category',
            'Department' : 'Department/School',
            'Designation' : 'Current Designation',
            'agp' : 'Academic Grade Pay (AGP)',
            'dt_last_promo' : 'Date of last Promotion, if any',
            'dt_eligibility' : 'Date of eligibility for Promotion',
            'addr_corres' : 'Address for correspondence (with PIN)',
            'addr_perm' : 'Permanent Address (with PIN)',
            'mobile' : 'Mobile No.',
            'email' : 'E-mail Id'
            
        }
