from django.contrib import admin
from .models import Node

class NodeAdmin(admin.ModelAdmin):
    '''
    Test for SystemCheckError when using the position field in the Admin.
    '''
    list_display = ('position', 'name')
    list_display_links = ('name',)
    list_filter = ('parent',)
    search_fields = ('name',)

admin.site.register(Node, NodeAdmin)
