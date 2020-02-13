try:
    from urllib import quote  # Python 2.X
except ImportError:
    from urllib.parse import quote
from django.shortcuts import render, reverse, redirect, get_object_or_404
from .models import *
from activity_log.models import ActivityLog

from .forms import *
from django.contrib import messages
from django.shortcuts import render_to_response
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from myapp.models import User
from django.contrib.auth import update_session_auth_hash
from django.template.response import TemplateResponse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
User = get_user_model()
from myapp.models import SiteConfiguration,SmtpConfiguration, Company, Employee,Website,WebsiteType,Location,LicenceType,Licence,Device,DeviceType,Documents,Document_category,Document_File
from django_otp.decorators import otp_required
from two_factor.models import PhoneDevice
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from django.core.mail import EmailMessage, send_mail
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User,Group
from django.contrib.auth import get_user_model
User = get_user_model()
from django.utils import six
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import permission_required
import json
from django.views.generic.edit import DeleteView
from django.contrib.auth.models import Permission
from django.contrib.admin.models import LogEntry
from django_countries import countries

def group_required(group, login_url=None, raise_exception=False):
    """
    Decorator for views that checks whether a user has a group permission,
    redirecting to the log-in page if necessary.
    If the raise_exception parameter is given the PermissionDenied exception
    is raised.
    """
    def check_perms(user):
        if isinstance(group, six.string_types):
            groups = (group, )
        else:
            groups = group
        # First check if the user has the permission (even anon users)

        if user.groups.filter(name__in=groups).exists():
            return True
        # In case the 403 handler should be called raise the exception
        if raise_exception:
            raise PermissionDenied
        # As the last resort, show the login form
        return False
    return user_passes_test(check_perms, login_url='profile')





# def signup(request):
#     if request.method == 'POST':
#         form = UserCreateForm(request.POST)
#         if form.is_valid():
#             user= form.save(commit=False)
#             user.save()
#             return redirect('dashboard')

#     else:
#         form = UserCreateForm()
#     return render(request, 'auth/user_form.html', {'form': form})

def setpassword_message(request):
    return render(request, 'registration/setpassword_message.html')



@login_required
def signup(request):
    a=Group.objects.exclude(name__in=['Company Admin','Company Employee','Company HR'])
    co=Company.objects.all()
    if request.method == 'POST':
        print("hello")
        form = SignUpForm(request.POST)
        if form.is_valid():
            print("hi")
            user= form.save(commit=False)
            user.phone_no = form.cleaned_data.get('phone_no')
            user.is_active = False
            user.save()
            role = form.cleaned_data.get('role')
            group = Group.objects.get(name=role)
            user.groups.add(group)
            current_site = get_current_site(request)
            mail_subject = 'Activate your Account.'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)) ,
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
          
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponseRedirect(reverse('setpassword_message'))
    else:      
        form = SignUpForm()
        
    return render(request, 'registration/user_registration.html', {'form': form,'a':a,'co':co})



@login_required
def company_employee_signup(request,cmp_id):
    compdetail=Company.objects.get(id=cmp_id)

    loc_count=Location.objects.filter(company_id=compdetail.id).count()
    web_count=Website.objects.filter(website_company_name=compdetail.id).count()
    lic_count=Licence.objects.filter(company_id=compdetail.id).count()
    doc_count=Documents.objects.filter(compani_name=compdetail.id).count()
    packs_count=Company_package.objects.filter(companys_name=compdetail.id).count()
    device_count=Device.objects.filter(company_id=compdetail.id).count()
    employee_count=Employee.objects.filter(company_name=compdetail.id).count()



    a=Group.objects.filter(name__in=['Company Admin','Company Employee','Company HR'])
    if request.method == 'POST':
        print("hello")
        form = SignUpForm(request.POST)
        if form.is_valid():
            print("hi")
            user= form.save(commit=False)
            user.phone_no = form.cleaned_data.get('phone_no')
            user.is_active = False            
            user.company_name=Company.objects.get(id=cmp_id)
            user.save()
            role = form.cleaned_data.get('role')
            group = Group.objects.get(name=role)
            user.groups.add(group)
            current_site = get_current_site(request)
            mail_subject = 'Activate your Account.'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)) ,
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
          
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponseRedirect(reverse('setpassword_message'))
    else:      
        form = SignUpForm()
        
    return render(request, 'registration/company_employee_registration.html', {'form': form,'a':a,'compdetail':compdetail,'loc_count':loc_count,'web_count':web_count,'lic_count':lic_count,'doc_count':doc_count,'packs_count':packs_count,'device_count':device_count,'employee_count':employee_count})




def activates(request, uidb64, token, backend='django.contrib.auth.backends.ModelBackend'):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return HttpResponseRedirect(reverse('setpassword',args=(uid,)))
    else:
        return HttpResponse('Activation link is invalid!')


def setpassword(request,uid, backend='django.contrib.auth.backends.ModelBackend'):
    if request.method=='POST':
        form = SetPasswordForm(request.POST)
        if form.is_valid():
            user = User.objects.get(pk=uid)
            password = request.POST.get('password')
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            query_set = Group.objects.filter(user = request.user)
            for g in query_set:
            # this should print all group names for the user
                print(g.id)
                if g.name == "Company Admin": 
                    return redirect('add_employee')
                elif g.name == "Company Employee":
                    return redirect('add_employee')
                elif g.name == "Company HR":
                    return redirect('add_employee')
                else:
                    return redirect('dashboard1')    
    else:
        form = SetPasswordForm()
    return render(request,"passwordset.html",{'form':form})






def add_employee(request):
    userinfo=User.objects.get(username=request.user)
    companyinfo=Company.objects.get(company_name=userinfo.company_name)
    empuser=Employee.objects.create(employee_name=userinfo,phone_number=userinfo.phone_no,employee_email=userinfo.email,company_name=companyinfo)
    empuser.save()

    return HttpResponseRedirect(reverse('dashboard1'))
 

@login_required
def dashboard1(request):
    userinfo=User.objects.get(username=request.user)
    try:
        empinfo=Employee.objects.get(employee_name=userinfo)
        print(empinfo)
    except Employee.DoesNotExist:
        empinfo = None


    query_set = Group.objects.filter(user = request.user)
    for g in query_set:
    # this should print all group names for the user
        print(g.name)
        if g.name == "Company Admin": 
            return HttpResponseRedirect(reverse('company_detail',args=(userinfo.company_name.id,)))       
        elif g.name == "Company Employee":
            return HttpResponseRedirect(reverse('employee_detail',args=(empinfo.id,)))
        elif g.name == "Company HR":
            return HttpResponseRedirect(reverse('employee_detail',args=(empinfo.id,)))
        else:
            return HttpResponseRedirect(reverse('dashboard'))



#@otp_required
@login_required
def index(request):
   
    try:
        a=PhoneDevice.objects.filter(user=request.user)
        if a:
            return render(request, 'myapp/index.html')
        else:
            return render(request, 'myapp/index.html')

    except PhoneDevice.DoesNotExist:
        a = None


@login_required
def profile(request):
    return render(request, 'myapp/profile.html')


@login_required
def calender(request):
    return render(request, 'myapp/page_calender.html')

def login_user(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request,username=username, password=password)          
            if user is not None:
                if user.is_active:
                    login(request, user)    
                    return redirect('/')
                    
    else:
        login_form = LoginForm()
    return render(request, 'registration/login.html', {'login_form': login_form,})


def success(request):
    return render(request, 'myapp/success.html')


