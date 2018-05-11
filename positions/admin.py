from django.conf import settings
from django.contrib import admin
from django.shortcuts import get_object_or_404
from django.utils.functional import update_wrapper
from django.conf.urls.defaults import patterns, url
from django.contrib.admin.util import unquote
from django.http import HttpResponseRedirect


class PositionAdmin(admin.ModelAdmin):
    def get_urls(self):
        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.module_name
        return patterns('',
            url(r'^(.+)/position-(up)/$', wrap(self.position_view), name='%s_%s_position_up' % info),
            url(r'^(.+)/position-(down)/$', wrap(self.position_view), name='%s_%s_position_down' % info),
        ) + super(PositionAdmin, self).get_urls()
        
    def position_view(self, request, object_id, direction):
        obj = get_object_or_404(self.model, pk=unquote(object_id))
        if direction == 'up':
            obj.position_up()
        else:
            obj.position_down()
        return HttpResponseRedirect('../../')
    
    def position_up_down_links(self, obj):
        return '''
        <a href="../../%(app_label)s/%(module_name)s/%(object_id)s/position-down/"><img src="%(STATIC_URL)spositions/img/arrow-up.gif" alt="Position Up" /></a>
        <a href="../../%(app_label)s/%(module_name)s/%(object_id)s/position-up/"><img src="%(STATIC_URL)spositions/img/arrow-down.gif" alt="Position Down" /></a>''' % {
            'app_label': self.model._meta.app_label,
            'module_name': self.model._meta.module_name,
            'object_id': obj.id,
            'STATIC_URL': settings.STATIC_URL,
        }

    position_up_down_links.allow_tags = True

    position_up_down_links.short_description = 'Position'


