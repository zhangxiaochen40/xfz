from django.urls import path
from .views import *

app_name = 'course'

urlpatterns = [
    path('', course_index, name='course_index'),
    path('<int:course_id>', course_detail, name='course_detail'),
    path('course_token/', course_token, name='course_token'),
    path('course_order/<int:course_id>/', course_order, name='course_order')
]