@login_required
def profile_account(request):
    password_form = PasswordChangedForm(request.POST)
    profile_form = UserForm(request.POST)
    image_form = ImageForm(request.POST)
    site_form = SiteForm()
    smtp_form = SmtpForm()

    try:
        site_set=SiteConfiguration.objects.get(user=request.user) 
    except SiteConfiguration.DoesNotExist:
        site_set = None

    try:
        smtp_set=SmtpConfiguration.objects.get(user=request.user)
    except SmtpConfiguration.DoesNotExist:
        smtp_set = None

    if request.method == "POST":
        old_password = request.POST.get("old_password")
        if 'btnform2' in request.POST:
            password_form = PasswordChangedForm(request.user, request.POST)
            if request.POST.get("old_password"):
                user = User.objects.get(username= request.user.username)
                if user.check_password('{}'.format(old_password)) == False:
                    password_form.set_old_password_flag()
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Your password was successfully updated!')
                return HttpResponseRedirect(reverse('profile_account'))
            else:
                messages.error(request, 'Please correct the error below.')
        elif 'btnform1' in request.POST:
            profile_form = UserForm(request.POST, instance=request.user)
            if profile_form.is_valid():
                profile_form.save()
        elif 'btnform3' in request.POST:
            image_form = ImageForm(request.POST, request.FILES , instance=request.user)
            if (image_form.is_valid()):
                image_form.save()            
                return HttpResponseRedirect(reverse('profile_account'))
        elif 'btnform4' in request.POST:
            if SiteConfiguration.objects.filter(user=request.user).exists():
                try:
                    site_sett=SiteConfiguration.objects.get(user=request.user) 
                except SiteConfiguration.DoesNotExist:
                    site_sett = None
                site_form = SiteForm(request.POST, request.FILES , instance=site_sett)        
                if site_form.is_valid():
                    site_form.save()            
                    return HttpResponseRedirect(reverse('profile_account'))                     
            else:       
                site_form = SiteForm(request.POST, request.FILES)
                if site_form.is_valid():
                    post = site_form.save(commit=False)
                    post.user = request.user
                    post.save()  
                    messages.success(request, 'Your site settings are successfully added !')
                    return HttpResponseRedirect(reverse('profile_account'))  
    
        elif 'btnform5' in request.POST:
            if SmtpConfiguration.objects.filter(user=request.user).exists(): 
                try:
                    smtp_sett=SmtpConfiguration.objects.get(user=request.user)
                except SmtpConfiguration.DoesNotExist:
                    smtp_sett = None              
                smtp_form = SmtpForm(request.POST, request.FILES , instance=smtp_sett)        
                if smtp_form.is_valid():
                    smtp_form.save()            
                    return HttpResponseRedirect(reverse('profile_account'))                      
            else:       
                smtp_form = SmtpForm(request.POST, request.FILES)
                if smtp_form.is_valid():
                    smtp_post = smtp_form.save(commit=False)
                    smtp_post.user = request.user
                    smtp_post.save()  
                    messages.success(request, 'Your smtp settings are successfully added !')
                    return HttpResponseRedirect(reverse('profile_account'))     
        else:
            raise Http404
    else:
        if SiteConfiguration.objects.filter(user=request.user).exists():
            site_profile_form = SiteForm(instance=SiteConfiguration.objects.get(user=request.user)) 
        elif SmtpConfiguration.objects.filter(user=request.user).exists():
            smtp_form = SmtpForm(instance=SmtpConfiguration.objects.get(user=request.user))        

    return TemplateResponse(request, template="myapp/extra_profile_account.html", context={
        'password_form': password_form,
        'profile_form': profile_form,
        'site_form': site_form,
        'smtp_form': smtp_form,
        'image_form': image_form,
        'site_set':site_set,
        'smtp_set':smtp_set,
    })


def test(request):
  response_str = "false"
  if request.is_ajax():
    old_password = request.GET.get("old_password")
    request_user = User.objects.get(id=request.user.id)
    if(request_user.check_password(old_password) == True):
        response_str = "true"
    return HttpResponse(response_str)



def test_user(request):
    response_str = "true"
    if request.is_ajax():
        username = request.GET.get("username")
        user_exists = User.objects.filter(username=username).exists()
        if (user_exists == True):
            response_str = "false"
        return HttpResponse(response_str)

def test_email(request):
    response_str = "true"
    if request.is_ajax():
        email = request.GET.get("email")
        email_exists = User.objects.filter(email=email).exists()
        print(email_exists)
        if (email_exists == True):
            response_str = "false"
        return HttpResponse(response_str)

def test_phone_no(request):
    response_str = "true"
    if request.is_ajax():
        phone_no = request.GET.get("phone_no")
        phone_no_exists = User.objects.filter(phone_no=phone_no).exists()
        print(phone_no_exists)
        if (phone_no_exists == True):
            response_str = "false"
        return HttpResponse(response_str)

def test_company(request):
    response_str = "true"
    if request.is_ajax():
        company_name = request.GET.get("company_name")
        company_exists = Company.objects.filter(company_name=company_name).exists()
        print(company_exists)
        if (company_exists == True):
            response_str = "false"
        return HttpResponse(response_str)


def test_group(request):
    response_str = "true"
    if request.is_ajax():
        name = request.GET.get("name")
        group_exists = Group.objects.filter(name=name).exists()
        print(group_exists)
        if (group_exists == True):
            response_str = "false"
        return HttpResponse(response_str)


def test_package(request):
    response_str = "true"
    if request.is_ajax():
        name = request.GET.get("name")
        package_exists = Package.objects.filter(name=name).exists()
        print(package_exists)
        if (package_exists == True):
            response_str = "false"
        return HttpResponse(response_str)


def test_location(request):
    response_str = "true"
    if request.is_ajax():
        location_name = request.GET.get("location_name")
        location_exists = Location.objects.filter(location_name=location_name).exists()
        print(location_exists)
        if (location_exists == True):
            response_str = "false"
        return HttpResponse(response_str)



def test_website(request):
    response_str = "true"
    if request.is_ajax():
        website_name = request.GET.get("website_name")
        website_exists = Website.objects.filter(website_name=website_name).exists()
        print(website_exists)
        if (website_exists == True):
            response_str = "false"
        return HttpResponse(response_str)



def test_website_url(request):
    response_str = "true"
    if request.is_ajax():
        website_url = request.GET.get("website_url")
        website_url_exists = Website.objects.filter(website_url=website_url).exists()
        print(website_url_exists)
        if (website_url_exists == True):
            response_str = "false"
        return HttpResponse(response_str)



def test_licence_key(request):
    response_str = "true"
    if request.is_ajax():
        licence_key = request.GET.get("licence_key")
        licence_key_exists = Licence.objects.filter(licence_key=licence_key).exists()
        print(licence_key_exists)
        if (licence_key_exists == True):
            response_str = "false"
        return HttpResponse(response_str)



def test_document(request):
    response_str = "true"
    if request.is_ajax():
        name = request.GET.get("name")
        document_exists = Documents.objects.filter(name=name).exists()
        print(document_exists)
        if (document_exists == True):
            response_str = "false"
        return HttpResponse(response_str)

def test_device_url(request):
    response_str = "true"
    
    if request.is_ajax():
        device_url_address = request.GET.get("device_url_address")
        device_url_exists = Device.objects.filter(device_url_address=device_url_address).exists()
        print(device_url_exists)
        if (device_url_exists == True):
            response_str = "false"
        return HttpResponse(response_str)



@login_required
@user_passes_test(lambda u: u.is_superuser)
@group_required(('HR', 'Admin','Accountant'))
def create_company(request):
    
    if request.method == "POST":
        compform = CompanyForm(request.POST, request.FILES)
        if compform.is_valid():
            compform.save()
            return HttpResponseRedirect(reverse('companyview'))

    else:
        compform = CompanyForm()
    return render(request, 'registration/company_registration.html', {'compform': compform})

# @login_required
# @user_passes_test(lambda u: u.is_superuser)
# @group_required(('HR','Admin'))
# def create_employee(request):
#     com = Company.objects.all()

#     if request.method == "POST":
#         form2 = EmployeeForm(request.POST)
#         if form2.is_valid():
#             print("hello")
#             form2.save()
#             return HttpResponseRedirect(reverse('companyview'))

#     else:
#         form2 = EmployeeForm()
#     return render(request, 'registration/employee_registration.html', {'form2': form2,'com':com})


  
# def user_update(request):
#     return render(request, 'myapp/profile.html')

# def siteupdate(request):
#     if Site.objects.filter(user=username).exists():
#     if request.method == 'POST':
#         site_profile_form = UpdateSiteForm(request.POST, request.FILES , instance=request.user.site)
        
#         if site_profile_form.is_valid():
           
#             site_profile_form.save()            
#             return HttpResponseRedirect(reverse('success'))
        
#     else:
#         site_profile_form = UpdateSiteForm(instance=request.user)
#     return render(request, 'profile_tabs/updatesite.html', {
#         'site_profile_form': site_profile_form,
       
#     })


# @login_required
# def update_profile(request):
#     if request.method == 'POST':
#         user_form = ImageForm(request.POST, request.FILES , instance=request.user)
        
#         if (user_form.is_valid()):
           
#             user_form.save()            
#             return HttpResponseRedirect(reverse('profile_account'))
        
#     else:
#         user_form = ImageForm(instance=request.user)
#     return render(request, 'profile_tabs/change_avtar.html', {
#         'user_form': user_form
#     })


