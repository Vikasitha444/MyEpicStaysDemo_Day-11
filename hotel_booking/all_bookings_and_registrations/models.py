# all_bookings_and_registrations/models.py
#Table එක manually හදාගෙන තියෙනවා කියලා Django ට කියන්න තමා mange=False කියලා දාන්නෙ

from django.db import models

class AwardAuthorities(models.Model):
    id = models.BigAutoField(primary_key=True)
    authority_name = models.CharField(max_length=255)
    url = models.URLField()
    description = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False  # Don't let Django manage this existing table
        db_table = 'award_authorities'

class Districts(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'districts'

class ExcursionMedia(models.Model):
    id = models.BigAutoField(primary_key=True)
    excursion_id = models.BigIntegerField()
    media_type = models.CharField(max_length=255)
    media_url = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField()
    display_order = models.IntegerField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'excursion_media'

class Excursions(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    long_description = models.TextField()
    google_location_pin = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_hours = models.IntegerField()
    max_participants = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'excursions'

class Icons(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    short_description = models.CharField(max_length=255)
    icon_path = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'icons'

# class Notifications(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     message = models.TextField()
#     notification_type = models.CharField(max_length=255)
#     target_user = models.CharField(max_length=255)
#     is_read = models.BooleanField()
#     created_at = models.DateTimeField()
#     read_at = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'notifications'

class property(models.Model):
    propertyid = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    longdescription = models.TextField()
    shortdescription = models.CharField(max_length=255)
    propertycategory = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    districtid = models.IntegerField()
    defaultpictureid = models.CharField(max_length=20)
    googlemappin = models.CharField(max_length=200)
    verified = models.CharField(max_length=3)
    verifiedby = models.CharField(max_length=200)
    verifiedtimestamp = models.CharField(max_length=200)
    verifiednotes = models.CharField(max_length=200)
    enabled = models.CharField(max_length=3)
    nextverification = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'property'

class PropertyAwards(models.Model):
    id = models.BigAutoField(primary_key=True)
    property_id = models.BigIntegerField()
    title = models.CharField(max_length=255)
    year_awarded = models.IntegerField()
    url = models.URLField()
    award_authority_id = models.BigIntegerField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'property_awards'

class PropertyCategories(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    icon_id = models.BigIntegerField()
    picture = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'property_categories'

class PropertyFacilities(models.Model):
    id = models.BigAutoField(primary_key=True)
    property_id = models.BigIntegerField()
    icon_id = models.BigIntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    property_picture_id = models.BigIntegerField()
    long_description_details = models.TextField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'property_facilities'

class PropertyPictures(models.Model):
    id = models.BigAutoField(primary_key=True)
    property_id = models.BigIntegerField()
    title = models.CharField(max_length=255)
    picture_url = models.CharField(max_length=255)
    description = models.TextField()
    is_cover = models.BooleanField()
    display_order = models.IntegerField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'property_pictures'

class PropertyRestrictions(models.Model):
    id = models.BigAutoField(primary_key=True)
    property_id = models.BigIntegerField()
    restriction_id = models.BigIntegerField()
    notes = models.TextField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'property_restrictions'

class PropertyRoomCategories(models.Model):
    id = models.BigAutoField(primary_key=True)
    property_id = models.BigIntegerField()
    verified = models.BooleanField()
    verification = models.CharField(max_length=255)
    picture = models.CharField(max_length=255)
    size_details = models.CharField(max_length=255)
    max_occupancy = models.IntegerField()
    no_of_units = models.IntegerField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'property_room_categories'

class PropertyRoomCategoryFeatures(models.Model):
    id = models.BigAutoField(primary_key=True)
    room_category_id = models.BigIntegerField()
    icon_id = models.BigIntegerField()
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'property_room_category_features'

class Restrictions(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    icon_id = models.BigIntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'restrictions'

class SystemConfiguration(models.Model):
    id = models.BigAutoField(primary_key=True)
    config_key = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    config_value = models.TextField()
    data_type = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'system_configuration'

class Users(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    email = models.CharField(max_length=255)
    password_hash = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    updated_at = models.DateTimeField()
    last_login_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'users'

class UserSessions(models.Model):
    session_id = models.BigAutoField(primary_key=True)
    user_id = models.BigIntegerField()
    ip_address = models.CharField(max_length=45)
    user_agent = models.TextField()
    expires_at = models.DateTimeField()
    is_active = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'user_sessions'

class VerificationDetails(models.Model):
    id = models.BigAutoField(primary_key=True)
    property_id = models.BigIntegerField()
    verified = models.BooleanField()
    verified_notes = models.TextField()
    verifier_timestamp = models.DateTimeField()
    times_verified = models.IntegerField()
    next_verification_date = models.DateTimeField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'verification_details'

# Your new Teachers model that will create a new table
class Teachers(models.Model):
    reg_no = models.IntegerField()
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    gender = models.CharField(max_length=10)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    subject = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Teachers"
        managed = False  # Django can manage this table
        db_table = 'teachers'

# Keep your existing Member model (from old database)
class Member(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.firstname} {self.lastname}"
    
    class Meta:
        managed = False  # Reference to existing table
        db_table = 'members_member'