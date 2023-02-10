from __future__ import unicode_literals
from .models import *

from django.contrib import admin

# Register your models here.

from record.models import Image
 
admin.site.register(Image)
admin.site.register(Record)