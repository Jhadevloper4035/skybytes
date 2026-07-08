from django.db import models

# Create your models here.

STATUS = (
    (0, 'Not Active'),
    (1, 'Active')
)

PROJECT_STATUS = (
        ('0', 'Under Construction'),
        ('1', 'New Launch'),
        ('2', 'Ready To Move')
)

PROJECT_CAT_TYPE = (
    ('residential', 'residential'),
    ('commercial', 'commercial'),
)

PROJECT_FEATURED = (
        (0, 'No'),
        (1, 'Yes')
)

PROJECT_PREMIUM = (
        (0, 'No'),
        (1, 'Yes'),
)

PROJECT_TYPE = (
    ('1 BHK', '1 BHK'),
    ('2 BHK', '2 BHK'),
    ('3 BHK', '3 BHK'),
    ('4 BHK', '4 BHK'),
    ('5 BHK', '5 BHK'),
    ('6 BHK', '6 BHK'),
    ('6+ BHK', '6+ BHK'),
    ('Villa', 'Villa'),
    ('Penthouse', 'Penthouse'),
    ('Builder Floor', 'Builder Floor'),
    ('Retail Shop', 'Retail Shop'),
    ('Anchor Store', 'Anchor Store'),
    ('Office Space', 'Office Space'),
    ('Multiplex', 'Multiplex'),
    ('Restaurant', 'Restaurant'),
    ('Food Court', 'Food Court'),
    ('Studio Apartment', 'Studio Apartment'),
    ('Plot', 'Plot')
)

PROPERTYTYPE = (
    ('Flats', 'Flats'),
    ('Plot', 'Plot'),
    ('House', 'House'),
    ('Apartments', 'Apartments'),
    ('Villas', 'Villas'),
    ('Duplex', 'Duplex'),
    ('Farm House', 'Farm House'),
    ('Studio Apartment', 'Studio Apartment'),
)

PROFILE_TYPE = (
        ('Business Owner', 'Business Owner'),
        ('Salaried', 'Salaried'),
        ('Other', 'Other')
)

PROJECT_AREA = (
        ('0', 'Sq.Ft'),
        ('1', 'Sq.Yards'),
        ('2', 'Sq.m'),
        ('3', 'Grounds'),
        ('4', 'Aankadam'),
        ('5', 'Rood'),
        ('6', 'Chataks'),
        ('7', 'Perch'),
        ('8', 'Guntha'),
        ('9', 'Acres'),
        ('10', 'Biswa'),
        ('11', 'Ares'),
        ('12', 'Bigha'),
        ('13', 'Kottah'),
        ('14', 'Hectares'),
        ('15', 'Marla'),
        ('16', 'Kanal')
)

DETAIL_TRANSACTION_TYPE = (
        ('0', 'Original Booking'),
        ('1', 'Resale')
)

DETAIL_OWNERSHIP = (
        ('0', 'First Owner'),
        ('1', 'Free Hold')
)

DETAIL_FLOORING = (
        ('0', 'Marble'),
        ('1', 'Virtified'),
        ('2', 'Polished Concrete'),
        ('3', 'Granite'),
        ('4', 'Ceramic'),
        ('5', 'Mosaic'),
        ('6', 'Cement'),
        ('7', 'Stone'),
        ('8', 'Vinyl'),
        ('9', 'Wood'),
        ('10', 'Concrete'),
        ('11', 'Spartex'),
        ('12', 'IPSFinish'),
        ('13', 'Others')

)

DETAIL_FURNISHING = (
        ('0', 'Un-Furnished'),
        ('1', 'Semi Furnished'),
        ('2', 'Full Furnished')
)

DETAIL_GATED_COMMUNITY = (
        ('0', 'No'),
        ('1', 'Yes')
)

DETAIL_PARKING = (
        ('0', 'Open Parking'),
        ('1', 'Covered Parking')
)

DETAIL_WATER_SOURCE = (
        ('0', 'Munciple Corporation'),
        ('1', 'Other')
)

DETAIL_SERVANT_QUARTER = (
        ('0', 'No'),
        ('1', 'Yes')
)

DETAIL_STORE = (
        ('0', 'No'),
        ('1', 'Yes')
)

DETAIL_STUDY_ROOM = (
        (0, 'No'),
        (1, 'Yes')
)

DETAIL_POOJA_ROOM = (
        (0, 'No'),
        (1, 'Yes')
)

DETAIL_PARK = (
        (0, 'No'),
        (1, 'Yes')
)

DETAIL_CLUB = (
        (0, 'No'),
        (1, 'Yes')
)

DETAIL_SWIMMING_POOL = (
        (0, 'No'),
        (1, 'Yes')
)

DETAIL_FACING = (
        ('0', 'East'),
        ('1', 'West'),
        ('2', 'North'),
        ('3', 'South'),
        ('4', 'North-East'),
        ('5', 'North-West'),
        ('6', 'South-East'),
        ('7', 'South-West')     
)