# @login_required
# def user_update(request, template_name='myapp/extra_profile_account.html'):
#     # user= get_object_or_404(User)
#     print("Helloo")
#     fform = UserForm(request.POST, instance=request.user)
#     if fform.is_valid():
#         fform.save()
#         return redirect('profile_account')
#     return render(request, template_name, {'fform':fform})

def companyview(request):
    test_all = Company.objects.all().values('id','company_name', 'description', 'company_website', 'company_address__location_name')
    data={"data": list(test_all)}
    with open('static/company.json', 'w') as f:
        json.dump(data, f, indent=4)
    return redirect('company_view')
   
   
def company_view(request):
    return render(request, 'myapp/company_list.html')


def userview(request):
    test_all = User.objects.all().values('id','first_name','last_name', 'username', 'email', 'phone_no', 'groups__name').exclude(is_superuser=True)
    data={"data": list(test_all)}
    with open('static/user.json', 'w') as f:
        json.dump(data, f, indent=4)
    return redirect('user_view')

def user_view(request):
    return render(request, 'myapp/user_list.html')


def user_delete(request,id):
    print("delete")
    c = User.objects.get(id=id)
    print(c)
    c.delete()    
    messages.success(request, "The user is deleted")  
    return HttpResponseRedirect(reverse('userview'))




def company_detail(request,id):
    # from datetime import datetime
    # now = datetime.today().date()
    # print(now)
    compdetail=Company.objects.get(id=id)

    
    loc_count=Location.objects.filter(company_id=compdetail.id).count()
    web_count=Website.objects.filter(website_company_name=compdetail.id).count()
    lic_count=Licence.objects.filter(company_id=compdetail.id).count()
    doc_count=Documents.objects.filter(compani_name=compdetail.id).count()
    packs_count=Company_package.objects.filter(companys_name=compdetail.id).count()
    device_count=Device.objects.filter(company_id=compdetail.id).count()
    employee_count=Employee.objects.filter(company_name=compdetail.id).count()




    try:
        webs=Website.objects.filter(website_company_name=compdetail.id,is_headquater_website=True)
    except Website.DoesNotExist:
        webs = None        
    try:
        loc=[Location.objects.filter(company_id=compdetail.id,is_headquater=True).latest('id')]
    except Location.DoesNotExist:
        loc = None 
    # logs = LogEntry.objects.select_related().filter(user=request.user) 
    # print(id)
    logs = LogEntry.objects.order_by('-action_time')    
    try:
        loc1=Location.objects.filter(company_id=compdetail.id)
    except Location.DoesNotExist:
        loc1 = None     
    # c=Location.objects.filter(company_id=compdetail.id)
    # print(c)
    # log = LogEntry.objects.select_related().all().order_by("id")            
    return render(request, 'myapp/company_detail.html',{'compdetail':compdetail,'webs':webs,'loc': loc,'loc1':loc1,'logs':logs,'loc_count':loc_count,'web_count':web_count,'lic_count':lic_count,'doc_count':doc_count,'packs_count':packs_count,'device_count':device_count,'employee_count':employee_count})



# def employeeview(request,id):
#     compdetail=Company.objects.get(id=id)
#     test_all = Employee.objects.filter(company_name=compdetail.id).values('id','company_name__company_name','employee_name__username')
#     data={"data": list(test_all)}
#     with open('static/employee.json', 'w') as f:
#         json.dump(data, f, indent=4)
#     return redirect('employee_view')
   
   
# def employee_view(request):
#     return render(request, 'myapp/employee_list.html')



def employeeview(request,id):
    compdetail=Company.objects.get(id=id)


    loc_count=Location.objects.filter(company_id=compdetail.id).count()
    web_count=Website.objects.filter(website_company_name=compdetail.id).count()
    lic_count=Licence.objects.filter(company_id=compdetail.id).count()
    doc_count=Documents.objects.filter(compani_name=compdetail.id).count()
    packs_count=Company_package.objects.filter(companys_name=compdetail.id).count()
    device_count=Device.objects.filter(company_id=compdetail.id).count()
    employee_count=Employee.objects.filter(company_name=compdetail.id).count()


    try:
        employee=Employee.objects.filter(company_name=id)
    except Employee.DoesNotExist:
        employee = None
    return render(request,'myapp/employee_list.html',{'employee':employee,'compdetail':compdetail,'loc_count':loc_count,'web_count':web_count,'lic_count':lic_count,'doc_count':doc_count,'packs_count':packs_count,'device_count':device_count,'employee_count':employee_count})



def employee_detail(request,id): 
    try:
        empdetail=Employee.objects.get(id=id)
    except Employee.DoesNotExist:
        empdetail = None   
    compdetail=Company.objects.get(id=empdetail.company_name.id)


    loc_count=Location.objects.filter(company_id=compdetail.id).count()
    web_count=Website.objects.filter(website_company_name=compdetail.id).count()
    lic_count=Licence.objects.filter(company_id=compdetail.id).count()
    doc_count=Documents.objects.filter(compani_name=compdetail.id).count()
    packs_count=Company_package.objects.filter(companys_name=compdetail.id).count()
    device_count=Device.objects.filter(company_id=compdetail.id).count()
    employee_count=Employee.objects.filter(company_name=compdetail.id).count()
              
    return render(request, 'myapp/employee_detail.html',{'empdetail':empdetail,'compdetail':compdetail,'loc_count':loc_count,'web_count':web_count,'lic_count':lic_count,'doc_count':doc_count,'packs_count':packs_count,'device_count':device_count,'employee_count':employee_count})



# @login_required
# @user_passes_test(lambda u: u.is_superuser)
# @group_required(('HR','Admin'))
# def employee_info(request,id):
#     userinfo=User.objects.get(id=id)
#     print(userinfo.phone_no)
#     if request.method == "POST":
#         empinfo = EmployeeInfoForm(request.POST)
#         if empinfo.is_valid():
#             print("hello")
#             empinfo.save(commit=False)
#             ee.employee_name=userinfo
#             ee.phone_number=userinfo.phone_no
#             ee.employee_email=userinfo.email

#             ee.save()
#             return HttpResponseRedirect(reverse('employee_detail',args=(id,)))

#     else:
#         empinfo = EmployeeInfoForm()
#     return render(request, 'myapp/employee_info.html', {'empinfo': empinfo,'userinfo':userinfo})



def user_update(request,user_id, template_name='myapp/edit_user.html'):
    user=User.objects.get(id=user_id)
    user= get_object_or_404(User,id=user_id)
    print(user.phone_no)
    a=user.groups.all()
    grps=Group.objects.all()
    print("Helloo")
    fform = User_updateForm(request.POST, instance=user)
    if fform.is_valid():
        print("dasfs")
        fform.save()
        return redirect('userview')
    return render(request, template_name, {'fform':fform,'user':user,'a':a,'grps':grps})




def company_update(request, pk, template_name='myapp/edit_company2.html'):
    company= get_object_or_404(Company, pk=pk)
    form = CompanyForm(request.POST or None, request.FILES, instance=company)
    if form.is_valid():
        form.save()
        return redirect('companyview')
    return render(request, template_name, {'form':form, 'company':company})



def company_delete(request,id):
    print("delete")
    b = Company.objects.get(id=id)
    print(b)
    b.delete()     
    return HttpResponseRedirect(reverse('companyview'))

# @login_required
def employee_update(request,empdetail_id):
    employee=Employee.objects.get(id=empdetail_id)
    compdetail=Company.objects.get(id=employee.company_name.id)
    emp=Device.objects.all()


    loc_count=Location.objects.filter(company_id=compdetail.id).count()
    web_count=Website.objects.filter(website_company_name=compdetail.id).count()
    lic_count=Licence.objects.filter(company_id=compdetail.id).count()
    doc_count=Documents.objects.filter(compani_name=compdetail.id).count()
    packs_count=Company_package.objects.filter(companys_name=compdetail.id).count()
    device_count=Device.objects.filter(company_id=compdetail.id).count()
    employee_count=Employee.objects.filter(company_name=compdetail.id).count()
  
    print(employee)
    if request.method == 'POST':
        emp_update_form = UpdateEmployeeInfo(request.POST, instance=employee)
        if (emp_update_form.is_valid()):
            emp_update_form.save()            
            return HttpResponseRedirect(reverse('user_employee_update',args=(empdetail_id,))) 
    else:
        emp_update_form = UpdateEmployeeInfo(instance=employee)
    return render(request, 'registration/employee_update1.html', {

        'emp_update_form': emp_update_form,'employee':employee,'compdetail':compdetail,'loc_count':loc_count,'web_count':web_count,'lic_count':lic_count,'doc_count':doc_count,'packs_count':packs_count,'device_count':device_count,'employee_count':employee_count,'emp':emp

    })


