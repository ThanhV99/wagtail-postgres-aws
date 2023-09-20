# from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.utils.formats import localize
import pytz

from .models import BlogPage

class BlogPageAdmin(admin.ModelAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)

        if db_field.name == 'update_time':
            # Set the timezone to Asia/Ho_Chi_Minh
            timezone_ict = pytz.timezone('Asia/Ho_Chi_Minh')

            # Convert update_time to the target timezone
            if formfield.initial:
                formfield.initial = localize(formfield.initial.astimezone(timezone_ict))

            return formfield

    content_panels = [
        # Define your content panels here
    ]

admin.site.register(BlogPage, BlogPageAdmin)
