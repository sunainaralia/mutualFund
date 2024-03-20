from django.db.models import Sum
from .models import SIP
from rest_framework.response import Response
from rest_framework import status
import json
from .serializers import SIPSerializer
from .renderers import UserRenderers
from rest_framework.views import APIView
from rest_framework.authentication import authenticate
from .renderers import UserRenderers
from rest_framework.permissions import IsAuthenticated
from api.v1.account.models import UserPurchaseOrderDetails
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .consumers import SIPConsumer
from api.v1.account.serializers import UserPurchaseOrderSerializer

class PostSip(APIView):
    renderer_classes = [UserRenderers]

    def post(self, request, format=None):
        serializer = SIPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "success": True,
                "msg": "SIP is saved successfully",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


# # get all sip
class GetAllSip(APIView):
    renderer_classes = [UserRenderers]

    def get(self, request, format=None):
        data = SIP.objects.all()
        if data:
            serializer = SIPSerializer(data, many=True)
            return Response(
                {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
            )
        else:
            return Response({"success": False}, status=status.HTTP_204_NO_CONTENT)


# # change user's sip details
class ChangeSip(APIView):
    renderer_classes = [UserRenderers]
    def patch(self, request, pk, format=None):
        try:
            data = SIP.objects.get(pk=pk)
            serializer = SIPSerializer(data, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(
                    {
                        "success": True,
                        "data": serializer.data,
                        "msg": " sip is changed successfully",
                    },
                    status=status.HTTP_200_OK,
                )
        except SIP.DoesNotExist:
            return Response(
                {"success": False, "msg": " user doesn't exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

    def delete(self, request, pk, format=None):
        try:
            data = SIP.objects.get(pk=pk)
            data.delete()
            return Response(
                {"success": True, "msg": " sip is deleted succcessfully"},
                status=status.HTTP_200_OK,
            )
        except SIP.DoesNotExist:
            return Response(
                {"success": False, "msg": " user doesn't exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

    def get(self, request, pk=None, format=None):
        try:
            data = SIP.objects.get(pk=pk)
            users_in_sip = UserPurchaseOrderDetails.objects.filter(sips=data.id)
            total_investors = users_in_sip.count()
            total_investment = sum(
                user_sip.invested_amount for user_sip in users_in_sip
            )
            current_value = sum(
                user_sip.current_value for user_sip in users_in_sip
            )
            total_gain =current_value - total_investment
            gain_percentage = (
                (total_gain / total_investment) * 100 if total_investment != 0 else 0
            )
            serializer = SIPSerializer(data)
            users_serializer = UserPurchaseOrderSerializer(users_in_sip, many=True)

            # Add additional calculated data to serializer data
            serializer_data = serializer.data
            serializer_data["total_investors"] = total_investors
            serializer_data["total_investment"] = total_investment
            serializer_data["total_gain"] = total_gain
            serializer_data["gain_percentage"] = gain_percentage
            serializer_data["current_value"] = current_value
            serializer_data["users"] = users_serializer.data
            return Response(
                {"success": True, "data": serializer_data}, status=status.HTTP_200_OK
            )
        except SIP.DoesNotExist:
            return Response(
                {"success": False, "msg": "SIP doesn't exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