def user_employee_update(request,empdetail_id):
    empuser=Employee.objects.get(id=empdetail_id)
    empuser1=User.objects.get(username=empuser)
    empuser1.phone_no=empuser.phone_number
    empuser1.email=empuser.employee_email
    empuser1.save()
    return HttpResponseRedirect(reverse('employee_detail',args=(empuser.id,)))
 


def employee_delete(request,emp_id):
        employeedelete = Employee.objects.get(id=emp_id)
        useremp=User.objects.get(username=employeedelete)
        useremp.delete()
        return HttpResponseRedirect(reverse('employeeview',args=(employeedelete.company_name.id,)))





def addgroup(request):
    permissions = Permission.objects.all()
    if request.method == 'POST':
        addgroup_form = GroupForm(request.POST)
        if addgroup_form.is_valid:
            name = request.POST.get('name')
            permissions = request.POST.getlist('permissions')
            print(permissions)
            new_group = Group.objects.create(name =name)       
            for z in permissions:   
                new_group.permissions.add(z) 
                new_group.save()
            return HttpResponseRedirect(reverse('groupview')) 

    else:
        addgroup_form = GroupForm()
    return render(request, 'myapp/addgroup.html', {'addgroup_form': addgroup_form,'permissions':permissions})


def groupview(request):
    test_all = Group.objects.all().values('id','name')
    data={"data": list(test_all)}
    with open('static/group.json', 'w') as f:
        json.dump(data, f, indent=4)
    return redirect('group_view')
   
   
def group_view(request):
    return render(request, 'myapp/group_list.html')


def group_detail(request,id):
    groupdetail=Group.objects.get(id=id)
    grpper=groupdetail.permissions.all()
    # grpper1=groupdetail.permissions.all().count()
    # grpper1=grpper1+1
    return render(request, 'myapp/group_detail.html',{'groupdetail':groupdetail,'grpper':grpper})



@login_required
def group_update(request,id):
    permissions = Permission.objects.all()
    groupupdate=Group.objects.get(id=id)
    grppermissions=groupupdate.permissions.all()
    if request.method == 'POST':
        group_form = GroupUpdateForm(request.POST, instance=groupupdate)
        if (group_form.is_valid()):
            group_form.save()            
            return HttpResponseRedirect(reverse('groupview')) 
    else:
        group_form = GroupUpdateForm(instance=groupupdate)
    return render(request, 'myapp/update_group.html', {
        'group_form': group_form,'groupupdate':groupupdate,'permissions':permissions,'grppermissions':grppermissions
    })


def group_delete(request,id):

        b = Group.objects.get(id=id)
        b.delete()    
        messages.success(request, "group is deleted")  
        return HttpResponseRedirect(reverse('groupview'))


# def locationlist(request,cmp_id):
#     compdetail=Company.objects.get(id=cmp_id)
#     test_all = Location.objects.filter(company_id=compdetail).values('id','location_name', 'location_address', 'location_city', 'location_postal_code','countries','location_bussiness_hours','is_headquater','is_off_hours_accessible')
#     print(compdetail.id)
#     data={"data": list(test_all)}
#     with open('static/address.json', 'w') as f:
#         json.dump(data, f, indent=4)
#     return redirect('location_view')

# def location_view(request):
#     return render(request,'myapp/addresslist.html')

def locationn(request,cmp_id):
    loc=Location.objects.filter(company_id=cmp_id)
    compdetail=Company.objects.get(id=cmp_id)

    loc_count=Location.objects.filter(company_id=compdetail.id).count()
    web_count=Website.objects.filter(website_company_name=compdetail.id).count()
    lic_count=Licence.objects.filter(company_id=compdetail.id).count()
    doc_count=Documents.objects.filter(compani_name=compdetail.id).count()
    packs_count=Company_package.objects.filter(companys_name=compdetail.id).count()
    device_count=Device.objects.filter(company_id=compdetail.id).count()
    employee_count=Employee.objects.filter(company_name=compdetail.id).count()
    
    return render(request,'myapp/addresslist.html',{'loc':loc,'compdetail':compdetail,'loc_count':loc_count,'web_count':web_count,'lic_count':lic_count,'doc_count':doc_count,'packs_count':packs_count,'device_count':device_count,'employee_count':employee_count})



def location_detail(request,loc_id):
    loc_detail=Location.objects.get(id=loc_id)
    compdetail=Company.objects.get(id=loc_detail.company_id.id)

    loc_count=Location.objects.filter(company_id=compdetail.id).count()
    web_count=Website.objects.filter(website_company_name=compdetail.id).count()
    lic_count=Licence.objects.filter(company_id=compdetail.id).count()
    doc_count=Documents.objects.filter(compani_name=compdetail.id).count()
    packs_count=Company_package.objects.filter(companys_name=compdetail.id).count()
    device_count=Device.objects.filter(company_id=compdetail.id).count()
    employee_count=Employee.objects.filter(company_name=compdetail.id).count()

    return render(request,'myapp/location_detail.html',{'loc_detail':loc_detail,'compdetail':compdetail,'loc_count':loc_count,'web_count':web_count,'lic_count':lic_count,'doc_count':doc_count,'packs_count':packs_count,'device_count':device_count,'employee_count':employee_count})


def location(request,cmp_id):
    compdetail=Company.objects.get(id=cmp_id)

    loc_count=Location.objects.filter(company_id=compdetail.id).count()
    web_count=Website.objects.filter(website_company_name=compdetail.id).count()
    lic_count=Licence.objects.filter(company_id=compdetail.id).count()
    doc_count=Documents.objects.filter(compani_name=compdetail.id).count()
    packs_count=Company_package.objects.filter(companys_name=compdetail.id).count()
    device_count=Device.objects.filter(company_id=compdetail.id).count()
    employee_count=Employee.objects.filter(company_name=compdetail.id).count()



    try:
        headquater = Location.objects.filter(company_id=cmp_id,is_headquater=True).exists()
        print(headquater)
    except Location.DoesNotExist:
        headquater = None
    countries = Country.objects.all()
    if request.method == 'POST':
        form = LocationForm(request.POST)   
        if form.is_valid():
          a = form.save(commit=False)
          a.company_id = Company.objects.get(pk = cmp_id)
          a.save()
          return HttpResponseRedirect(reverse('locationn',args=(cmp_id,)))
    else:
        form = LocationForm()
    return render(request, 'myapp/location.html', {'form': form,'compdetail':compdetail,'countries':countries,'headquater':headquater,'loc_count':loc_count,'web_count':web_count,'lic_count':lic_count,'doc_count':doc_count,'packs_count':packs_count,'device_count':device_count,'employee_count':employee_count})



def websitee(request,cmp_id):
    compdetail=Company.objects.get(id=cmp_id)

    loc_count=Location.objects.filter(company_id=compdetail.id).count()
    web_count=Website.objects.filter(website_company_name=compdetail.id).count()
    lic_count=Licence.objects.filter(company_id=compdetail.id).count()
    doc_count=Documents.objects.filter(compani_name=compdetail.id).count()
    packs_count=Company_package.objects.filter(companys_name=compdetail.id).count()
    device_count=Device.objects.filter(company_id=compdetail.id).count()
    employee_count=Employee.objects.filter(company_name=compdetail.id).count()

    loc=Website.objects.filter(website_company_name=compdetail.id)    
    return render(request,'myapp/websitelist.html',{'loc':loc,'compdetail':compdetail,'countries':countries,'loc_count':loc_count,'web_count':web_count,'lic_count':lic_count,'doc_count':doc_count,'packs_count':packs_count,'device_count':device_count,'employee_count':employee_count})





def website(request,cmp_id):
    compdetail=Company.objects.get(id=cmp_id)

    loc_count=Location.objects.filter(company_id=compdetail.id).count()
    web_count=Website.objects.filter(website_company_name=compdetail.id).count()
    lic_count=Licence.objects.filter(company_id=compdetail.id).count()
    doc_count=Documents.objects.filter(compani_name=compdetail.id).count()
    packs_count=Company_package.objects.filter(companys_name=compdetail.id).count()
    device_count=Device.objects.filter(company_id=compdetail.id).count()
    employee_count=Employee.objects.filter(company_name=compdetail.id).count()


    try:
        headquater_website = Website.objects.filter(website_company_name=cmp_id,is_headquater_website=True).exists()
        print(headquater_website)
    except Website.DoesNotExist:
        headquater_website = None
    website = WebsiteType.objects.all()
    if request.method == 'POST':
        form = WebsiteForm(request.POST)   
        if form.is_valid():
          a = form.save(commit=False)
          a.website_company_name = Company.objects.get(pk = cmp_id)
          a.save()
          return HttpResponseRedirect(reverse('websitee',args=(cmp_id,)))                 
    else:
        form = WebsiteForm()
    return render(request, 'myapp/website.html', {'form': form,'website':website,'compdetail':compdetail,'headquater_website':headquater_website,'loc_count':loc_count,'web_count':web_count,'lic_count':lic_count,'doc_count':doc_count,'packs_count':packs_count,'device_count':device_count,'employee_count':employee_count})




