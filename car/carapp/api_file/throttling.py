from rest_framework.throttling import UserRateThrottle

class CarViewThrottle (UserRateThrottle):
    scope = 'throttling_for_car_view'
    
class CarDetailThrottle (UserRateThrottle):
    scope = 'throttling_for_car_details'