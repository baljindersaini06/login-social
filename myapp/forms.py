from django import forms
from django.contrib.auth.models import User, Group,Permission
from myapp.models import *

from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from django_countries.fields import CountryField
from django_countries import widgets, countries
import datetime

User = get_user_model()


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "phone_no" ,"password1", "password2")


class LoginForm(forms.ModelForm):
    username = forms.CharField(max_length=30, required=True)
    password = forms.CharField(widget=forms.PasswordInput,max_length=30, required=False)

    class Meta:
        model = User
        fields = ['username', 'password']


class PasswordChangedForm(PasswordChangeForm):
    old_password_flag = True
    old_password = forms.CharField(widget=forms.PasswordInput,max_length=30,required=True)
    new_password1 = forms.CharField(widget=forms.PasswordInput,max_length=30,required=True)
    new_password2 = forms.CharField(widget=forms.PasswordInput,max_length=30,required=True)

    def set_old_password_flag(self): 

    #This method is called if the old password entered by user does not match the password in the database, which sets the flag to False

        self.old_password_flag = False

        return 0

    def clean_old_password(self, *args, **kwargs):
        old_password = self.cleaned_data.get('old_password')

        if not old_password:
            raise forms.ValidationError("You must enter your old password.")

        if self.old_password_flag == False:
        #It raise the validation error that password entered by user does not match the actucal old password.

            raise forms.ValidationError("The old password that you have entered is wrong.")

        return old_password


    def clean(self):
        cleaned_data = super(PasswordChangedForm, self).clean()
        old_password = cleaned_data.get('old_password')
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if new_password1 != new_password2:
            raise forms.ValidationError('The passwords does not match.')
        return cleaned_data


class UserForm(forms.ModelForm):
    profile_image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

class ImageForm(forms.ModelForm):
    profile_image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['profile_image']
        


class SiteForm(forms.ModelForm):
    site_name = forms.CharField(max_length=50, required=True)
    site_email=forms.EmailField(max_length=50, required=True)
    site_favicon = forms.ImageField()
    site_logo = forms.ImageField()
    site_address = forms.CharField(max_length=200,required=True)
    copy_right = forms.CharField(max_length=200,required=True)
    
    class Meta:
        model = SiteConfiguration
        fields = ['site_name', 'site_email', 'site_favicon','site_logo','site_address','copy_right']


class UpdateSiteForm(forms.ModelForm):
    site_name = forms.CharField(max_length=50, required=True)
    site_email=forms.EmailField(max_length=50, required=True)
    site_favicon = forms.ImageField(required=True)
    site_logo = forms.ImageField(required=True)
    site_address = forms.CharField(max_length=200,required=True)
    copy_right = forms.CharField(max_length=200,required=True)

    class Meta:
        model = SiteConfiguration
        fields = ['site_name', 'site_email', 'site_favicon','site_logo','site_address','copy_right']


class SmtpForm(forms.ModelForm):
    smtp_email=forms.EmailField(max_length=50, required=True)
    smtp_password = forms.CharField(widget=forms.PasswordInput,max_length=50, required=True)

    class Meta:
        model = SmtpConfiguration
        fields = ['smtp_email', 'smtp_password']


class SignUpForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    username = forms.CharField(max_length=254)
    email = forms.EmailField(max_length=254,required=True)
    role =forms.ModelChoiceField(queryset=Group.objects.all()) 
   
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'phone_no', 'role','company_name','department','hr_start_date','hr_title','ht_birth_date','hr_notes','hr_emergency_contact_name','hr_emergency_contact_relation','hr_emergency_conatct_no')
        

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).count() > 0:
            raise forms.ValidationError('This email address is already registered.')
        return email

    def clean_phone_no(self):
        phone_no = self.cleaned_data.get('phone_no')
        # username = self.cleaned_data.get('username')
        if phone_no and User.objects.filter(phone_no=phone_no).count() > 0:
            raise forms.ValidationError('This phone number is already registered.')
        return phone_no


class SetPasswordForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput,max_length=30, required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput,max_length=30, required=False)
   
    class Meta:
        model = User
        fields = ('password', 'confirm_password')

    def clean(self):
        cleaned_data = super(SetPasswordForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        # check for min length
        min_length = 8
        if len(password) < min_length:
            msg = 'Password must be at least %s characters long.' %(str(min_length))
            self.add_error('password', msg)

        # check for digit
        if sum(c.isdigit() for c in password) < 1:
            msg = 'Password must contain at least 1 number.'
            self.add_error('password', msg)
        
        if password != confirm_password:
            raise forms.ValidationError('The passwords does not match.')
        return cleaned_data




class CompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = ('company_name', 'contact_number', 'description', 'company_logo','company_map')


class EmployeeForm(forms.ModelForm):

    class Meta:
        model = Employee
        fields = ('company_name', 'employee_name', 'phone_number', 'note', 'designation', 'employee_email',)



class EmployeeInfoForm(forms.ModelForm):

    class Meta:
        model = Employee
        fields = ('note', 'designation')


class UpdateEmployeeForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('phone_no','email')



class UpdateEmployeeInfo(forms.ModelForm):
    note = forms.CharField(max_length=254,required=False)
    designation = forms.CharField(max_length=254,required=False)
    class Meta:
        model = Employee

        fields = ('phone_number','note', 'designation','employee_email','emp_location','workstation')        


        
class GroupForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.SelectMultiple(attrs={"class" : "form-control select-multiple"}))
    class Meta:
        model = Group
        fields = ('name', 'permissions')


class GroupUpdateForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.SelectMultiple(attrs={"class" : "form-control select-multiple"}))
    class Meta:
        model = Group
        fields = ('name', 'permissions')


class User_updateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    username = forms.CharField(max_length=254)
    email = forms.EmailField(max_length=254,required=True)
    role =forms.ModelChoiceField(queryset=Group.objects.all()) 
    phone_no =  forms.CharField(max_length=10, required=True)
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'phone_no', 'role')
        


class LocationForm(forms.ModelForm):
    location_bussiness_hours = forms.CharField(max_length=30, required=False)
    class Meta:
        model = Location
        fields = ('company_id','location_name','location_address','country','location_city','location_postal_code','location_bussiness_hours','is_headquater','is_off_hours_accessible') 




class LocationUpdateForm(forms.ModelForm):
    location_bussiness_hours = forms.CharField(max_length=30, required=False)

    class Meta:
        model = Location
        fields = ('location_name','location_address','country','location_city','location_postal_code','location_bussiness_hours','is_headquater','is_off_hours_accessible') 





class WebsiteForm(forms.ModelForm):
    class Meta:
        model = Website
        fields = ('website_company_name','website_type','website_name','website_url','is_headquater_website')        


class Website_UpdateForm(forms.ModelForm):
    class Meta:
        model = Website
        fields = ('website_type','website_name','website_url')        




class LicenceForm(forms.ModelForm):
    class Meta:
        model = Licence
        fields = ('licence_type_id','company_id','licence_name','licence_key','workstation_asset_tag','aquisition_date','activation_date','expire_date','licence_note')        


class Licence_UpdateForm(forms.ModelForm):
    class Meta:
        model = Licence
        fields = ('licence_type_id','licence_name','licence_key','workstation_asset_tag','aquisition_date','activation_date','expire_date','licence_note')        




class DocumentsForm(forms.ModelForm):

    class Meta:
        model = Documents
        fields = ('compani_name','document_category_id','name','title','content')        

class DocumentsUpdateForm(forms.ModelForm):
    class Meta:
        model = Documents
        fields = ('document_category_id','name','title','content')        


class DocumentsFileForm(forms.ModelForm):
    file_upload=forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    class Meta:
        model = Document_File
        fields = ('file_upload',)        
  

class DocumentsLinkForm(forms.ModelForm):
    class Meta:
        model = Document_Links
        fields = ('links',)        
  

class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ('name','description','connectwise_check','connectwise_api','moneris_check','moneris_api')  



class Company_package_Form(forms.ModelForm):
    class Meta:
        model = Company_package
        fields = ('companys_name','Package_selected')          

class DeviceForm(forms.ModelForm):
    device_password = forms.CharField(max_length=10, widget=forms.PasswordInput)
    class Meta:
        model = Device
        fields = ('device_type_id','company_id','location_id','device_name','device_url_address','device_note','device_username','device_password')        


class Device_UpdateForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ('device_name','device_url_address','device_note','device_username','device_password')          



class Meeting_Form(forms.ModelForm):
    attendees = forms.ModelMultipleChoiceField(
        queryset=Employee.objects.all(),
        widget=forms.SelectMultiple(attrs={"class" : "form-control select-multiple"}))
    date_time =forms.DateField(required=True,widget=forms.TextInput(
            attrs={
                'id': 'date_time',
                
            }
        ))
    
    class Meta:
        model = Meeting
        fields=('title','date_time','time','where','attendees','priority')

    