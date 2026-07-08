from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from category.models import Category, SubCategory, SubChildCategory
from PIL import Image
import sys
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from ckeditor_uploader.fields import RichTextUploadingField
from .choices import (
    PROJECT_TYPE,
    PROJECT_FEATURED,
    PROJECT_PREMIUM,
    PROJECT_AREA,
    DETAIL_FACING,
    DETAIL_POWER_BACKUP,
    DETAIL_PARKING,
    DETAIL_TRANSACTION_TYPE,
    DETAIL_WATER_SOURCE,
    DETAIL_OWNERSHIP,
    DETAIL_LIGHT,
    DETAIL_FLOORING,
    DETAIL_GATED_COMMUNITY,
    DETAIL_FURNISHING,
    PROPERTY_PRICE_NEGOTIABLE,
    DETAIL_SERVANT_QUARTER,
    DETAIL_SECURITY_DEPOSIT,
    STATUS,
    PROJECT_STATUS,
    STATUS_ALL,
    PROJECT_CAT_TYPE
)
import random, string

# Create your models here.

class Country(models.Model):
    name = models.CharField(max_length=128, null=True, blank=True,
                        help_text="Type: String, values: Enter Country Name")
    iso = models.CharField(max_length=16, null=True, blank=True, help_text="Type: String, values: Enter Country ISO")
    phonecode = models.IntegerField(null=True, blank=True, help_text="Type: Int, values: Enter Country Phone Code")

    def __str__(self):
        return self.name or "Country"

class State(models.Model):
    name = models.CharField(max_length=96, null=True, blank=True, help_text="Type: String, values: Enter State Name.")
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='StateCountry',
                                help_text="Type: Int, values: Select Country Name.")

    def __str__(self):
        return self.name or "State"

class City(models.Model):
    name = models.CharField(max_length=64, null=True, blank=True, help_text="Type: String, Values: Enter City Name")
    city_slug = models.SlugField(max_length=96, unique=True, null=True, blank=True, help_text="Type: String, Values: enter City Slug")
    city_code = models.CharField(max_length=16, unique=True, null=True, blank=True, help_text="Type: String, Values: Enter City Code")
    state = models.ForeignKey(State, related_name='states', on_delete=models.CASCADE, help_text="Type: Int, Values: Select State")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or "City"

