from datetime import datetime

from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account_books.models import Memo
from account_books.pagination import PaginationHandlerMixin
from account_books.serializers import MemoSerializer
from config.permissions import IsMine


class MemoAPI(APIView, PaginationHandlerMixin):
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    serializer_class = MemoSerializer
    order_fields = ['created_at', '-created_at', 'spend_price', '-spend_price']

    def get(self, request):
        order_by = request.query_params.get('order_by', '-created_at')
        if order_by not in self.order_fields:
            return Response({'message': 'Invalid ordering option'}, status=status.HTTP_400_BAD_REQUEST)
        memos = Memo.objects.filter(user=request.user, deleted_at=None).order_by(order_by)
        page = self.paginate_queryset(memos)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        else:
            serializer = self.serializer_class(memos, many=True)
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
