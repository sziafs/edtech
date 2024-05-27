from django.shortcuts import render
from django.shortcuts import get_object_or_404
from courses.models import Course

# Create your views here.
def courses(request):
    courses = Course.objects.all()
    dados = {
        'courses':courses,
    }
    return render(request, 'courses/courses.html', context=dados)

def course(request, slug):
    #course = Course.objects.get(pk=id)
    #course = get_object_or_404(Course, pk=id) # mais ideal para nao encontrado
    course = get_object_or_404(Course, slug=slug)
    dados = {
        'course': course,
    }
    return render(request, 'courses/course.html', context=dados)