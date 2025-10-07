from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from .models import Member, Teachers  # Import both models
from django.db import transaction
from datetime import datetime
import html
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.db import IntegrityError
from django.contrib import messages
import uuid
from .models import (
    Property, Users, Districts,  PropertyFacilities,
    PropertyCategories, PropertyPictures, Excursions,
    PropertyRoomCategories, PropertyPriceDetails,
    PropertyPictures 
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



        #මෙතැනදී, කරලා තියෙන්නේ, Property Pictures එක ගන්න එක
        property_pictures = []
        for property in all_properties:
            property_pictures.append(PropertyPictures.objects.filter(propertyid=property.propertyid).values('picture').first()['picture'])

        #මෙතැනදී, ලේසි වෙන්න, total_price එකයි,  "all_properties" ටිකයි, එකක් විදිහට එකතු කරලා, Template එකට යවනවා.
        all_in_one = zip(total_price,all_properties,property_pictures)

        #Zip object එක, එයාට පාරක් විතරයි iterate වෙන්න පුළුවන්
        #ඒ නිසා, ආයේ Property Details, Zip object එකක් විදිහට හැදුවා Map එකට දෙන්න.
        all_in_one_for_map = zip(total_price,all_properties,property_pictures)


        
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
            'all_in_one_for_map': all_in_one_for_map,
            
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
    

    property_pictures = PropertyPictures.objects.filter(propertyid=propertyid_extraction_from_uuid).first()
    


    context = {
        'properties': properties,
        'property_facilities': property_facilities,
        'minimum_night_price': minimum_night_price,
        'additional_guests_chages': additional_guests_chages,
        'nights': nights,
        'total_price': total_price,
        'guests': guests,
        'additional_guests_price': additional_guests_price,
        'property_pictures': property_pictures,
    }   
    return render(request, 'info.html', context)
    







def register_hotel(request):

    if request.method == 'POST':
        try:
            # Get form data - Basic Information
            title = request.POST.get('title')
            shortdescription = request.POST.get('shortdescription')
            longdescription = request.POST.get('longdescription')
            propertycategory_id = request.POST.get('propertycategory')
            districtid = request.POST.get('districtid')
            address = request.POST.get('address')
            googlemappin = request.POST.get('googlemappin', '')
            
            # Get image URLs from form
            main_picture = request.POST.get('main_picture')
            bedareaimage = request.POST.get('bedareaimage')
            diningareaimage = request.POST.get('diningareaimage')
            bathroomimage = request.POST.get('bathroomimage')
            roominteriorimage = request.POST.get('roominteriorimage')
            poolareaimage = request.POST.get('poolareaimage')
            picture_title = request.POST.get('picture_title', 'Property Images')
            picture_description = request.POST.get('picture_description', '')
            
            # Get selected facilities from checkboxes
            selected_facilities = request.POST.getlist('facilities')
            
            # Get price details
            minimum_night_price = request.POST.get('minimum_night_price')
            additional_guest_price = request.POST.get('additional_guest_price')
            
            # Facility details mapping (iconid එක හා title එක)
            facility_details = {
                '201': 'Swimming Pool',
                '202': 'Spa & Wellness',
                '203': 'Free WiFi',
                '204': 'Business Center',
                '205': 'Private Beach',
                '206': 'Golf Course',
                '207': 'Kids Club',
                '208': 'Tea Tasting',
                '209': 'Wildlife Safari',
                '210': 'Historic Tours'
            }
            
            # Validate required fields
            if not all([title, shortdescription, longdescription, propertycategory_id, 
                       districtid, address, main_picture, bedareaimage, diningareaimage, 
                       bathroomimage, roominteriorimage, poolareaimage, 
                       minimum_night_price, additional_guest_price]):
                messages.error(request, 'Please fill all required fields!')
                return redirect('register_hotel')
            
            # Validate at least one facility is selected
            if len(selected_facilities) == 0:
                messages.error(request, 'Please select at least one facility!')
                return redirect('register_hotel')
            
            # Validate price values
            try:
                minimum_night_price = int(minimum_night_price)
                additional_guest_price = int(additional_guest_price)
                
                if minimum_night_price <= 0 or additional_guest_price < 0:
                    messages.error(request, 'Prices must be positive numbers!')
                    return redirect('register_hotel')
            except ValueError:
                messages.error(request, 'Invalid price values!')
                return redirect('register_hotel')
            
            # Create new property
            property = Property.objects.create(
                title=title,
                shortdescription=shortdescription,
                longdescription=longdescription,
                propertycategory_id=propertycategory_id,
                districtid_id=districtid,
                address=address,
                googlemappin=googlemappin if googlemappin else None,
                defaultpictureid=None,
                verified='N',
                enabled='Y',
                verifiedby=None,
                verifiedtimestamp=None,
                verifiednotes=None,
                nextverification=None,
                uuid=uuid.uuid4()
            )
            
            # Save property pictures to propertypicture table
            property_picture = PropertyPictures.objects.create(
                propertyid=property,  # Foreign Key
                title=picture_title,
                picture=main_picture,
                description=picture_description,
                bedareaimage=bedareaimage,
                diningareaimage=diningareaimage,
                bathroomimage=bathroomimage,
                roominteriorimage=roominteriorimage,
                poolareaimage=poolareaimage
            )
            
            # Save property price details to property_price_details table
            PropertyPriceDetails.objects.create(
                propertyid=property,  # Foreign Key
                minimum_night_price=minimum_night_price,
                additional_guest_price=additional_guest_price
            )
            
            # Save selected facilities to propertyfacilities table
            for iconid in selected_facilities:
                facility_title = facility_details.get(iconid, 'Unknown Facility')
                
                PropertyFacilities.objects.create(
                    propertyid=property,  # Foreign Key
                    title=facility_title,
                    iconid=int(iconid),
                    description='',  # Empty description
                    propertypictureid=property_picture.propertypictureid,
                    sizedimentiondetails=''  # Empty size details
                )
            
            # Success message
            messages.success(request, 
                f'Property "{title}" with {len(selected_facilities)} facilities and pricing details have been successfully saved!')
            
            return redirect('register_hotel')
            
        except Exception as e:
            messages.error(request, f'Database Error: {str(e)}')
            return redirect('register_hotel')
    
    # GET request - show form
    all_districts = Districts.objects.all()
    propertycategory_all_related_tables = PropertyCategories.objects.all()
    
    context = {
        'all_districts': all_districts,
        'propertycategory': propertycategory_all_related_tables
    }
    return render(request, 'register_hotel.html', context)






def delete_hotel(request):
    search_query = request.GET.get('search_query', '').strip()
    
    # Handle DELETE request
    if request.method == 'POST':
        property_id = request.POST.get('property_id')
        
        try:
            property = Property.objects.get(propertyid=property_id)
            property_title = property.title
            
            # Delete property (cascade delete will handle related records)
            property.delete()
            
            messages.success(request, f'Property "{property_title}" (ID: {property_id}) has been successfully deleted!')
            return redirect('delete_hotel')
            
        except Property.DoesNotExist:
            messages.error(request, f'Property with ID {property_id} does not exist!')
            return redirect('delete_hotel')
        except Exception as e:
            messages.error(request, f'Error deleting property: {str(e)}')
            return redirect('delete_hotel')
    
    # Handle GET request (display properties)
    if search_query:
        # Search by title or property ID
        try:
            # Try to search by ID first
            property_id = int(search_query)
            properties = Property.objects.select_related('propertycategory', 'districtid').filter(propertyid=property_id)
        except ValueError:
            # If not a number, search by title
            properties = Property.objects.select_related('propertycategory', 'districtid').filter(
                title__icontains=search_query
            )
    else:
        properties = None
    
    # Get all properties for display when not searching
    all_properties = Property.objects.select_related('propertycategory', 'districtid').all()
    
    context = {
        'properties': properties,
        'all_properties': all_properties,
        'search_query': search_query
    }
    
    return render(request, 'delete_hotel.html', context)



def check_hotel_criteria(hotel_name, min_occurrences=5):
    """
    Hotel නම web එකේ search කරලා එය කී වතාවක් පෙන්වනවාද check කරනවා
    Returns: True if criteria met, False otherwise
    """

    def normalize_text(text):
        """Text එක lowercase කරලා extra spaces remove කරනවා"""
        return ' '.join(text.lower().split())

    def is_similar(text1, text2, threshold=0.8):
        """දෙක texts එක්ක similar ද කියලා check කරනවා"""
        norm1 = normalize_text(text1)
        norm2 = normalize_text(text2)

        if norm1 == norm2:
            return True

        if norm1 in norm2 or norm2 in norm1:
            return True

        similarity = SequenceMatcher(None, norm1, norm2).ratio()
        return similarity >= threshold

    print(f"🔍 '{hotel_name}' සඳහා search කරනවා...\n")

    try:
        results = DDGS().text(hotel_name, max_results=10)

        if not results:
            print("❌ Search results හම්බ වෙන්නේ නැහැ!")
            return False

        count = 0
        matched_items = []

        for i, result in enumerate(results, 1):
            title = result.get('title', '')
            body = result.get('body', '')
            url = result.get('href', '')

            title_match = is_similar(hotel_name, title, threshold=0.7)
            body_match = hotel_name.lower() in body.lower()

            if title_match or body_match:
                count += 1
                matched_items.append({
                    'index': i,
                    'title': title,
                    'url': url,
                    'matched_in': 'Title' if title_match else 'Body'
                })

        print("📊 Search Results:\n" + "="*80)
        for item in matched_items:
            print(f"{item['index']}. ✅ {item['title']}")
            print(f"   🔗 {item['url']}")
            print(f"   📍 Matched in: {item['matched_in']}\n")

        print("="*80)
        print(f"\n📈 Summary:")
        print(f"   Hotel නම '{hotel_name}' පෙන්වුණු වාර ගණන: {count}/10")

        if count > min_occurrences:
            print(f"\n✅ ✅ ✅ CRITERIA 1 HAS DONE! ✅ ✅ ✅")
            print(f"   (Hotel නම {count} වතාවක් හම්බ වුණා, අවශ්‍ය වුණේ >{min_occurrences})")
            return True
        else:
            print(f"\n❌ Criteria 1 NOT met.")
            print(f"   (Hotel නම {count} වතාවක් විතරයි හම්බ වුණේ, අවශ්‍ය >{min_occurrences})")
            return False

    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")
        return False