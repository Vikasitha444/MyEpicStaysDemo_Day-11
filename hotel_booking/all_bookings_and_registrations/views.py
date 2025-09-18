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
    Property, Users, Districts, 
    PropertyCategories, PropertyPictures, Excursions,
    PropertyRoomCategories
)




def home(request):
  all_districts = Property.objects.select_related('districtid').all() 
  context = {
      'all_districts': all_districts  
  }
  return render(request, 'home.html',context)




def results(request):
  if request.method == 'POST':  
      destination = request.POST.get('destination', '').strip()
      startDate = request.POST.get('startDate', '').strip()
      endDate = request.POST.get('endDate', '').strip()
      guests = request.POST.get('guests', '').strip()
     
      all_properties  = Property.objects.all()

      #මෙතන, Foreign Key එකක් භාවිතා කරලා, "propertycategory" table එකේ data ලබා ගන්නවා.
      #ඒ සඳහා, select_related() method එක භාවිතා කරනවා.
      # select_related() method එක, Foreign Key relationship එකක් ඇති fields වල data එකතු කරලා, single query එකක් තුළින් ලබා ගන්නා විදිහයි.
      # මෙතන, 'propertycategory' කියලා තියෙන්නේ, Property Table එකේ Foreign Key field එකේ නමයි.
      # ඒ field එක, PropertyCategories model එකට refer කරනවා.
      propertycategory_all_related_tables = Property.objects.select_related('propertycategory').all() 
      all_districts = Property.objects.select_related('districtid').all() 
      
      
      context = {
          'destination': destination,
          'startDate': startDate,
          'endDate': endDate,
          'guests': guests,
          'all_properties': all_properties,
          'propertycategory': propertycategory_all_related_tables
          ,'all_districts': all_districts
          }


      
  
      return render(request, 'results.html',context)
    







   
    
















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
    