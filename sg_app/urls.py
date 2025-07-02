from django.urls import path
from .views import (
    map_view,
    groves_list, 
    index,
    submit_sacred_grove,
    verify_sacred_groves,
    approve_sacred_grove,
    about
)

urlpatterns = [
    path("", index, name="index"),
    path('map/', map_view, name='map'),
    path('about/', about, name='about'),

    path('api/groves-list/', groves_list, name='groves_list_api'),

    path('submit-grove/', submit_sacred_grove, name='submit_sacred_grove'),

    path('verify-groves/', verify_sacred_groves, name='verify_sacred_groves'),
    path('approve-grove/<int:grove_id>/', approve_sacred_grove, name='approve_sacred_grove'),
]
