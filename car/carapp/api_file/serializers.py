from rest_framework import serializers
from ..models import Carlist , Showroomlist , Review


def alphanumeric (value):
    if not str (value).isalnum ():
        raise serializers.ValidationError ('Only alphanumeric characters are allowed') 

class ReviewSerializer (serializers.ModelSerializer):
    apiuser = serializers.StringRelatedField (read_only = True)
    class Meta :
        model = Review
        # fields = '__all__'
        exclude = ['car']

class CarSerializer (serializers.ModelSerializer):
    chassisno = serializers.CharField (validators = [alphanumeric])
    discounted_price = serializers.SerializerMethodField ()
    Review = ReviewSerializer (many = True , read_only = True)
    class  Meta :
        model = Carlist
        fields = '__all__'
    
    def validate_price (self, value):
        if value <= 20000.00:
            raise serializers.ValidationError ('Price must be greater than 20000.00')
        return value
    
    def validate(self, data):
        if data ['name'] == data ['desc'] :
            raise serializers.ValidationError ("Name and desc must be different")
        return data
    
    def get_discounted_price (self , object):
        discountprice = object.price - 5000
        return discountprice

class ShowroomSerializer (serializers.ModelSerializer):
    # Showroom = CarSerializer (many = True , read_only = True)
    Showroom = serializers.StringRelatedField (many = True)
    # Showroom = serializers.PrimaryKeyRelatedField (many = True , read_only = True)
    # Showroom = serializers.HyperlinkedRelatedField (many = True , read_only = True , view_name= 'car_detail')
    class Meta:
        model = Showroomlist
        fields = '__all__'
    


