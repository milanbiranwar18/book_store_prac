import logging

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from book.models import Book
from book.serializer import BookSerializer

logging.basicConfig(filename="user_serializer.log",
                    filemode='a',
                    format='%(asctime)s %(levelname)s-%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class BookAPI(APIView):

    def post(self, request):
        try:
            serializer = BookSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"Message": "Book created successfully", 'data': serializer.data, 'status': 201})
        except Exception as e:
            logging.error(e)
            return Response({"message": str(e)}, status=400)

    def get(self, request):
        try:
            book = Book.objects.all()
            serializer = BookSerializer(book, many=True)
            return Response({"Message": "All Books are", 'data': serializer.data, 'status': 201})
        except Exception as e:
            logging.error(e)
            return Response({"message": str(e)}, status=400)

    def put(self, request, id):
        try:
            book = Book.objects.get(id=id)
            serializer = BookSerializer(book, request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"Message": "Book updated successfully", 'data': serializer.data, 'status': 200})
        except Exception as e:
            logging.error(e)
            return Response({"message": str(e)}, status=400)

    def delete(self, request, id):
        try:
            book = Book.objects.get(id=id)
            book.delete()
            return Response({"Message": "Book deleted successfully", 'status': 200})
        except Exception as e:
            logging.error(e)
            return Response({"message": str(e)}, status=400)
