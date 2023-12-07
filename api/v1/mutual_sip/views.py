# mutual_fund_app/views.py
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
from api.v1.account.models import UserSipDetails


#  post sip
# class PostSip(APIView):
#     renderer_classes = [UserRenderers]

#     def post(self, request, format=None):
#         serializer = SIPSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         return Response(
#             {
#                 "success": True,
#                 "msg": " sip is saved successfully",
#                 "data": serializer.data,
#             },
#             status=status.HTTP_201_CREATED,
#         )


# class PostSip(APIView):
#     renderer_classes = [UserRenderers]

#     def post(self, request, format=None):
#         serializer = SIPSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         user_sip_details_count = UserSipDetails.objects.filter(sips_taken=user).count()
#         user.no_of_investors = user_sip_details_count
#         user.save()

#         return Response(
#             {
#                 "success": True,
#                 "msg": "SIP is saved successfully",
#                 "data": serializer.data,
#             },
#             status=status.HTTP_201_CREATED,
#         )


class PostSip(APIView):
    renderer_classes = [UserRenderers]

    def post(self, request, format=None):
        serializer = SIPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        users_in_sip = UserSipDetails.objects.filter(sips_taken=user)
        user.no_of_investors = users_in_sip.count()
        user.total_investment = sum(
            user_sip.invested_amount for user_sip in users_in_sip
        )
        user.save()

        return Response(
            {
                "success": True,
                "msg": "SIP is saved successfully",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


# get all sip
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


# change user's sip details
class ChangeSip(APIView):
    renderer_classes = [UserRenderers]

    def patch(self, request, pk, format=None):
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

    def delete(self, request, pk, format=None):
        data = SIP.objects.get(pk=pk)
        data.delete()
        return Response(
            {"success": True, "msg": " sip is deleted succcessfully"},
            status=status.HTTP_200_OK,
        )

    
    def get(self, request, pk=None, format=None):
        data = SIP.objects.get(pk=pk)
        serializer = SIPSerializer(data)
        return Response(
            {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )
