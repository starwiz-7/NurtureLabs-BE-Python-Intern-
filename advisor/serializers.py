from rest_framework import serializers
from .models import *
from user.models import User

class addAdvisor(serializers.ModelSerializer):

    class Meta:
        model = Advisor
        fields = ['id','name','profile_pic']

    def validate(self,attrs):
        name = attrs.get('name','')
        profile_pic = attrs.get('profile_pic','')
        return attrs

    def create(self,data):
        return Advisor.objects.create(**data)

class allAdvisor(serializers.ModelSerializer):

    class Meta:
        model = Advisor
        fields = ['id','name','profile_pic']

class bookAdvisor(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = ['id','time','user','advisor']
    
    def validate(self,attrs):
        time = attrs.get('time','')
        return attrs
    
    def create(self,data):
        return Booking.objects.create(**data)

class allBooking(serializers.ModelSerializer):
    
    advisor = allAdvisor()
    class Meta:
        model = Booking
        fields = ['id','time','advisor']
    