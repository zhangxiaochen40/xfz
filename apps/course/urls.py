from django.urls import path
from .views import *

app_name = 'course'

urlpatterns = [
    path('', course_index, name='course_index'),
    path('<int:course_id>', course_detail, name='course_detail')
]