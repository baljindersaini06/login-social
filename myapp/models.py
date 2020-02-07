from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from activity_log.models import UserMixin
from django_countries.fields import CountryField

from .validators import validate_file_extension,validate_file1_extension



from cities_light.models import Country

EMPLOYEE_TYPE_CHOICES = (
    ('hr', 'HR'),
    ('admin', 'ADMIN'),
    ('accountant', 'ACCOUNTANT'),
    ('sales manager', 'SALES MANAGER')
)



class User(AbstractUser):
    profile_image = models.ImageField(upload_to='images/', default='images/image.jpg')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be upto 10 digits")
    phone_no = models.CharField(validators=[phone_regex], max_length=10, blank=True) 
    company_name = models.ForeignKey('Company', on_delete=models.CASCADE,blank=True, null=True)
    department = models.CharField(max_length=100,null=True,blank=True)
    hr_start_date=models.DateField(blank=True,null=True)
    hr_title=models.CharField(max_length=80,blank=True,null=True)
    ht_birth_date=models.DateField(blank=True,null=True)
    hr_notes=models.CharField(max_length=200,blank=True,null=True)
    hr_emergency_contact_name=models.CharField(max_length=70,blank=True,null=True)
    hr_emergency_contact_relation=models.CharField(max_length=60,blank=True,null=True)
    hr_emergency_conatct_no=models.CharField(validators=[phone_regex],max_length=10,blank=True,null=True)
    last_activity=models.DateTimeField(default=timezone.now, blank=True)


class SiteConfiguration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    site_name = models.CharField(max_length=50,default="")
    site_email = models.EmailField(max_length=50,default="")
    site_favicon = models.ImageField(upload_to='images/',validators=[validate_file_extension],default="")
    site_logo = models.ImageField(upload_to='images/',validators=[validate_file_extension],default="")
    site_address = models.CharField(max_length=200,default="")
    copy_right = models.CharField(max_length=50,default="")

   
    def __str__(self):
        return self.site_name

class SmtpConfiguration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    smtp_email = models.EmailField(max_length=50,default="")
    smtp_password = models.CharField(max_length=50,default="")


    def __str__(self):
        return self.smtp_email

class WebsiteType(models.Model):
    website_type_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.website_type_name



class Website(models.Model):
    website_company_name = models.ForeignKey('Company', on_delete=models.CASCADE, blank=True,null=True)
    website_type = models.ForeignKey(WebsiteType, on_delete=models.CASCADE, blank=True,null=True)
    website_name = models.CharField(max_length=100)
    website_url = models.URLField(max_length = 200)
    is_headquater_website=models.BooleanField(default=False)
    
    def __str__(self):
        return self.website_name

      
class Location(models.Model):
    company_id = models.ForeignKey('Company', on_delete=models.CASCADE,blank=True, null=True)     
    location_name =  models.CharField(max_length=32)
    location_address =  models.CharField(max_length=500)
    location_city =  models.CharField(max_length=32)
    location_postal_code = models.CharField(max_length=6, validators=[RegexValidator(r'^\d{1,10}$')])
    country = models.ForeignKey(Country,on_delete=models.CASCADE,blank=True, null=True)
    location_bussiness_hours = models.CharField(max_length=32)
    is_headquater = models.BooleanField(default=False)
    is_off_hours_accessible = models.BooleanField(default=False)


    def __str__(self):
            return self.location_name



class Company(models.Model):
    company_name = models.CharField(max_length=48)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be upto 10 digits")
    contact_number = models.CharField(validators=[phone_regex], max_length=10, default="")
    description = models.TextField()
    company_website = models.ForeignKey('Website', on_delete=models.CASCADE, blank=True,null=True)
    company_logo = models.ImageField(upload_to='images/', default="")
    company_address = models.ForeignKey('Location', on_delete=models.CASCADE, blank=True,null=True)
    company_map = models.URLField(max_length = 400,default="")
    
    def __str__(self):
        return self.company_name

    
