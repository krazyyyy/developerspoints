from django.contrib import admin

from .models import Portfolio, ProjectImages, Contact
# Register your models here.

class InlineProjects(admin.StackedInline):
    model = ProjectImages
    extra = 0
    classes = ["collapse"]

class PortfolioAdmin(admin.ModelAdmin):
    inlines = [InlineProjects]

admin.site.register(Portfolio, PortfolioAdmin)
admin.site.register(Contact)