from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns=[
    #path('signup',views.signup,name='signup'),
    path('dashboard', views.index, name='dashboard'),
    path('',views.dashboard1,name='dashboard1'),
    path('setpassword_message',views.setpassword_message,name='setpassword_message'),

    path('success',views.success,name='success'),
    path('profile', views.profile, name='profile'),
    path('page_calender', views.calender, name='page_calender'),
    path('profile_account', views.profile_account, name='profile_account'),
    #path('siteupdate',views.siteupdate,name='siteupdate'),
    #path('editprofile',views.update_profile,name='editprofile'),
    #path('change_password', views.change_password, name='change_password'),
    #path('userclient',views.user_update, name='userclient'),
    path('test',views.test, name='test'),
    path('test_user',views.test_user, name='test_user'),
    path('test_email',views.test_email, name='test_email'),
    path('test_phone_no',views.test_phone_no, name='test_phone_no'),
    path('test_company',views.test_company, name='test_company'),
    path('test_group',views.test_group, name='test_group'),
    path('test_package',views.test_package, name='test_package'),
    path('test_location',views.test_location, name='test_location'),
    path('test_website',views.test_website, name='test_website'),
    path('test_website_url',views.test_website_url, name='test_website_url'),
    path('test_licence_key',views.test_licence_key, name='test_licence_key'),
    path('test_document',views.test_document, name='test_document'),
    path('test_device_url',views.test_device_url, name='test_device_url'),
    path('test_meeting',views.test_meeting, name='test_meeting'),


    #path('user_registration', views.userre, name='user_registration'),
    path('company_registration', views.create_company, name='company_registration'),
    path('company_employee_signup/<int:cmp_id>/', views.company_employee_signup, name='company_employee_signup'),
    path('user', views.signup, name='user'),
    path('activates/<uidb64>/<token>/',views.activates, name='activates'),
    path('setpassword/<int:uid>',views.setpassword,name='setpassword'),
    path('add_employee',views.add_employee,name='add_employee'),
    path('companyview',views.companyview,name='companyview'),

    path('company_view',views.company_view,name='company_view'),
    path('company_detail/<int:id>/',views.company_detail,name='company_detail'),
    path('employeeview/<int:id>/',views.employeeview,name='employeeview'),
    # path('employee_view',views.employee_view,name='employee_view'),
    path('employee_detail/<int:id>/',views.employee_detail,name='employee_detail'),
    path('updatecompany/<int:pk>',views.company_update, name='updatecompany'),
    path('deletecompany', views.company_delete, name='deletecompany'),
    path('companydelete/<int:id>/',views.company_delete,name='companydelete'),
    path('userview',views.userview,name='userview'),
    path('user_view',views.user_view,name='user_view'),
    path('employee_delete/<int:emp_id>/<int:cmp_id>/',views.employee_delete,name='employee_delete'),
    # path('employee_employee_delete/<int:e_id>/',views.employee_employee_delete,name='employee_employee_delete'),

    path('addgroup',views.addgroup,name='addgroup'),
    path('groupview',views.groupview,name='groupview'),
    path('group_view',views.group_view,name='group_view'),
    path('group_detail/<int:id>/',views.group_detail,name='group_detail'),
    path('user_delete/<int:id>', views.user_delete, name='user_delete'),
    path('group_update/<int:id>',views.group_update,name='group_update'),
    path('group_delete/<int:id>',views.group_delete,name='group_delete'),
    path('user_update/<int:user_id>',views.user_update,name='user_update'),
    path('location/<int:cmp_id>/',views.location,name='location'),
    # path('locationlist/<int:cmp_id>/',views.locationlist,name='locationlist'),
    # path('location_view/',views.location_view,name='location_view'),
    path('website/<int:cmp_id>/',views.website,name='website'),
    # path('employee_info/<int:id>/',views.employee_info,name='employee_info'),
    path('employee_update/<int:empdetail_id>/',views.employee_update,name='employee_update'),
    path('user_employee_update/<int:empdetail_id>/',views.user_employee_update,name='user_employee_update'),
    path('locationn/<int:cmp_id>/',views.locationn,name='locationn'),
    path('location_detail/<int:loc_id>',views.location_detail,name='location_detail'),

    path('company_location_update/<int:location_id>',views.company_location_update,name='company_location_update'),
    path('company_location_delete/<int:location_id>',views.company_location_delete,name='company_location_delete'),
    path('employee_delete/<int:emp_id>/',views.employee_delete,name='employee_delete'),

    path('websitee/<int:cmp_id>/',views.websitee,name='websitee'),
    path('website_update/<int:cmp_id>/<int:w_id>/',views.website_update,name='website_update'),
    path('website_delete/<int:cmp_id>/<int:w_id>',views.website_delete,name='website_delete'),

    
    path('licence/<int:cmp_id>/',views.licence,name='licence'),
    path('licencelist/<int:cmp_id>/',views.licencelist,name='licencelist'),
    path('licence_detail/<int:lic_id>/',views.licence_detail,name='licence_detail'),
    path('licence_delete/<int:cmp_id>/<int:lic_id>/',views.licence_delete,name='licence_delete'),
    path('licence_update/<int:cmp_id>/<int:lic_id>/',views.licence_update,name='licence_update'),

    path('documents/<int:cmp_id>/',views.documents,name='documents'),
    path('documentss/<int:cmp_id>/',views.documentss,name='documentss'),
    path('documents_delete/<int:cmp_id>/<int:d_id>',views.documents_delete,name='documents_delete'),
    path('document_update/<int:cmp_id>/<int:doc_id>',views.document_update,name='document_update'),
    path('document_detail/<int:doc_id>/',views.document_detail,name='document_detail'),
    path('documents_file/<int:doc_id>/',views.documents_file,name='documents_file'),
    path('documents_file_delete/<int:file_id>/',views.documents_file_delete,name='documents_file_delete'),
    path('documents_links/<int:doc_id>/',views.documents_links,name='documents_links'),
    path('documents_links_delete/<int:link_id>/',views.documents_links_delete,name='documents_links_delete'),



    path('packages/',views.packages,name='addpackage'),
    path('packagess/',views.packagess,name='packagess'),
    path('packages_delete/<int:p_id>',views.package_delete,name='package_delete'),
    path('packages_update/<int:p_id>',views.package_update,name='package_update'),
    path('packages_details/<int:p_id>',views.package_detail,name='package_detail'),


    path('comapny_packages/<int:cmp_id>',views.package_list,name='package_list'),
    path('add_package/<int:cmp_id>/<int:p_id>',views.add_package,name='add_package'),
    path('compack_details/<int:cmp_id>/<int:p_id>',views.compack_details,name='compack_details'),
    path('list_compack/<int:cmp_id>',views.list_compack,name='list_compack'),
    path('compackage_delete/<int:cmp_id>/<int:p_id>',views.compackage_delete,name='compackage_delete'),

    path('add_device/<int:cmp_id>/',views.add_device,name='add_device'),
    path('device_list/<int:cmp_id>/',views.device_list,name='device_list'),
    path('device_detail/<int:device_id>/',views.device_detail,name='device_detail'),
    path('device_delete/<int:device_id>/<int:cmp_id>/',views.device_delete,name='device_delete'),
    path('device_update/<int:device_id>/<int:cmp_id>/',views.device_update,name='device_update'),

    # path('share_doc/<int:doc_id>/',views.share_doc,name='share_doc'),
   
    path('meetings/<int:cmp_id>/',views.meetings,name='meetings'),
    path('meeting_list/<int:cmp_id>/',views.meeting_list,name='meeting'),
    path('meeting_update/<int:m_id>/<int:cmp_id>',views.meeting_update,name='meeting_update'),
    path('meeting_delete/<int:m_id>/<int:cmp_id>',views.meeting_delete,name='meeting_delete'),
    path('meeting_details/<int:m_id>/<int:cmp_id>',views.meeting_details,name='meeting_details'),

    path('generate_meeting_pdf/<int:m_id>',views.generate_meeting_pdf,name='generate_meeting_pdf'),
    path('employee_meetings/<int:id>',views.employee_meeting,name='employee_meetings'),
    path('employee_meeting_details/<int:m_id>/<int:id>',views.employee_meeting_details,name='employee_meeting_details'),









]