class Employee(models.Model):
    company_name = models.ForeignKey('Company', on_delete=models.CASCADE,blank=True, null=True,related_name='company')
    employee_name = models.ForeignKey('User', on_delete=models.CASCADE, blank=True,null=True,related_name='employee')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be upto 10 digits")
    phone_number = models.CharField(validators=[phone_regex], max_length=10, default="")
    note = models.CharField(max_length=48)
    designation = models.CharField(max_length=32)
    employee_email = models.EmailField()
    workstation = models.ForeignKey('Device', on_delete=models.CASCADE,blank=True, null=True,related_name='workstation')
    def __str__(self):
        return str(self.employee_name)


class Document_category(models.Model):
    name_type = models.CharField(max_length=100)
    def __str__(self):
        return self.name_type


class Documents(models.Model):
    compani_name = models.ForeignKey('Company', on_delete=models.CASCADE,blank=True, null=True,related_name='companie')
    document_category_id = models.ForeignKey('Document_category', on_delete=models.CASCADE, blank=True,null=True)
    date=models.DateTimeField(default=timezone.now, blank=True)
    d_by=models.ForeignKey('User', on_delete=models.CASCADE,blank=True, null=True,related_name='userr')
    name = models.CharField(max_length=48)
    title = models.CharField(max_length=48)
    content = models.CharField(max_length=48)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return 'documents/%s/' % self.name



class Document_File(models.Model):
    document = models.ForeignKey('Documents', on_delete=models.CASCADE)
    file_upload = models.FileField(upload_to='documents/', validators=[validate_file1_extension])

    def __str__(self):
        return str(self.file_upload)

    def get_absolute_url(self):
        return 'document_files/%s/' % self.file_upload




class LicenceType(models.Model):
    licence_type_name = models.CharField(max_length=48)
   
    def __str__(self):
        return self.licence_type_name



class Licence(models.Model):
    licence_type_id = models.ForeignKey('LicenceType', on_delete=models.CASCADE,blank=True, null=True)     
    company_id = models.ForeignKey('Company', on_delete=models.CASCADE,blank=True, null=True)     
    licence_name =  models.CharField(max_length=50)
    licence_quantity =  models.CharField(max_length=500)
    licence_key =  models.CharField(max_length=200)
    aquisition_date = models.DateField()
    activation_date = models.DateField()
    expire_date = models.DateField()
    licence_note=models.CharField(max_length=200)
    
    
    def __str__(self):
            return self.licence_name



class Package(models.Model):
    name= models.CharField(max_length=200)
    description=models.CharField(max_length=200)
    date_time=models.DateTimeField(default=timezone.now, blank=True)
    by=models.ForeignKey('User', on_delete=models.CASCADE,blank=True, null=True,related_name='userrs')
    connectwise_check = models.BooleanField(default=False)
    connectwise_api =models.CharField(max_length=200,blank=True,null=True)
    moneris_check = models.BooleanField(default=False)
    moneris_api=models.CharField(max_length=500,blank=True,null=True)

    def __str__(self):
            return self.name



class Company_package(models.Model):
    companys_name = models.ForeignKey('Company', on_delete=models.CASCADE,blank=True, null=True,related_name='companies')
    Package_selected = models.ForeignKey('Package', on_delete=models.CASCADE,blank=True, null=True)

    def __str__(self):
            return str(self.Package_selected)



class DeviceType(models.Model):
    device_type_name = models.CharField(max_length=48)
   
    def __str__(self):
        return self.device_type_name



class Device(models.Model):
    device_type_id = models.ForeignKey('DeviceType', on_delete=models.CASCADE,blank=True, null=True)     
    company_id = models.ForeignKey('Company', on_delete=models.CASCADE,blank=True, null=True)     
    location_id = models.ForeignKey('Location', on_delete=models.CASCADE,blank=True, null=True)     
    device_name =  models.CharField(max_length=50)
    device_url_address =  models.URLField(max_length = 400,default="")
    device_note=models.CharField(max_length=200)
    device_configuration_id=models.CharField(max_length=200)
    device_configuration_parent_id=models.CharField(max_length=200)

    def __str__(self):
        return self.device_name