def website_update(request,cmp_id,w_id):
    compdetail=Company.objects.get(id=cmp_id)

    loc_count=Location.objects.filter(company_id=compdetail.id).count()
    web_count=Website.objects.filter(website_company_name=compdetail.id).count()
    lic_count=Licence.objects.filter(company_id=compdetail.id).count()
    doc_count=Documents.objects.filter(compani_name=compdetail.id).count()
    packs_count=Company_package.objects.filter(companys_name=compdetail.id).count()
    device_count=Device.objects.filter(company_id=compdetail.id).count()
    employee_count=Employee.objects.filter(company_name=compdetail.id).count()

    a = WebsiteType.objects.all()
    webs=Website.objects.get(id=w_id)
    print(webs.id)
    if request.method == 'POST':
        form = Website_UpdateForm(request.POST, instance=webs)
        if (form.is_valid()):
            form.save()            
            return HttpResponseRedirect(reverse('websitee',args=(cmp_id,))) 
    else:
        form = Website_UpdateForm(instance=webs)
    return render(request, 'myapp/website_update.html', {
        'form': form,'webs':webs,'a':a,'compdetail':compdetail,'loc_count':loc_count,'web_count':web_count,'lic_count':lic_count,'doc_count':doc_count,'packs_count':packs_count,'device_count':device_count,'employee_count':employee_count
    })


def website_delete(request,cmp_id,w_id):

        b = Website.objects.get(id=w_id)
        b.delete()    
        messages.success(request, "The user is deleted")  
        return HttpResponseRedirect(reverse('websitee',args=(cmp_id,)))






# @login_required
# @user_passes_test(lambda u: u.is_superuser)
# @group_required(('HR','Admin'))
# def addwebsite(request):
#     web = WebsiteType.objects.all()
#     compp=Company.objects.all()
#     if request.method == "POST":
#         webform = WebsiteForm(request.POST)
#         if webform.is_valid():
#             print("hello")
#             webform.save()
#             return HttpResponseRedirect(reverse('dashboard'))

#     else:
#         webform = WebsiteForm()
#     return render(request, 'myapp/addwebsite.html', {'webform': webform,'web':web,'compp':compp})


def company_location_update(request,location_id):
    countries = Country.objects.all()
    locupdate=Location.objects.get(id=location_id)
    compdetail=Company.objects.get(id=locupdate.company_id.id)

    loc_count=Location.objects.filter(company_id=compdetail.id).count()
    web_count=Website.objects.filter(website_company_name=compdetail.id).count()
    lic_count=Licence.objects.filter(company_id=compdetail.id).count()
    doc_count=Documents.objects.filter(compani_name=compdetail.id).count()
    packs_count=Company_package.objects.filter(companys_name=compdetail.id).count()
    device_count=Device.objects.filter(company_id=compdetail.id).count()
    employee_count=Employee.objects.filter(company_name=compdetail.id).count()

  
    print(locupdate.company_id.id)
    if request.method == 'POST':
        loc_update_form = LocationUpdateForm(request.POST, instance=locupdate)
        if (loc_update_form.is_valid()):
            loc_update_form.save()            
            return HttpResponseRedirect(reverse('locationn',args=(compdetail.id,))) 
    else:
        loc_update_form = LocationUpdateForm(instance=locupdate)
    return render(request, 'myapp/location_update.html', {
        'loc_update_form': loc_update_form,'locupdate':locupdate,'compdetail':compdetail,'countries':countries,'loc_count':loc_count,'web_count':web_count,'lic_count':lic_count,'doc_count':doc_count,'packs_count':packs_count,'device_count':device_count,'employee_count':employee_count
    })





def company_location_delete(request,location_id):

        locdelete = Location.objects.get(id=location_id)
        locdelete.delete()    
        messages.success(request, "location is deleted")  
        return HttpResponseRedirect(reverse('locationn',args=(location_id,)))




def licence(request,cmp_id):
    compdetail=Company.objects.get(id=cmp_id)

    loc_count=Location.objects.filter(company_id=compdetail.id).count()
    web_count=Website.objects.filter(website_company_name=compdetail.id).count()
    lic_count=Licence.objects.filter(company_id=compdetail.id).count()
    doc_count=Documents.objects.filter(compani_name=compdetail.id).count()
    packs_count=Company_package.objects.filter(companys_name=compdetail.id).count()
    device_count=Device.objects.filter(company_id=compdetail.id).count()
    employee_count=Employee.objects.filter(company_name=compdetail.id).count()

    lt=LicenceType.objects.all()
    if request.method == 'POST':
        licence_form = LicenceForm(request.POST)   
        if licence_form.is_valid():
          l = licence_form.save(commit=False)
          l.company_id = Company.objects.get(pk = cmp_id)
          l.save()
          return HttpResponseRedirect(reverse('licencelist',args=(cmp_id,)))
    else:
        licence_form = LicenceForm()
    return render(request, 'myapp/add_licence.html', {'licence_form': licence_form,'lt':lt,'compdetail':compdetail,'loc_count':loc_count,'web_count':web_count,'lic_count':lic_count,'doc_count':doc_count,'packs_count':packs_count,'device_count':device_count,'employee_count':employee_count})


def licencelist(request,cmp_id):
    compdetail=Company.objects.get(id=cmp_id)

    loc_count=Location.objects.filter(company_id=compdetail.id).count()
    web_count=Website.objects.filter(website_company_name=compdetail.id).count()
    lic_count=Licence.objects.filter(company_id=compdetail.id).count()
    doc_count=Documents.objects.filter(compani_name=compdetail.id).count()
    packs_count=Company_package.objects.filter(companys_name=compdetail.id).count()
    device_count=Device.objects.filter(company_id=compdetail.id).count()
    employee_count=Employee.objects.filter(company_name=compdetail.id).count()


    lic=Licence.objects.filter(company_id=cmp_id)
    return render(request,'myapp/licence_list.html',{'lic':lic,'compdetail':compdetail,'loc_count':loc_count,'web_count':web_count,'lic_count':lic_count,'doc_count':doc_count,'packs_count':packs_count,'device_count':device_count,'employee_count':employee_count})



def licence_detail(request,lic_id):
    lic_detail=Licence.objects.get(id=lic_id)
    compdetail=Company.objects.get(id=lic_detail.company_id.id)

    loc_count=Location.objects.filter(company_id=compdetail.id).count()
    web_count=Website.objects.filter(website_company_name=compdetail.id).count()
    lic_count=Licence.objects.filter(company_id=compdetail.id).count()
    doc_count=Documents.objects.filter(compani_name=compdetail.id).count()
    packs_count=Company_package.objects.filter(companys_name=compdetail.id).count()
    device_count=Device.objects.filter(company_id=compdetail.id).count()
    employee_count=Employee.objects.filter(company_name=compdetail.id).count()

    return render(request,'myapp/licence_detail.html',{'lic_detail':lic_detail,'compdetail':compdetail,'loc_count':loc_count,'web_count':web_count,'lic_count':lic_count,'doc_count':doc_count,'packs_count':packs_count,'device_count':device_count,'employee_count':employee_count})


def licence_delete(request,cmp_id,lic_id):

        b = Licence.objects.get(id=lic_id)
        b.delete()    
        messages.success(request, "The user is deleted")  
        return HttpResponseRedirect(reverse('licencelist',args=(cmp_id,)))