class Location(models.Model):
    city = models.ForeignKey(City, related_name='locationcity', on_delete=models.CASCADE, null=True, blank=True, verbose_name="City Name", help_text="Type: Int, values: Select City Name.")
    name = models.CharField(max_length=96, null=True, blank=True, help_text="Type: String, Values: Enter Location Name.")
    slug = models.SlugField(max_length=96, unique=True, blank=True, null=True, help_text="Type: String, Values: Enter Location Slug.")
    meta_title = models.CharField(max_length=96, blank=True, null=True, help_text="Type: String, Values: Enter Location Meta Title.")
    meta_desc = models.TextField(max_length=180, blank=True, null=True, help_text="Type: String, Values: Enter Location Meta Description.")
    meta_keyword = models.CharField(max_length=180, blank=True, null=True, help_text="Type: String, Values: Enter Location Meta Keywords.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or "Location"

class ProjectStatus(models.Model):
    # keep app_label strings if cross-app import issues occur
    city = models.ForeignKey('City', on_delete=models.CASCADE, default=None, related_name="ProjectStatusCity", help_text="Type: Int, Values: Select City Name.")
    name = models.CharField(max_length=190, null=True, blank=True, help_text="Type: string, Default: None, Values: Enter Project Status.")
    slug = models.SlugField(max_length=190, unique=True, editable=True, null=True, blank=True, help_text="Type: String, Default: None, Values: Enter Slug.")
    for_slug = models.CharField(max_length=64, null=True, blank=True, help_text="Type: String, Values: eg-Project in, Property in, Used for create Project Slug.")
    meta_title = models.CharField(max_length=190, null=True, blank=True, help_text="Type: string, Default: None, Values: Enter Project Status.")
    meta_desc = models.TextField(max_length=255, null=True, blank=True, help_text="Type: string, Default: None, Values: Enter Project Status.")
    meta_keywords = models.CharField(max_length=190, null=True, blank=True, help_text="Type: string, Default: None, Values: Enter Project Status.")
    status_image = models.ImageField(upload_to='status_image/%Y/%m/%d', null=True, blank=True, max_length=255, help_text="Type: string, Default: null, Values: Upload Project Status Image.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or "ProjectStatus"

class Amenity(models.Model):
    am_name = models.CharField(max_length=120, null=True, blank=True)
    am_icon = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        return self.am_name or "Amenity"

class CategoryProjectCity(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    # category relation uses SubCategory from category app — keep string to avoid import issues if that model is moved
    category = models.ForeignKey('category.SubCategory', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=225, null=True, blank=True)
    slug = models.SlugField(max_length=225, unique=True, null=True, blank=True)
    meta_title = models.CharField(max_length=225, null=True, blank=True)
    meta_desc = models.CharField(max_length=285, null=True, blank=True)
    overview = RichTextUploadingField(null=True, blank=True, verbose_name='Overview', help_text="Type: string, Default: null, Values: Enter Overview")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or "CategoryProjectCity"


class ProjectLinks(models.Model):
    """
    A landing-page record that groups projects under a specific URL.
    URL structure: /<subchild_category.cat_slug>/<project_links.slug>/
    e.g. /residential-project/plots-for-sale-in-sonipat/
    """
    subchild_category = models.ForeignKey(
        'category.SubChildCategory',
        on_delete=models.CASCADE,
        related_name='project_links',
        verbose_name='Subchild Category',
        help_text="The subchild category this link page belongs to (determines the first URL segment)."
    )
    name = models.CharField(
        max_length=255,
        verbose_name='Name',
        help_text="Display name, e.g. Plots for Sale in Sonipat"
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name='Slug',
        help_text="URL slug, e.g. plots-for-sale-in-sonipat"
    )
    meta_title = models.CharField(max_length=165, null=True, blank=True, verbose_name='Meta Title')
    meta_desc = models.TextField(max_length=255, null=True, blank=True, verbose_name='Meta Description')
    meta_keyword = models.CharField(max_length=255, null=True, blank=True, verbose_name='Meta Keywords')
    content = RichTextUploadingField(
        null=True, blank=True,
        verbose_name='Page Content',
        help_text="Rich-text content displayed on this landing page above the project listings."
    )
    status = models.BooleanField(default=True, verbose_name='Active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Project Link'
        verbose_name_plural = 'Project Links'
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/{self.subchild_category.cat_slug}/{self.slug}/"


class Project(models.Model):
    # use string reference to avoid circular import; replace 'category.SubChildCategory' if model is in different app
    category = models.ManyToManyField('category.SubChildCategory', verbose_name='Select Category', related_name='pro_cat', blank=True)
    project_link = models.ForeignKey(
        ProjectLinks,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='projects',
        verbose_name='Project Link Page',
        help_text="Select the Project Links landing page this project is listed under."
    )
    city = models.ForeignKey('City', related_name='propcity', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Select City', help_text="Type: Int, Values: Select City Name.")
    location = models.ForeignKey('Location', related_name='proplocation', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Select Location', help_text="Type: Int, Values: Select ")
    amenity = models.ManyToManyField(Amenity, verbose_name="Select Project Amenity", related_name='ProjectAmenity', blank=True)
    name = models.CharField(null=True, max_length=114, blank=True, help_text="Type: string, Values: Enter Project Name.")
    slug = models.SlugField(null=True, unique=True, max_length=114, blank=True, help_text="Type: string, Values: Enter Project Slug.")
    public_id = models.CharField(max_length=12, unique=True, db_index=True, null=True, blank=True)
    isFeatured = models.BooleanField(default=False, verbose_name="Check for Featured Project")
    premium = models.BooleanField(default=False, verbose_name="Check for Premium Project")
    status = models.BooleanField(default=True, verbose_name="Check Status Active/In-Active")
    meta_title = models.CharField(max_length=165, null=True, blank=True, verbose_name='Meta Title', help_text="Type: string, Default: null, Values: Project Meta Title.")
    meta_desc = models.TextField(max_length=255, null=True, blank=True, verbose_name='Meta Description', help_text="Type: string, Default: null, Values: Project Meta Description.")
    keyword = models.CharField(max_length=165, null=True, blank=True, verbose_name='Meta Keyword', help_text="Type: string, Default: null, Values: Project Meta Keyword.")
    description = RichTextUploadingField(null=True, blank=True, verbose_name='Project Description', help_text="Type: string, Default: null, Values: Project Description.")
    paymentplan = RichTextUploadingField(null=True, blank=True, verbose_name='Payment Plan', help_text="Type: string, Default: null, Values: Project Payment Plan.")
    keyfeatures = RichTextUploadingField(null=True, blank=True, verbose_name='Education/Healthcare Hub', help_text="Type: string, Default: null, Values: Project Education & Healthcare Hub.")
    loc_adv = RichTextUploadingField(null=True, blank=True, verbose_name='Location Advantages', help_text="Type: string, Default: null, Values: Project Location Advantages.")
    location_image = models.ImageField(upload_to='location_image/%Y/%m/%d', null=True, blank=True, max_length=255, help_text="Type: string, Default: null, Values: Upload Location Image.")
    sitemap_image = models.ImageField(upload_to='sitemap_image/%Y/%m/%d', null=True, blank=True, max_length=255, help_text="Type: string, Default: null, Values: Upload SiteMap Image.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or "Project"

    def _generate_public_id(self, prefix="PJ", length=6):
        alphabet = string.ascii_uppercase + string.digits
        while True:
            candidate = prefix + ''.join(random.choices(alphabet, k=length))
            if not Project.objects.filter(public_id=candidate).exists():
                return candidate

    def save(self, *args, **kwargs):
        if not self.public_id:
            self.public_id = self._generate_public_id()
        # ensure slug exists
        if not self.slug and self.name:
            base = slugify(self.name)[:110]
            candidate = base
            i = 1
            while Project.objects.filter(slug=candidate).exists():
                candidate = f"{base}-{i}"
                i += 1
            self.slug = candidate
        super().save(*args, **kwargs)

    # class Meta:
    #     permissions = (
    #         ('view_project', 'Can view project'),
    #         ('add_change_project', 'Add or change project'),
    #         ('delete_project', 'Delete project'),
    #     )

    def get_absolute_url(self):
        # guard against missing city or slug
        city_slug = getattr(self.city, 'city_slug', None)
        slug = self.slug
        if city_slug and slug:
            return reverse('project:project_detail', kwargs={"slug": slug})
        return '#'
    
class Detail(models.Model):
    project = models.OneToOneField(Project, related_name='project_details', on_delete=models.CASCADE)
    possession = models.CharField(null=True, max_length=8, blank=True, choices=PROJECT_STATUS, verbose_name="Project Possession", help_text="Type: int, Values: Select Project Possession")
    minarea = models.CharField(null=True, max_length=32, blank=True, verbose_name='Minimum Area', help_text="Type: Int, Values: Enter Minimum Area.")
    areaselect = models.CharField(default='0', max_length=8, verbose_name="Select Project Area", choices=PROJECT_AREA, help_text="Type: Int, Default:0, Values: Select One")
    project_area_type = models.CharField(default='9', max_length=8, choices=PROJECT_AREA, verbose_name="Total Land Area", help_text="Type: Int, Default: 9, Values: Select Project Area.")
    maxarea = models.CharField(max_length=32, null=True, blank=True, verbose_name='Maximum Area', help_text="Type: Int, Values: Enter Maximum Area")
    minprice = models.IntegerField(null=True, blank=True, verbose_name="Minimum Price", help_text="Type: Int, Values: Enter Minimum Price")
    maxprice = models.IntegerField(null=True, blank=True, verbose_name='Maximum Price', help_text="Type: Int, Values: Enter Maximum Price")
    towers = models.IntegerField(null=True, blank=True, verbose_name='Total Towers', help_text="Type: Int, Values: Total Towers")
    floors = models.IntegerField(null=True, blank=True, verbose_name='Total Floors', help_text="Type: Int, Values: Total Floors")
    rera = models.CharField(max_length=96, null=True, blank=True, verbose_name='Rera Number', help_text="Type: String, Values: Enter Rera Number")
    bedroom = models.CharField(max_length=8, null=True, blank=True, verbose_name='Total Bedroom', help_text="Type: Int, Values: Enter Number of Bedroom")
    bathroom = models.CharField(max_length=8, null=True, blank=True, verbose_name='Total Bathroom', help_text="Type: Int, Values: Enter Number of Bathroom")
    sqft_area = models.CharField(max_length=285, null=True, blank=True)
    facing = models.CharField(max_length=32, null=True, blank=True, verbose_name='Project Facing', choices=DETAIL_FACING, help_text="Type: Int, Values: Select Project Facing.")
    overlooking = models.CharField(max_length=32, null=True, blank=True, verbose_name='Overlooking', choices=DETAIL_FACING, help_text="Type: Int, Values: Enter Project Overlooking.")
    unites = models.IntegerField(null=True, blank=True, verbose_name='Total Units', help_text="Type: Int, Values: Enter Total Project Units")
    tot_area = models.FloatField(null=True, blank=True, verbose_name='Total Area', help_text="Type: Int, Values: Enter Total Project Area")
    fav_pro = models.CharField(max_length=64, null=True, blank=True, verbose_name='Favour Of', help_text="Type: String, Values: Enter Cheque in Favour Of")
    available_from = models.DateField(verbose_name='Available From', null=True, blank=True, help_text="Type: String, Values: Enter Project Possession Date.")
    launch_date = models.DateField(verbose_name='Launch Date', null=True, blank=True, help_text="Type: String, Values: Enter Project Launch Date.")
    power_backup = models.CharField(max_length=8, default='0', choices=DETAIL_POWER_BACKUP, help_text="Type: Int, Default: 0")
    parking = models.CharField(default='0', max_length=8, choices=DETAIL_PARKING, help_text="Type: Int, Default: Open parking")
    transaction_type = models.CharField(null=True, max_length=8, blank=True, choices=DETAIL_TRANSACTION_TYPE, help_text="Type: Int, Values: Select One")
    water_source = models.CharField(default='0', max_length=8, choices=DETAIL_WATER_SOURCE, help_text="Type: Int, Values: Municipal")
    ownership = models.CharField(null=True, blank=True, max_length=8, choices=DETAIL_OWNERSHIP, help_text="Type: Int, Values: Select Ownership")
    price_negotiable = models.IntegerField(null=True, blank=True, choices=PROPERTY_PRICE_NEGOTIABLE, verbose_name="Price Negotiable", help_text="Type: Int, Values: Select Yes/No")
    flooring = models.CharField(null=True, blank=True, max_length=64, choices=DETAIL_FLOORING, verbose_name="Project Flooring", help_text="Type: Int, Values: Select Flooring")
    furnishing = models.CharField(null=True, blank=True, max_length=8, choices=DETAIL_FURNISHING, verbose_name="Furnishing Type", help_text="Type: Int, Values: Select Furnishing")
    gated_community = models.CharField(null=True, blank=True, max_length=16, choices=DETAIL_GATED_COMMUNITY, verbose_name="Gated Community", help_text="Type: Int, Values: Select Gated Community")
    air_conditioned = models.CharField(max_length=8, choices=STATUS_ALL, default='Yes', verbose_name="Air Conditioned", help_text="Type: Int, Values: Select Air Conditioned")
    moduler_kitchen = models.CharField(max_length=8, choices=STATUS_ALL, default='No', verbose_name="Modular Kitchen", help_text="Type: Int, Values: Modular Kitchen")
    pet_friendly = models.CharField(max_length=8, choices=STATUS_ALL, default='Yes', verbose_name="Pet Friendly", help_text="Type: Int, Values: Pet Friendly")
    vastu_complaint = models.CharField(max_length=8, choices=STATUS_ALL, default='Yes', verbose_name="Vastu Complaint", help_text="Type: Int, Values: Vastu Complaint")
    maintenence_staff = models.CharField(max_length=16, choices=STATUS_ALL, default='Yes', verbose_name="Maintenance Staff", help_text="Type: Int, Values: Maintenance Staff")
    maintenence_charges = models.IntegerField(null=True, blank=True, verbose_name="Maintenance Charges", help_text="Type: Int, Values: Enter Maint. Charges")
    # Project Info Fields
    project_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Project Name")
    project_location = models.CharField(max_length=255, null=True, blank=True, verbose_name="Location")
    main_road_width = models.CharField(max_length=64, null=True, blank=True, verbose_name="Main Road Width")
    internal_road_width = models.CharField(max_length=64, null=True, blank=True, verbose_name="Internal Road Width")
    scheme = models.CharField(max_length=255, null=True, blank=True, verbose_name="Scheme")
    approved_by = models.CharField(max_length=255, null=True, blank=True, verbose_name="Approved By")
    gst_on_plot = models.CharField(max_length=64, null=True, blank=True, verbose_name="GST on Plot")
    construction_permission = models.CharField(max_length=255, null=True, blank=True, verbose_name="Construction Permission")
    registry_type = models.CharField(max_length=128, null=True, blank=True, verbose_name="Registry Type")
    bank_loan_availability = models.CharField(max_length=255, null=True, blank=True, verbose_name="Bank Loan Availability")
    eligibility = models.CharField(max_length=255, null=True, blank=True, verbose_name="Eligibility")
    distance_to_railway = models.CharField(max_length=64, null=True, blank=True, verbose_name="Distance to Railway")
    distance_to_delhi = models.CharField(max_length=64, null=True, blank=True, verbose_name="Distance to Delhi")
    distance_to_airport = models.CharField(max_length=64, null=True, blank=True, verbose_name="Distance to Airport")
    nearby_university = models.CharField(max_length=255, null=True, blank=True, verbose_name="Nearby University")
    metro_expansion = models.CharField(max_length=255, null=True, blank=True, verbose_name="Metro Expansion")
    rrts = models.CharField(max_length=255, null=True, blank=True, verbose_name="RRTS")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def yearmonth(self):
        return self.available_from.strftime('%B, %Y') if self.available_from else ''

    @property
    def min_price_tag(self):
        if not self.minprice:
            return ""
        value = self.minprice
        if 1000 <= value <= 99999:
            return f"{value//1000} K"
        if 100000 <= value <= 9999999:
            return f"{value//100000} Lac"
        return f"{value/10000000:.2f} Cr"

    @property
    def max_price_tag(self):
        if not self.maxprice:
            return ""
        value = self.maxprice
        if 1000 <= value <= 99999:
            return f"{value//1000} K"
        if 100000 <= value <= 9999999:
            return f"{value//100000} Lac"
        return f"{value/10000000:.2f} Cr"

class ProjectImages(models.Model):
    project = models.ForeignKey(Project, related_name='projectimage', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    project_image = models.ImageField(upload_to='project_images/%Y/%m/%d', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.project.name if self.project else "ProjectImage"

    def save(self, *args, **kwargs):
        # compress only when creating and when image is present
        if self.project_image and not self.id:
            try:
                self.project_image = self.compressImage(self.project_image)
            except Exception:
                # if compression fails, keep original
                pass
        super(ProjectImages, self).save(*args, **kwargs)

    def compressImage(self, project_image):
        imageTemproary = Image.open(project_image)
        if imageTemproary.mode in ("RGBA", "P"):
            imageTemproary = imageTemproary.convert("RGB")
        outputIoStream = BytesIO()
        imageTemproaryResized = imageTemproary.resize((758, 500))
        imageTemproaryResized.save(outputIoStream, format='JPEG', quality=60)
        outputIoStream.seek(0)
        project_image = InMemoryUploadedFile(outputIoStream, 'ImageField', "%s.jpg" % project_image.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
        return project_image

    @property
    def imageURL(self):
        try:
            return self.project_image.url
        except:
            return ''


class Education(models.Model):
    project = models.ForeignKey(Project, related_name='education', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, help_text="Name of nearest educational institution or landmark")
    distance = models.CharField(max_length=64, help_text="Distance (e.g., 2 km)")

    def __str__(self):
        return f"Education: {self.name} ({self.distance})"


class Health(models.Model):
    project = models.ForeignKey(Project, related_name='health', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, help_text="Name of nearest health facility or hospital")
    distance = models.CharField(max_length=64, help_text="Distance (e.g., 1.5 km)")

    def __str__(self):
        return f"Health: {self.name} ({self.distance})"


class Transportation(models.Model):
    project = models.ForeignKey(Project, related_name='transportation', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, help_text="Nearest transport hub or landmark")
    distance = models.CharField(max_length=64, help_text="Distance (e.g., 500 m)")

    def __str__(self):
        return f"Transport: {self.name} ({self.distance})"

LEAD_SOURCE_CHOICES = [
    ('enquire', 'Enquire Now'),
    ('brochure', 'Download Brochure'),
    ('get_quote', 'Get Quote'),
    ('website', 'Website'),
]

class ProjectLead(models.Model):
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, related_name='leads', verbose_name='Project')
    name = models.CharField(max_length=128, verbose_name='Name')
    email = models.EmailField(null=True, blank=True, verbose_name='Email')
    phone = models.CharField(max_length=20, verbose_name='Phone')
    message = models.TextField(null=True, blank=True, verbose_name='Message')
    source = models.CharField(max_length=32, choices=LEAD_SOURCE_CHOICES, default='website', verbose_name='Source')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Project Lead'
        verbose_name_plural = 'Project Leads'

    def __str__(self):
        return f"{self.name} – {self.phone}"

class ProjectFloorPlan(models.Model):
    project = models.ForeignKey(Project, related_name='projectfloorplan', on_delete=models.CASCADE, null=True, blank=True)
    floorplan_image = models.ImageField(upload_to='floorplan_image/%Y/%m/%d', null=True, blank=True)
    bhk = models.CharField(max_length=100, null=True, blank=True, help_text="Type: String, Values: Enter Value")
    bed = models.CharField(max_length=100, null=True, blank=True, help_text="Type: String, Values: Enter Value")
    bath = models.CharField(max_length=100, null=True, blank=True, help_text="Type: String, Values: Enter Value")
    balcony = models.CharField(max_length=100, null=True, blank=True, help_text="Type: String, Values: Enter Value")
    size = models.CharField(max_length=100, null=True, blank=True, help_text="Type: String, Values: Enter Value")
    price = models.CharField(max_length=100, null=True, blank=True, help_text="Type: String, Values: Enter Value")
    price_persqft = models.IntegerField(null=True, blank=True, help_text="Type: String, Values: Enter Value")
    booking_amount = models.CharField(max_length=100, null=True, blank=True, help_text="Type: String, Values: Enter Value")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.project.name if self.project else "FloorPlan"

    def save(self, *args, **kwargs):
        if self.floorplan_image and not self.id:
            try:
                self.floorplan_image = self.compressImage(self.floorplan_image)
            except Exception:
                pass
        super(ProjectFloorPlan, self).save(*args, **kwargs)

    def compressImage(self, floorplan_image):
        imageTemproary = Image.open(floorplan_image)
        if imageTemproary.mode in ("RGBA", "P"):
            imageTemproary = imageTemproary.convert("RGB")
        outputIoStream = BytesIO()
        imageTemproaryResized = imageTemproary.resize((800, 600))
        imageTemproaryResized.save(outputIoStream, format='JPEG', quality=80)
        outputIoStream.seek(0)
        floorplan_image = InMemoryUploadedFile(outputIoStream, 'ImageField', "%s.jpg" % floorplan_image.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
        return floorplan_image
