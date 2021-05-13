from rest_framework import generics,permissions,status
from rest_framework.views import APIView
from rest_framework_simplejwt.backends import TokenBackend
from .serializers import *
from .models import *
from user.models import User
from rest_framework.response import Response
from datetime import datetime

class addAdvisorView(generics.GenericAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = addAdvisor
    def post(self,request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_200_OK)

class allAdvisorView(generics.ListAPIView):
    # def get(self,request,id):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = allAdvisor
    queryset = Advisor.objects.all()
    data = allAdvisor(queryset,many=True)
        # return Response(data.data,status=status.HTTP_200_OK)

class bookAdvisorView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = bookAdvisor
    def post(self,request,user_id,advisor_id):
        try:
            advisor = Advisor.objects.get(id=advisor_id)
            user = User.objects.get(id=user_id)
            time = request.data['time']
            current = datetime.now()
            if datetime.fromisoformat(time) < current:
                return Response({'message':'Date and time passed'},status=status.HTTP_400_BAD_REQUEST)
            if request.user.id == user_id:
                data = {
                    "time": time,
                    "user": user_id,
                    "advisor":advisor_id
                }
                serializer = self.serializer_class(data=data)
                # print(time)
                print(serializer.is_valid(raise_exception=True))
                serializer.save(user=user,advisor=advisor)
                return Response(status=status.HTTP_200_OK)
            else:
                return Response({'message':'Request user id mismatch'},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"message":str(e)},status=status.HTTP_400_BAD_REQUEST)

class allBookingsView(APIView):
    def get(self,request,user_id):
        permission_classes = [permissions.IsAuthenticated]
        serializer_class = allBooking
        if request.user.id == user_id:
        # bookings = user.bookings.all()
            booking = list(Booking.objects.all().filter(user=user_id))
            bookings = []
            for i in booking:
                advisor = Advisor.objects.get(id=i.advisor.id)
                print(i.advisor.id)
                data = {
                    'id':i.id,
                    'time':i.time,
                    'advisor':advisor
                }
                bookings.append(data.copy())
            serializer = serializer_class(bookings,many=True,context={'request':request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message':'Request user id mismatch'},status=status.HTTP_400_BAD_REQUEST)