def licence_update(request,cmp_id,lic_id):
    compdetail=Company.objects.get(id=cmp_id)

    loc_count=Location.objects.filter(company_id=compdetail.id).count()
    web_count=Website.objects.filter(website_company_name=compdetail.id).count()
    lic_count=Licence.objects.filter(company_id=compdetail.id).count()
    doc_count=Documents.objects.filter(compani_name=compdetail.id).count()
    packs_count=Company_package.objects.filter(companys_name=compdetail.id).count()
    device_count=Device.objects.filter(company_id=compdetail.id).count()
    employee_count=Employee.objects.filter(company_name=compdetail.id).count()

    comp1=Company.objects.filter(id=cmp_id)
    a = LicenceType.objects.all()
    lic=Licence.objects.get(id=lic_id)
    if request.method == 'POST':
        form = Licence_UpdateForm(request.POST, instance=lic)
        if (form.is_valid()):
            form.save()            
            return HttpResponseRedirect(reverse('licencelist',args=(cmp_id,))) 
    else:
        form = Licence_UpdateForm(instance=lic)
    return render(request, 'myapp/licence_update.html', {
        'form': form,'lic':lic,'a':a,'compdetail':compdetail,'comp1':comp1,'loc_count':loc_count,'web_count':web_count,'lic_count':lic_count,'doc_count':doc_count,'packs_count':packs_count,'device_count':device_count,'employee_count':employee_count
    })





def documentss(request,cmp_id):
    compdetail=Company.objects.get(id=cmp_id)
    doc_cat = Document_category.objects.all()
    loc_count=Location.objects.filter(company_id=compdetail.id).count()
    web_count=Website.objects.filter(website_company_name=compdetail.id).count()
    lic_count=Licence.objects.filter(company_id=compdetail.id).count()
    doc_count=Documents.objects.filter(compani_name=compdetail.id).count()
    packs_count=Company_package.objects.filter(companys_name=compdetail.id).count()
    device_count=Device.objects.filter(company_id=compdetail.id).count()
    employee_count=Employee.objects.filter(company_name=compdetail.id).count()

    doc=Documents.objects.filter(compani_name=compdetail.id)
    return render(request,'myapp/documents_list.html',{'doc':doc,'compdetail':compdetail,'loc_count':loc_count,'web_count':web_count,'lic_count':lic_count,'doc_count':doc_count,'packs_count':packs_count,'device_count':device_count,'employee_count':employee_count,'doc_cat':doc_cat})





def documents(request,cmp_id):
    compdetail=Company.objects.get(id=cmp_id)

    loc_count=Location.objects.filter(company_id=compdetail.id).count()
    web_count=Website.objects.filter(website_company_name=compdetail.id).count()
    lic_count=Licence.objects.filter(company_id=compdetail.id).count()
    doc_count=Documents.objects.filter(compani_name=compdetail.id).count()
    packs_count=Company_package.objects.filter(companys_name=compdetail.id).count()
    device_count=Device.objects.filter(company_id=compdetail.id).count()
    employee_count=Employee.objects.filter(company_name=compdetail.id).count()

    b=request.user
    doc = Document_category.objects.all()
    if request.method == 'POST':
        form = DocumentsForm(request.POST, request.FILES)
        print("addsa")
        if form.is_valid():
            print("dasf")
            a = form.save(commit=False)
            a.compani_name = Company.objects.get(pk = cmp_id)
            a.d_by = User.objects.get(pk=b.id)
            a.save()
            return HttpResponseRedirect(reverse('documentss',args=(cmp_id,)))
            
    else:
        form = DocumentsForm()
    return render(request, 'myapp/documents_list.html', {'form': form,'doc':doc,'compdetail':compdetail,'loc_count':loc_count,'web_count':web_count,'lic_count':lic_count,'doc_count':doc_count,'packs_count':packs_count,'device_count':device_count,'employee_count':employee_count}) 



def documents_file(request,doc_id):
    document=Documents.objects.get( id=doc_id)
    compdetail=Company.objects.get(id=document.compani_name.id)

    loc_count=Location.objects.filter(company_id=compdetail.id).count()
    web_count=Website.objects.filter(website_company_name=compdetail.id).count()
    lic_count=Licence.objects.filter(company_id=compdetail.id).count()
    doc_count=Documents.objects.filter(compani_name=compdetail.id).count()
    packs_count=Company_package.objects.filter(companys_name=compdetail.id).count()
    device_count=Device.objects.filter(company_id=compdetail.id).count()
    employee_count=Employee.objects.filter(company_name=compdetail.id).count()

    if request.method == 'POST':
        form = DocumentsFileForm(request.POST, request.FILES)
        print("addsa")
        if form.is_valid():
            files = request.FILES.getlist('file_upload')
            print("dasf")
            for f in files:
                instance = Document_File(document=document, file_upload=f)
                instance.save()
            #     doc = form.save(commit=False)
            # doc.document = Documents.objects.get( id=doc_id)
            # doc.save()
            return HttpResponseRedirect(reverse('document_detail',args=(doc_id,)))          
    else:
        form = DocumentsFileForm()
    return render(request, 'myapp/documents_file.html', {'form': form,'compdetail':compdetail,'loc_count':loc_count,'web_count':web_count,'lic_count':lic_count,'doc_count':doc_count,'packs_count':packs_count,'device_count':device_count,'employee_count':employee_count}) 




def documents_links(request,doc_id):
    document=Documents.objects.get( id=doc_id)
    compdetail=Company.objects.get(id=document.compani_name.id)

    loc_count=Location.objects.filter(company_id=compdetail.id).count()
    web_count=Website.objects.filter(website_company_name=compdetail.id).count()
    lic_count=Licence.objects.filter(company_id=compdetail.id).count()
    doc_count=Documents.objects.filter(compani_name=compdetail.id).count()
    packs_count=Company_package.objects.filter(companys_name=compdetail.id).count()
    device_count=Device.objects.filter(company_id=compdetail.id).count()
    employee_count=Employee.objects.filter(company_name=compdetail.id).count()

    if request.method == 'POST':
        form = DocumentsLinkForm(request.POST)
        print("addsa")
        if form.is_valid():
            print("dasf")
            doc = form.save(commit=False)
            doc.document = Documents.objects.get( id=doc_id)
            doc.save()
            return HttpResponseRedirect(reverse('document_detail',args=(doc_id,)))          
    else:
        form = DocumentsLinkForm()
    return render(request, 'myapp/documents_links.html', {'form': form,'compdetail':compdetail,'loc_count':loc_count,'web_count':web_count,'lic_count':lic_count,'doc_count':doc_count,'packs_count':packs_count,'device_count':device_count,'employee_count':employee_count}) 








def document_update(request,cmp_id,doc_id):
    compdetail=Company.objects.get(id=cmp_id)

    loc_count=Location.objects.filter(company_id=compdetail.id).count()
    web_count=Website.objects.filter(website_company_name=compdetail.id).count()
    lic_count=Licence.objects.filter(company_id=compdetail.id).count()
    doc_count=Documents.objects.filter(compani_name=compdetail.id).count()
    packs_count=Company_package.objects.filter(companys_name=compdetail.id).count()
    device_count=Device.objects.filter(company_id=compdetail.id).count()
    employee_count=Employee.objects.filter(company_name=compdetail.id).count()

    comp1=Company.objects.filter(id=cmp_id)
    doc_category = Document_category.objects.all()
    doc=Documents.objects.get(id=doc_id)
    if request.method == 'POST':
        form = DocumentsUpdateForm(request.POST, request.FILES, instance=doc)
        if (form.is_valid()):
            form.save()            
            return HttpResponseRedirect(reverse('documentss',args=(cmp_id,))) 
    else:
        form = DocumentsUpdateForm(instance=doc)
    return render(request, 'myapp/document_update.html', {
        'form': form,'doc_category':doc_category,'doc':doc,'compdetail':compdetail,'comp1':comp1,'loc_count':loc_count,'web_count':web_count,'lic_count':lic_count,'doc_count':doc_count,'packs_count':packs_count,'device_count':device_count,'employee_count':employee_count
    })




def document_detail(request,doc_id):
    doc_detail=Documents.objects.get(id=doc_id)
    print(doc_detail.id)
    compdetail=Company.objects.get(id=doc_detail.compani_name.id)
 
    files=Document_File.objects.filter(document=doc_detail.id)
    files_exists=Document_File.objects.filter(document=doc_detail.id).exists()

    links=Document_Links.objects.filter(document=doc_detail.id)
    links_exists=Document_Links.objects.filter(document=doc_detail.id).exists()

    loc_count=Location.objects.filter(company_id=compdetail.id).count()
    web_count=Website.objects.filter(website_company_name=compdetail.id).count()
    lic_count=Licence.objects.filter(company_id=compdetail.id).count()
    doc_count=Documents.objects.filter(compani_name=compdetail.id).count()
    packs_count=Company_package.objects.filter(companys_name=compdetail.id).count()
    device_count=Device.objects.filter(company_id=compdetail.id).count()
    employee_count=Employee.objects.filter(company_name=compdetail.id).count()


    url_text=request.build_absolute_uri()
    print(url_text)
    gmail_share_string=quote(url_text)
    print(gmail_share_string)
    share_string=quote(doc_detail.title)
    return render(request,'myapp/document_detail.html',{'doc_detail':doc_detail,'files':files,'files_exists':files_exists,'links':links,'links_exists':links_exists,'compdetail':compdetail,'loc_count':loc_count,'web_count':web_count,'lic_count':lic_count,'doc_count':doc_count,'packs_count':packs_count,'device_count':device_count,'employee_count':employee_count,'gmail_share_string':gmail_share_string,'share_string':share_string})



