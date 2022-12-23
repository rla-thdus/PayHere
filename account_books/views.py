from datetime import datetime

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account_books.models import Memo
from account_books.serializers import MemoSerializer
from config.permissions import IsMine


class MemoAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = MemoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MemoDetailAPI(APIView):
    permission_classes = [IsAuthenticated, IsMine]

    def get_object(self, memo_id):
        if Memo.objects.filter(id=memo_id, deleted_at=None).exists():
            memo = Memo.objects.get(id=memo_id)
            self.check_object_permissions(self.request, memo)
            return memo
        return None

    def get(self, request, memo_id):
        memo = self.get_object(memo_id)
        if memo is None:
            return Response({'message': 'Invalid memo id'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = MemoSerializer(memo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, memo_id):
        memo = self.get_object(memo_id)
        if memo is None:
            return Response({'message': 'Invalid memo id'}, status=status.HTTP_400_BAD_REQUEST)
        memo.deleted_at = datetime.today()
        memo.save()
        return Response({'message': f'Deleted memo id is {memo_id}'}, status=status.HTTP_202_ACCEPTED)
