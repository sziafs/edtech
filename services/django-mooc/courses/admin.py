from django.contrib import admin
#from courses.models import Course
from .models import Course
# Register your models here.

class CourseAdmin(admin.ModelAdmin):
    '''
    Ao inves de só registrar o curso    
    Opções para customizar o model no admin
    '''
    list_display = ['name', 'slug', 'start_date', 'created_at']
    search_fields = ['name', 'slug'] # OR

    #fazer o slug de forma automatica
    #ele pega o nome, deixa tudo minusculo, sem simbolos, separado por -
    prepopulated_fields = {'slug':('name',)}

#admin.site.register(Course)
admin.site.register(Course, CourseAdmin)