def documents_delete(request,cmp_id,d_id):

        b = Documents.objects.get(id=d_id)
        b.delete()    
        messages.success(request, "The user is deleted")  
        return HttpResponseRedirect(reverse('documentss',args=(cmp_id,)))


def documents_file_delete(request,file_id):

    doc_file = Document_File.objects.get(id=file_id)
    doc_file.delete() 
    doc_id=doc_file.document.id   
    messages.success(request, "File is deleted")  
    return HttpResponseRedirect(reverse('document_detail',args=(doc_id,)))


def documents_links_delete(request,link_id):

    doc_link = Document_Links.objects.get(id=link_id)
    doc_link.delete() 
    doc_id=doc_link.document.id   
    messages.success(request, "Link is deleted")  
    return HttpResponseRedirect(reverse('document_detail',args=(doc_id,)))





def packages(request):  
    b=request.user
    if request.method == 'POST':
        form = PackageForm(request.POST)
        print("addsa")
        if form.is_valid():
            print("dasf")
            a = form.save(commit=False)
            a.by = User.objects.get(pk=b.id)

            a.save()
            return HttpResponseRedirect(reverse('packagess'))
            
    else:
        form = PackageForm()
    return render(request, 'myapp/addpackage.html', {'form': form,})


def packagess(request):
    pack=Package.objects.all()
    return render(request,'myapp/package_list.html',{'pack':pack,})    


def package_delete(request,p_id):
    b = Package.objects.get(id=p_id)
    if  Company_package.objects.filter(Package_selected=p_id).exists():

        # raise Exception("can not be deleted ")
        # return HttpResponseRedirect(reverse('packagess'))
        # return render_to_response('packagess', message='Save complete')
        messages.success(request, 'Successfully Sent The Message!')
        return HttpResponseRedirect(reverse('packagess'))
    else:
        
        b.delete()    
        messages.success(request, "The user is deleted")  
        return HttpResponseRedirect(reverse('packagess'))


def package_update(request,p_id):
   
    packs=Package.objects.get(id=p_id)
    if request.method == 'POST':
        form = PackageForm(request.POST, instance=packs)
        if (form.is_valid()):
            form.save()            
            return HttpResponseRedirect(reverse('packagess')) 
    else:
        form = PackageForm(instance=packs)
    return render(request, 'myapp/package_update.html', {
        'form': form,'packs':packs,
    })


def package_detail(request,p_id):
    packs=Package.objects.get(id=p_id)
    p=Company_package.objects.filter(Package_selected=p_id).count()
    print(p)
    return render(request,'myapp/package_detail.html',{'packs':packs,'p':p})


def package_list(request,cmp_id):
    compdetail=Company.objects.get(id=cmp_id)
    
    loc_count=Location.objects.filter(company_id=compdetail.id).count()
    web_count=Website.objects.filter(website_company_name=compdetail.id).count()
    lic_count=Licence.objects.filter(company_id=compdetail.id).count()
    doc_count=Documents.objects.filter(compani_name=compdetail.id).count()
    packs_count=Company_package.objects.filter(companys_name=compdetail.id).count()
    device_count=Device.objects.filter(company_id=compdetail.id).count()
    employee_count=Employee.objects.filter(company_name=compdetail.id).count()

    packs=Company_package.objects.filter(companys_name=cmp_id).values('Package_selected')
    print(packs)
    pack=Package.objects.exclude(id__in=packs)
    return render(request,'myapp/company_package.html',{'pack':pack,'compdetail':compdetail,'loc_count':loc_count,'web_count':web_count,'lic_count':lic_count,'doc_count':doc_count,'packs_count':packs_count,'device_count':device_count,'employee_count':employee_count})   




def add_package(request,cmp_id,p_id):
    compdetail=Company.objects.get(id=cmp_id)

    loc_count=Location.objects.filter(company_id=compdetail.id).count()
    web_count=Website.objects.filter(website_company_name=compdetail.id).count()
    lic_count=Licence.objects.filter(company_id=compdetail.id).count()
    doc_count=Documents.objects.filter(compani_name=compdetail.id).count()
    packs_count=Company_package.objects.filter(companys_name=compdetail.id).count()
    device_count=Device.objects.filter(company_id=compdetail.id).count()
    employee_count=Employee.objects.filter(company_name=compdetail.id).count()

    p=Package.objects.get(id=p_id)
    if request.method == 'POST':
        print("dfsfs")
        form = Company_package_Form(request.POST)
        print("addsa")
        if form.is_valid():
            print("dasf")
            a = form.save(commit=False)
            a.save()
            return HttpResponseRedirect(reverse('compack_details',args=(cmp_id,p_id)))            
    else:
        form = Company_package_Form()
    return render(request, 'myapp/add_compackage.html', {'form': form,'p':p,'compdetail':compdetail,'loc_count':loc_count,'web_count':web_count,'lic_count':lic_count,'doc_count':doc_count,'packs_count':packs_count,'device_count':device_count,'employee_count':employee_count})


def compack_details(request,cmp_id,p_id):
    compdetail=Company.objects.get(id=cmp_id)

    loc_count=Location.objects.filter(company_id=compdetail.id).count()
    web_count=Website.objects.filter(website_company_name=compdetail.id).count()
    lic_count=Licence.objects.filter(company_id=compdetail.id).count()
    doc_count=Documents.objects.filter(compani_name=compdetail.id).count()
    packs_count=Company_package.objects.filter(companys_name=compdetail.id).count()
    device_count=Device.objects.filter(company_id=compdetail.id).count()
    employee_count=Employee.objects.filter(company_name=compdetail.id).count()

    packs=Package.objects.get(id=p_id)
    return render(request,'myapp/compack_details.html',{'packs':packs,'compdetail':compdetail,'loc_count':loc_count,'web_count':web_count,'lic_count':lic_count,'doc_count':doc_count,'packs_count':packs_count,'device_count':device_count,'employee_count':employee_count}) 


def list_compack(request,cmp_id):  
    compdetail=Company.objects.get(id=cmp_id) 

    loc_count=Location.objects.filter(company_id=compdetail.id).count()
    web_count=Website.objects.filter(website_company_name=compdetail.id).count()
    lic_count=Licence.objects.filter(company_id=compdetail.id).count()
    doc_count=Documents.objects.filter(compani_name=compdetail.id).count()
    packs_count=Company_package.objects.filter(companys_name=compdetail.id).count()
    device_count=Device.objects.filter(company_id=compdetail.id).count()
    employee_count=Employee.objects.filter(company_name=compdetail.id).count()

    packs=Company_package.objects.filter(companys_name=cmp_id)
    return render(request,'myapp/list_compack.html',{'packs':packs,'compdetail':compdetail,'loc_count':loc_count,'web_count':web_count,'lic_count':lic_count,'doc_count':doc_count,'packs_count':packs_count,'device_count':device_count,'employee_count':employee_count}) 


def compackage_delete(request,cmp_id,p_id):

        b = Company_package.objects.get(id=p_id)
        b.delete()    
        messages.success(request, "The user is deleted")  
        return HttpResponseRedirect(reverse('list_compack',args=(cmp_id,)))    
    
    
def add_device(request,cmp_id):
    compdetail=Company.objects.get(id=cmp_id)

    loc_count=Location.objects.filter(company_id=compdetail.id).count()
    web_count=Website.objects.filter(website_company_name=compdetail.id).count()
    lic_count=Licence.objects.filter(company_id=compdetail.id).count()
    doc_count=Documents.objects.filter(compani_name=compdetail.id).count()
    packs_count=Company_package.objects.filter(companys_name=compdetail.id).count()
    device_count=Device.objects.filter(company_id=compdetail.id).count()
    employee_count=Employee.objects.filter(company_name=compdetail.id).count()

    device_type=DeviceType.objects.all()
    device_location=Location.objects.filter(company_id=cmp_id)
    if request.method == 'POST':
        deviceform = DeviceForm(request.POST)   
        print("ddddd")
        if deviceform.is_valid():
            print("dbjbcks")
            dev = deviceform.save(commit=False)
            dev.company_id = Company.objects.get(id=cmp_id)
            dev.save()
            return HttpResponseRedirect(reverse('device_list',args=(cmp_id,)))                    
    else:
        deviceform = DeviceForm()
    return render(request, 'myapp/add_device.html', {'deviceform': deviceform,'device_type':device_type,'device_location':device_location,'compdetail':compdetail,'loc_count':loc_count,'web_count':web_count,'lic_count':lic_count,'doc_count':doc_count,'packs_count':packs_count,'device_count':device_count,'employee_count':employee_count})


