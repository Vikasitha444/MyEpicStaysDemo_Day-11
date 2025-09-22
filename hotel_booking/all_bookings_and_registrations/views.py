from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from .models import Member, Teachers  # Import both models
from django.db import transaction
import html
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.db import IntegrityError
from .models import (
    Property, Users, Districts,  PropertyFacilities,
    PropertyCategories, PropertyPictures, Excursions,
    PropertyRoomCategories, PropertyPriceDetails  
)




def home(request):
  all_districts = Districts.objects.all()
  context = {
      'all_districts': all_districts  
  }
  return render(request, 'home.html',context)




def results(request):
    if request.method == 'POST':  
        destination = request.POST.get('destination', '').strip() #මේකේ තියෙන්නේ, form එකෙන් එන, destination කියන field එකේ, value එක. මේකෙන් ගන්නේ, District එකේ ID එක.
        startDate = request.POST.get('startDate', '').strip()
        endDate = request.POST.get('endDate', '').strip()
        guests = request.POST.get('guests', '').strip()
        
        
        #මෙතන, Foreign Key එකක් භාවිතා කරලා, "propertycategory" table එකේ data ලබා ගන්නවා.
        #ඒ සඳහා, select_related() method එක භාවිතා කරනවා.
        # select_related() method එක, Foreign Key relationship එකක් ඇති fields වල data එකතු කරලා, single query එකක් තුළින් ලබා ගන්නා විදිහයි.
        # මෙතන, 'propertycategory' කියලා තියෙන්නේ, Property Table එකේ Foreign Key field එකේ නමයි.
        # ඒ field එක, PropertyCategories model එකට refer කරනවා.
        propertycategory_all_related_tables = Property.objects.select_related('propertycategory').all() 
        
        
        all_districts = Districts.objects.all()
        
        #මේකෙන්, Location එකට පමණක් අදාළ Results Filter කරලා ගන්නවා. 
        all_properties  = Property.objects.select_related('districtid').filter(districtid=destination)
        
        
        property_price_details = PropertyPriceDetails.objects.select_related('propertyid').all()

        
        #අපි හැමෝම දන්නවා නේ, HTML Tempaltes වල පුළුවන්, Data එකක් Display කරන්න 
        # විතරයි.
        # මේ නිසා අපිට, View එකේ, Data ටික Process කරලා, Template එකට යවන්න වෙනවා.        
        #මෙතැනදී කරන්නේ, "home.html" එකෙන්, User තෝරපු Hotel වල විතරක්, 
        # Guest Price එක අරගෙන, ඒක, List එකකට එකතු කරන එක.
        guest_price = []
        for property in all_properties:
            price_record = PropertyPriceDetails.objects.filter(propertyid=property.propertyid).values('guest_price').first()
            if price_record:
                guest_price.append(price_record['guest_price'])
            else:
                guest_price.append(0)  

        #මෙතැනදී, minimum_night_price එක අරගෙන, ඒක, List එකකට එකතු කරන එක.
        minimum_night_price = []
        for property in all_properties:
            price_record = PropertyPriceDetails.objects.filter(propertyid=property.propertyid).values('minimum_night_price').first()
            if price_record:
                minimum_night_price.append(price_record['minimum_night_price'])
            else:
                minimum_night_price.append(0)  

        #ඊට පස්සේ, ඒක Zip එකක් විදිහට එකතු කරලා Template එකට යවනවා.
        properties_with_prices = zip(minimum_night_price, guest_price)






        context = {
            'destination': destination,
            'startDate': startDate,
            'endDate': endDate,
            'guests': guests,
            'all_properties': all_properties,
            'propertycategory': propertycategory_all_related_tables,
            'all_districts': all_districts,
            'properties_with_prices': properties_with_prices
        }


        

        return render(request, 'results.html', context)
    




def info(request):    
    uuid_of_the_clicked_hotel = request.GET.get('id', '').strip()
    
    
    properties = Property.objects.select_related('propertycategory','districtid').filter(uuid = uuid_of_the_clicked_hotel)
    
    
    propertyid_extraction_from_uuid = Property.objects.filter(uuid = uuid_of_the_clicked_hotel).values('propertyid')
    property_facilities = PropertyFacilities.objects.filter(propertyid = propertyid_extraction_from_uuid[0]['propertyid'])
    context = {
        'properties': properties,
        'property_facilities': property_facilities
    }   
    return render(request, 'info.html', context)
    
















# # 01) Insert data into table
#     # Teachers.objects.create(
#     #     reg_no=10,
#     #     name='nimal',
#     #     address='horana',
#     #     gender='male',
#     #     salary=20000,
#     #     subject="ICT"
#     # )

#     # 02) Database එකේ සියලුම විස්තර දර්ශනය කිරීම
#     Teachers_Table = Teachers.objects.all()

#     # 03) හොරණ ජිවත් වන ගුරුවරුන්ගේ, ගුරු අංකය හා විෂය ලබා ගැනීම
#     horana_teachers = Teachers.objects.filter(address='horana').values('reg_no', 'subject', 'name')

#     # 04) ගම්පහ නොවන වෙනත් ප්‍රදේශ වල ජිවත් වන ගුරුවරුන්ගේ නම හා ලිපිනය තෝරා ගැනීම
#     non_gampaha_teachers = Teachers.objects.exclude(address='gampaha').values('name', 'address')
    
#     # 05) වැටුප 25,000 ට වැඩි ගුරුවරුන්ගේ, ගුරු අංකය, නම, විෂය හා වැටුප තේරීම
#     high_salary_teachers = Teachers.objects.filter(salary__gt=25000).values('reg_no', 'name', 'subject', 'salary')

#     # 06) kaluගේ ලිපිනය කළුතර බවට වෙනස් කිරීම
#     try:
#         teacher = Teachers.objects.get(name='kalu')
#         teacher.address = 'kaluthara'
#         teacher.save()
#         update_status = "Updated successfully"
#     except Teachers.DoesNotExist:
#         update_status = "Teacher 'kalu' not found"

#     # 07) වැටුප 25,000ට අඩු ගුරුවරුන්ගේ සියලුම දත්ත මැකීම
#     teachers_to_delete = Teachers.objects.filter(salary__lt=25000).delete()
    