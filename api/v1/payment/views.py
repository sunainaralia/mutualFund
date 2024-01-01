from .models import Transactions
from .serializers import TransactionSerializer
from rest_framework.views import APIView
from .renderers import UserRenderers
from rest_framework.response import Response
from rest_framework import status


class TransactionView(APIView):
    renderer_classes = [UserRenderers]

    def post(self, request, format=None):
        serializer = TransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "success": True,
                "msg": "payment info is saved successfully",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


class GetTransactionView(APIView):
    def get(self, request, pk=None, format=None):
        try:
            data = Transactions.objects.get(pk=pk)
            serializer = TransactionSerializer(data)
            return Response(
                {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
            )
        except Transactions.DoesNotExist:
            return Response(
                {"success": False, "msg": " user doesn't exist"},
                status=status.HTTP_404_NOT_FOUND,
            )


class GetTransactionThroughUserId(APIView):
    def get(self, request, pk=None, format=None):
        try:
            queryset = Transactions.objects.filter(user=pk)
            instances = queryset.all()
            serializer = TransactionSerializer(instances, many=True)

            return Response(
                {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
            )
        except Transactions.DoesNotExist:
            return Response(
                {"success": False, "msg": " user doesn't exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
