from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('estate/<int:id>/', views.detail, name='detail'),
    path('estate_list/', views.estate_list_view, name='estate_list'),
    path('estates/filter/<str:filter_type>/', views.estate_list_filtered, name='estate_list_filtered'),

    path('estate_like/<int:id>/', views.user_estate_like, name='estate_like'),
    path('favourite_list/', views.favourite_list, name='favourite_list'),
    path('favourite/<int:id>/', views.toggle_favourite, name='favourite'),
    path('contact/', views.contact_view, name='contact'),
    path('about/', views.about_view, name='about'),
    path('response/<int:pk>/delete/', views.delete_response, name='delete_response'),
    path('feedback/<int:pk>/delete/', views.delete_feedback, name='delete_feedback'),
]

