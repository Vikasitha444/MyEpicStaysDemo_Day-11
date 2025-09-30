from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from .models import Member, Teachers  # Import both models
from django.db import transaction
from datetime import datetime
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

        
        



        #මෙතැනදී, කරලා තියෙන්නේ, Total Price එක හොයන එක
        #"Total Price = (minimum_night_price × Nights ) + Additional Guest Prices" කියන සුත්‍රය තමා මේකට භාවිතා කරන්නේ
        #එක් එක්, Hotel එකේ, Price එක ගබඩා කිරීමට, "total_price" කියලා List එකක් හැදුවා
        total_price = []
        number_of_nights = 0
        additional_guests_chages = 0
        for property in all_properties:
            additional_guests_price = PropertyPriceDetails.objects.filter(propertyid=property.propertyid).values('additional_guest_price').first()['additional_guest_price']
            minimum_night_price = PropertyPriceDetails.objects.filter(propertyid=property.propertyid).values('minimum_night_price').first()['minimum_night_price']
            
            #මෙතැනදී කරලා තියෙන්නේ, හෝටලේ අවශ්‍ය දවස් ගාන හොයාගන්න එක
            date_gap = datetime.strptime(endDate, '%Y-%m-%d') - datetime.strptime(startDate, '%Y-%m-%d')
            number_of_nights = date_gap.days

            #Guessලා ගාන 02ට වඩා වැඩි නම්, Additional Chages ගණනය කරයි.
            if int(guests) > 2:
                additional_guests = int(guests) - 2 #වැඩි Guessලා Count එක හොයාගන්නවා
                additional_guests_chages = additional_guests * int(additional_guests_price) # "Additional guests Amount * Additional guest's price" මේ සුත්‍රය තමා මෙතන භාවිතා වෙන්නේ.
            else:   
                additional_guests_chages = 0
            #මෙතැනදී, Total price එක ලැබෙනවා
            total_price.append((minimum_night_price * number_of_nights) + additional_guests_chages)

        properties_with_prices = total_price
        print(properties_with_prices)

        
        #මෙතැනදී, ලේසි වෙන්න, total_price එකයි,  "all_properties" ටිකයි, එකක් විදිහට එකතු කරලා, Template එකට යවනවා.
        all_in_one = zip(total_price,all_properties)

        #Zip object එක, එයාට පාරක් විතරයි iterate වෙන්න පුළුවන්
        #ඒ නිසා, ආයේ Property Details, Zip object එකක් විදිහට හැදුවා Map එකට දෙන්න.
        all_in_one_for_map = zip(total_price,all_properties)

        context = {
            'destination': destination,
            'startDate': startDate,
            'endDate': endDate,
            'guests': guests,
            'all_properties': all_properties,
            'propertycategory': propertycategory_all_related_tables,
            'all_districts': all_districts,
            'properties_with_prices': properties_with_prices,
            'number_of_nights': number_of_nights, # මේකෙන්, Nights ගණන Template එකට යවනවා, මොකද, ආයේ ඒ Value එක "info.html" එකේ ගණනය කරන්න ඕනෙ නිසා.
            'all_in_one': all_in_one,
            'all_in_one_for_map': all_in_one_for_map
        }


        

        return render(request, 'results.html', context)
    




def info(request):    
    uuid_of_the_clicked_hotel = request.GET.get('id', '').strip()
    nights = request.GET.get('nights', '').strip()
    guests = request.GET.get('guests', '').strip()
    
    
    properties = Property.objects.select_related('propertycategory','districtid').filter(uuid = uuid_of_the_clicked_hotel)
    
    
    propertyid_extraction_from_uuid = Property.objects.filter(uuid = uuid_of_the_clicked_hotel).values('propertyid')
    property_facilities = PropertyFacilities.objects.filter(propertyid = propertyid_extraction_from_uuid[0]['propertyid'])
    
    #මේකෙදි, "propertyid_extraction_from_uuid" value එක Int එකක් කරනවා.
    propertyid_extraction_from_uuid = int(propertyid_extraction_from_uuid[0]['propertyid'])
    

    minimum_night_price = PropertyPriceDetails.objects.filter(propertyid=propertyid_extraction_from_uuid).values('minimum_night_price').first()['minimum_night_price']
    additional_guests_price = PropertyPriceDetails.objects.filter(propertyid=propertyid_extraction_from_uuid).values('additional_guest_price').first()['additional_guest_price']

    

    #මෙතැනදී, කරලා තියෙන්නේ, Total Price එක හොයන එක
    #"Total Price = (minimum_night_price × Nights ) + Additional Guest Prices" කියන සුත්‍රය තමා මේකට භාවිතා කරන්නේ
    #ආයේ ගාන මෙතන හැදුවා, GET Methords වලින් යවලා Security එක අඩු වෙන නිසා
    total_price = 0
    number_of_nights = 0
    additional_guests_chages = 0
    if int(guests) > 2: 
        additional_guests = int(guests) - 2 #වැඩි Guessලා Count එක හොයාගන්නවා
        additional_guests_chages = additional_guests * int(additional_guests_price) # "Additional guests Amount * Additional guest's price" මේ සුත්‍රය තමා මෙතන භාවිතා වෙන්නේ.  
        total_price = (minimum_night_price * int(nights)) + additional_guests_chages
    else:   
        total_price = (minimum_night_price * int(nights)) + 0
    


    context = {
        'properties': properties,
        'property_facilities': property_facilities,
        'minimum_night_price': minimum_night_price,
        'additional_guests_chages': additional_guests_chages,
        'nights': nights,
        'total_price': total_price,
        'guests': guests,
        'additional_guests_price': additional_guests_price
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
    