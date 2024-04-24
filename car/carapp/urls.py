from django.urls import path , include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter ()
router.register ('showroom' , views.Showroom_viewset , basename= 'showroom')


urlpatterns = [
    path ('list' , views.Car_list_view.as_view () , name='car_list'),
    path ('<int:pk>', views.Car_detail_view.as_view () , name="car_detail"),
    path ('' , include (router.urls)),
    path ('showroom/<int:pk>/review-create' , views.Review_create.as_view() , name="review_create"),
    path ('showroom/<int:pk>/review' , views.Reviewlist.as_view() , name="review_list"),
    path ('showroom/review/<int:pk>/' , views.Review_detail.as_view() , name="review_detail"),
    # path ('review' , views.Reviewlist.as_view () , name= 'review_list'),
    # path ('review/<int:pk>' , views.Review_detail.as_view () , name= 'review_detail'),
    # path ('showroom' , views.Showroom_view.as_view () , name='showroom_view'),
    # path ('showroom/<int:pk>', views.Showroom_detail.as_view () , name="showroom_detail"),
    # path ('account/' , include ('user_app.api.urls')),
]