DETAIL_POWER_BACKUP = (
        ('0', 'Full'),
        ('1', 'Partial'),
        ('2', 'None')
)

DETAIL_LIGHT = (
        (0, 'No'),
        (1, 'Yes')
)

DETAIL_FRIDGE = (
        (0, 'No'),
        (1, 'Yes')
)

DETAIL_AC = (
        (0, 'No'),
        (1, 'Yes')
)

DETAIL_STOVE = (
        (0, 'No'),
        (1, 'Yes')
)

DETAIL_WASHING_MACHINE = (
        (0, 'No'),
        (1, 'Yes')
)

DETAIL_PURIFIER = (
        (0, 'No'),
        (1, 'Yes')
)

DETAIL_MICROWAVE = (
        (0, 'No'),
        (1, 'Yes')
)

DETAIL_CHIMNEY = (
        (0, 'No'),
        (1, 'Yes')
)

DETAIL_EXAST_FANS = (
        (0, 'No'),
        (1, 'Yes')
)

DETAIL_SOFA = (
        (0, 'No'),
        (1, 'Yes')
)

DETAIL_DINING_TABLE = (
        (0, 'No'),
        (1, 'Yes')
)

DETAIL_SOFA = (
        (0, 'No'),
        (1, 'Yes')
)

DETAIL_SECURITY_DEPOSIT = (
        (0, 'No'),
        (1, 'Yes')
)

PROPERTY_FOR = (
        (0, 'Sale'),
        (1, 'Rent')
)

PROPERTY_STATUS = (
        (0, 'Active'),
        (1, 'Not Active')
)

PROPERTY_AVAILABLE_FOR = (
        ('0', 'Family'),
        ('1', 'Bachelors'),
        ('2', 'Single Men'),
        ('3', 'Single Women'),
        ('4', 'Business Man'),
        ('5', 'All')
)

PROPERTY_PRICE_NEGOTIABLE = (
        (0, 'No'),
        (1, 'Yes')
)

PROPERTY_BROKERAGE_NEGOTIABLE = (
        (0, 'No'),
        (1, 'Yes')
)

PROPERTY_AGE = (
        ('0', '0-1 Years'),
        ('1', '1-5 Years'),
        ('1', '5-10 Years'),
        ('1', '10+ Years')
)

PROPERTY_MONTH_NOTICE = (
        ('0', 'None'),
        ('1', '1 Month'),
        ('2', '2 Month'),
        ('3', '3 Month'),
        ('4', '4 Month'),
        ('5', '5 Month'),
        ('6', '6 Month')
        
)

PROPERTY_RENT_AGREEMENT_DURATION = (
        ('0', '0 Months'),
        ('1', '1 Months'),
        ('2', '2 Months'),
        ('3', '3 Months'),
        ('4', '4 Months'),
        ('5', '5 Months'),
        ('6', '6 Months'),
        ('7', '7 Months'),
        ('8', '8 Months'),
        ('9', '9 Months'),
        ('10', '10 Months'),
        ('11', '11 Months'),
        ('12', '12 Months'),
        ('13', '13 Months'),
        ('14', '14 Months'),
        ('15', '15 Months'),
        ('16', '16 Months'),
        ('17', '17 Months'),
        ('18', '18 Months'),
        ('19', '19 Months'),
        ('20', '20 Months'),
        ('21', '21 Months'),
        ('22', '22 Months'),
        ('23', '23 Months'),
        ('24', '24 Months'),
        ('25', '25 Months'),
        ('26', '26 Months'),
        ('27', '27 Months'),
        ('28', '28 Months'),
        ('29', '29 Months'),
        ('30', '30 Months'),
        ('31', '31 Months'),
        ('32', '32 Months'),
        ('33', '33 Months'),
        ('34', '34 Months'),
        ('35', '35 Months'),
        ('36', '36 Months')     
)
PROPERTY_FEATURES = (
        ('0', 'Water Storage'),
        ('1', 'Security/Fire Alarm'),
        ('2', 'Vaastu Compliant'),
        ('3', 'Intercom Facility'),
        ('4', 'Piped Gas'),
        ('5', 'Internet/Wi-fi Connectivity'),
        ('6', 'Centrally Air Conditioned'),
        ('7', 'Water Purifier'),
        ('8', 'Private Garden/Terraces')
)

PROPERTY_SOCIETY_FEATURES = (
        ('0', 'Visitor Parking'),
        ('1', 'Water Softening Plant'),
        ('2', 'Shopping Centre'),
        ('3', 'Club House/Community Centre'),
        ('4', 'Security Personal')
)

PROPERTY_OTHER_FEATURES = (
        ('0', 'Waste Disposal'),
        ('1', 'Bank Attached Property')
)

PROPERTY_ADDITIONAL_FEATURES = (
        ('0', 'In a Gated Society'),
        ('1', 'Corner Property'),
        ('2', 'Pet Friendly'),
        ('3', 'Wheelchair Friendly')
)

STATUS_ALL = (
        ('No', 'No'),
        ('Yes', 'Yes')    
)