def device_list(request,cmp_id):
    compdetail=Company.objects.get(id=cmp_id)

    loc_count=Location.objects.filter(company_id=compdetail.id).count()
    web_count=Website.objects.filter(website_company_name=compdetail.id).count()
    lic_count=Licence.objects.filter(company_id=compdetail.id).count()
    doc_count=Documents.objects.filter(compani_name=compdetail.id).count()
    packs_count=Company_package.objects.filter(companys_name=compdetail.id).count()
    device_count=Device.objects.filter(company_id=compdetail.id).count()
    employee_count=Employee.objects.filter(company_name=compdetail.id).count()

    try:
        device=Device.objects.filter(company_id=cmp_id)
    except Device.DoesNotExist:
        device = None
    return render(request,'myapp/device_list.html',{'device':device,'compdetail':compdetail,'loc_count':loc_count,'web_count':web_count,'lic_count':lic_count,'doc_count':doc_count,'packs_count':packs_count,'device_count':device_count,'employee_count':employee_count})



def device_detail(request,device_id):
    device_detail=Device.objects.get(id=device_id)
    compdetail=Company.objects.get(id=device_detail.company_id.id)

    loc_count=Location.objects.filter(company_id=compdetail.id).count()
    web_count=Website.objects.filter(website_company_name=compdetail.id).count()
    lic_count=Licence.objects.filter(company_id=compdetail.id).count()
    doc_count=Documents.objects.filter(compani_name=compdetail.id).count()
    packs_count=Company_package.objects.filter(companys_name=compdetail.id).count()
    device_count=Device.objects.filter(company_id=compdetail.id).count()
    employee_count=Employee.objects.filter(company_name=compdetail.id).count()

    return render(request,'myapp/device_detail.html',{'device_detail':device_detail,'compdetail':compdetail,'loc_count':loc_count,'web_count':web_count,'lic_count':lic_count,'doc_count':doc_count,'packs_count':packs_count,'device_count':device_count,'employee_count':employee_count})


def device_delete(request,device_id,cmp_id):
    b = Device.objects.get(id=device_id)
    b.delete()    
    messages.success(request, "The device is deleted")  
    return HttpResponseRedirect(reverse('device_list',args=(cmp_id,)))


def device_update(request,device_id,cmp_id):
    compdetail=Company.objects.get(id=cmp_id)

    loc_count=Location.objects.filter(company_id=compdetail.id).count()
    web_count=Website.objects.filter(website_company_name=compdetail.id).count()
    lic_count=Licence.objects.filter(company_id=compdetail.id).count()
    doc_count=Documents.objects.filter(compani_name=compdetail.id).count()
    packs_count=Company_package.objects.filter(companys_name=compdetail.id).count()
    device_count=Device.objects.filter(company_id=compdetail.id).count()
    employee_count=Employee.objects.filter(company_name=compdetail.id).count()

    comp=Company.objects.filter(id=cmp_id)
    dev=Device.objects.get(id=device_id)
    if request.method == 'POST':
        dev_form = Device_UpdateForm(request.POST, instance=dev)
        if (dev_form.is_valid()):
            dev_form.save()            
            return HttpResponseRedirect(reverse('device_list',args=(cmp_id,))) 
    else:
        dev_form = Device_UpdateForm(instance=dev)
    return render(request, 'myapp/device_update.html', {
        'dev_form': dev_form,'dev':dev,'compdetail':compdetail,'comp':comp,'loc_count':loc_count,'web_count':web_count,'lic_count':lic_count,'doc_count':doc_count,'packs_count':packs_count,'device_count':device_count,'employee_count':employee_count
    })




# def share_doc(request,doc_id):
#     doc_detail=Documents.objects.get(id=doc_id)
#     files=Document_File.objects.filter(document=doc_detail.id)
#     files_exists=Document_File.objects.filter(document=doc_detail.id).exists()
    
#     links=Document_Links.objects.filter(document=doc_detail.id)
#     links_exists=Document_Links.objects.filter(document=doc_detail.id).exists()
#     url_text=request.build_absolute_uri()
#     print(url_text)
#     gmail_share_string=quote(url_text)
#     print(gmail_share_string)
#     share_string=quote(doc_detail.title)
#     return render(request,'myapp/share_doc.html',{'doc_detail':doc_detail,'gmail_share_string':gmail_share_string,'files':files,'share_string':share_string,'files_exists':files_exists,'links':links,'links_exists':links_exists})





def meetings(request,cmp_id):
    compdetail=Company.objects.get(id=cmp_id)  
    by=request.user
    lt=Employee.objects.filter(company_name=cmp_id)
    if request.method == 'POST':
        form = Meeting_Form(request.POST)
        print("addsa")
        if form.is_valid():
            date_time=form.cleaned_data["date_time"]
            time=form.cleaned_data["time"]
            where=form.cleaned_data["where"]
    
            title=form.cleaned_data["title"]
            attendees=form.cleaned_data["attendees"]
            a = form.save(commit=False)
            a.by = User.objects.get(pk=by.id)
            a.company_i = Company.objects.get(id=cmp_id)
            a.save()
            mail_subject = 'Meeting Scheduled'
            message = render_to_string('myapp/email_message.html', {
                'date_time': date_time,
                'time': time,
                'where':where ,
                'title':title,
                'by':by,
                'attendees':attendees
            })
            emailto = [attendee.employee_email for attendee in form.cleaned_data["attendees"]]          
            email = EmailMessage(mail_subject, message, to=emailto)
            email.send()
        return HttpResponseRedirect(reverse('meeting',args=(cmp_id,))) 
            
    else:
        form = Meeting_Form()
    return render(request, 'myapp/meeting.html', {'form': form,'compdetail':compdetail,'lt':lt})






def meeting_list(request,cmp_id):
    compdetail=Company.objects.get(id=cmp_id)  
    meet=Meeting.objects.filter(company_i=compdetail.id)
    return render(request,'myapp/meeting_list.html',{'meet':meet,'compdetail':compdetail})  


  

def meeting_update(request,m_id,cmp_id):
    compdetail=Company.objects.get(id=cmp_id)
    meet=Meeting.objects.get(id=m_id)
    emp1=meet.attendees.values('id')
    emp_id_list = [e["id"] for e in emp1]
    lt=Employee.objects.filter(company_name=cmp_id).exclude(id__in=emp_id_list)
    emp=meet.attendees.all()
    by=request.user
    if request.method == 'POST':
        form = Meeting_Form(request.POST, instance=meet)
        if (form.is_valid()):
            form.save()            
            return HttpResponseRedirect(reverse('meeting',args=(cmp_id,))) 
    else:
        form = Meeting_Form(instance=meet)
    return render(request, 'myapp/meeting_update.html', {
        'form': form,'meet':meet,'compdetail':compdetail,'lt':lt,'emp':emp

    })


def meeting_delete(request,m_id,cmp_id):
    b = Meeting.objects.get(id=m_id)
    b.delete()    
    messages.success(request, "The meeting is deleted")  
    return HttpResponseRedirect(reverse('meeting',args=(cmp_id,)))

def meeting_details(request,m_id,cmp_id):
    compdetail=Company.objects.get(id=cmp_id)
    meet= Meeting.objects.get(id=m_id)
    lt=Meeting.objects.filter(id=meet.id)
    emp=meet.attendees.all()
    return render(request,'myapp/meeting_detail.html',{'meet':meet,'compdetail':compdetail,'lt':lt,'emp':emp})


# class AttendeesAutocomplete(autocomplete.Select2QuerySetView):

#     def get_queryset(self):
#         # Don't forget to filter out results depending on the visitor !
#         # if not self.request.user.is_authenticated():
#         #     return Course.objects.none()
#         print("dsfdff")
#         qs = Employee.objects.all()
#         if self.q:
#             qs = qs.filter(name__istartswith=self.q)
#         return qs  