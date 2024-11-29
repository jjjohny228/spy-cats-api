from django.contrib import admin
from cats.models import Cat, Mission, Target

admin.site.register([Cat, Mission, Target])
