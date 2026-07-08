from django.contrib import admin
from .models import (
    Project, Detail, ProjectImages, ProjectFloorPlan,
    CategoryProjectCity, ProjectStatus, Amenity,
    Country, State, City, Location
)
from .models import Education, Health, Transportation, ProjectLead, ProjectLinks


@admin.register(ProjectLinks)
class ProjectLinksAdmin(admin.ModelAdmin):
    list_display = ('name', 'subchild_category', 'slug', 'status', 'created_at')
    list_filter = ('status', 'subchild_category')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        ('Page Identity', {
            'fields': (('name', 'slug'), 'subchild_category', 'status')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_desc', 'meta_keyword')
        }),
        ('Page Content', {
            'fields': ('content',)
        }),
    )


@admin.register(ProjectLead)
class ProjectLeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'project', 'source', 'created_at')
    list_filter = ('source', 'created_at', 'project')
    search_fields = ('name', 'phone', 'email')
    readonly_fields = ('name', 'phone', 'email', 'message', 'project', 'source', 'created_at')
    ordering = ('-created_at',)

class DetailsInline(admin.StackedInline):
    model = Detail
    can_delete = False
    fk_name = 'project'
    extra = 0
    max_num = 1
    verbose_name = 'Project Detail'
    verbose_name_plural = 'Project Details'
    fieldsets = (
        ('Area & Pricing', {
            'fields': (
                ('minarea', 'maxarea', 'areaselect', 'project_area_type', 'tot_area'),
                ('minprice', 'maxprice', 'price_negotiable', 'transaction_type'),
            )
        }),
        ('Project Structure', {
            'fields': (
                ('possession', 'towers', 'floors', 'unites'),
                ('bedroom', 'bathroom', 'sqft_area', 'rera'),
                ('available_from', 'launch_date', 'fav_pro'),
            )
        }),
        ('Features & Amenities', {
            'fields': (
                ('facing', 'overlooking', 'flooring', 'furnishing'),
                ('power_backup', 'parking', 'water_source', 'ownership'),
                ('air_conditioned', 'moduler_kitchen', 'pet_friendly', 'vastu_complaint'),
                ('maintenence_staff', 'maintenence_charges', 'gated_community'),
            )
        }),
        ('Project Info', {
            'fields': (
                ('project_name', 'project_location'),
                ('main_road_width', 'internal_road_width', 'scheme'),
                ('approved_by', 'gst_on_plot', 'construction_permission'),
                ('registry_type', 'bank_loan_availability', 'eligibility'),
                ('distance_to_railway', 'distance_to_delhi', 'distance_to_airport'),
                ('nearby_university', 'metro_expansion', 'rrts'),
            )
        }),
    )

class ProjectImagesInline(admin.TabularInline):
    model = ProjectImages
    extra = 1

class ProjectFloorPlanInline(admin.TabularInline):
    model = ProjectFloorPlan
    extra = 1


class EducationInline(admin.TabularInline):
    model = Education
    extra = 1
    max_num = 10


class HealthInline(admin.TabularInline):
    model = Health
    extra = 1
    max_num = 10


class TransportationInline(admin.TabularInline):
    model = Transportation
    extra = 1
    max_num = 10

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'public_id', 'city', 'location', 'status', 'isFeatured', 'premium', 'created_at')
    list_filter = ('city', 'status', 'isFeatured', 'premium')
    search_fields = ('name', 'public_id', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [DetailsInline, ProjectImagesInline, ProjectFloorPlanInline, EducationInline, HealthInline, TransportationInline]
    filter_horizontal = ('amenity', 'category',)
    fieldsets = (
        ('Basic Information', {
            'fields': (
                ('name', 'slug', 'public_id'),
                ('city', 'location'),
                ('isFeatured', 'premium', 'status'),
            )
        }),
        ('SEO', {
            'classes': ('collapse',),
            'fields': (
                ('meta_title', 'keyword'),
                'meta_desc',
            )
        }),
        ('Category & Amenities', {
            'fields': ('project_link', 'category', 'amenity')
        }),
        ('Rich Content', {
            'classes': ('collapse',),
            'fields': ('description', 'paymentplan', 'keyfeatures', 'loc_adv')
        }),
        ('Project Images', {
            'fields': (
                ('location_image', 'sitemap_image'),
            )
        }),
    )
    class Media:
        css = {
            'all': ('admin_custom/project_admin.css',)
        }

# @admin.register(Detail)
# class DetailAdmin(admin.ModelAdmin):
#     list_display = ('project', 'minprice', 'maxprice', 'bedroom', 'bathroom')
#     search_fields = ('project__name',)


# @admin.register(Education)
# class EducationAdmin(admin.ModelAdmin):
#     list_display = ('project', 'name', 'distance')
#     search_fields = ('project__name', 'name')


# @admin.register(Health)
# class HealthAdmin(admin.ModelAdmin):
#     list_display = ('project', 'name', 'distance')
#     search_fields = ('project__name', 'name')


# @admin.register(Transportation)
# class TransportationAdmin(admin.ModelAdmin):
#     list_display = ('project', 'name', 'distance')
#     search_fields = ('project__name', 'name')

# Register supporting models simply
# admin.site.register(CategoryProjectCity)
# admin.site.register(ProjectStatus)
admin.site.register(Amenity)
# admin.site.register(Country)
# admin.site.register(State)
admin.site.register(City)
admin.site.register(Location)
