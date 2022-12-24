from datetime import datetime

from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account_books.models import Memo
from account_books.serializers import MemoSerializer
from config.permissions import IsMine


class MemoAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        memos = Memo.objects.filter(user=request.user, deleted_at=None)
        serializer = MemoSerializer(memos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
        raise NotFound(detail='Invalid memo id')

    def get(self, request, memo_id):
        memo = self.get_object(memo_id)
        serializer = MemoSerializer(memo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, memo_id):
        memo = self.get_object(memo_id)
        memo.id = None
        memo.save()
        return Response({'message': f'memo({memo_id}) copied to memo({memo.id})'}, status=status.HTTP_201_CREATED)

    def patch(self, request, memo_id):
        memo = self.get_object(memo_id)
        serializer = MemoSerializer(memo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, memo_id):
        memo = self.get_object(memo_id)
        memo.deleted_at = datetime.today()
        memo.save()
        return Response({'message': f'Deleted memo id is {memo_id}'}, status=status.HTTP_202_ACCEPTED)
