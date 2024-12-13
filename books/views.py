from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from .models import Book
from .serializers import BookSerializer


class BookListAPIView(APIView):
    """
    API view to retrieve books with filtering, ordering, and pagination.
    """

    def get(self, request):
        queryset = Book.objects.prefetch_related(
            "authors", "bookshelves", "languages", "subjects", "formats"
        ).order_by("-download_count")

        # Extract query parameters
        id_filter = request.query_params.getlist("id")
        language_filter = request.query_params.getlist("language")
        mime_type_filter = request.query_params.getlist("mime-type")
        topic_filter = request.query_params.getlist("topic")
        author_filter = request.query_params.getlist("author")
        title_filter = request.query_params.getlist("title")

        # Apply filters
        if id_filter:
            queryset = queryset.filter(gutenberg_id__in=id_filter)
        if language_filter:
            queryset = queryset.filter(languages__code__in=language_filter)
        if mime_type_filter:
            queryset = queryset.filter(formats__mime_type__in=mime_type_filter)
        if topic_filter:
            topic_queries = Q()
            for topic in topic_filter:
                topic_queries |= Q(subjects__name__icontains=topic) | Q(bookshelves__name__icontains=topic)
            queryset = queryset.filter(topic_queries)
        if author_filter:
            for author in author_filter:
                queryset = queryset.filter(authors__name__icontains=author)
        if title_filter:
            for title in title_filter:
                queryset = queryset.filter(title__icontains=title)

        queryset = queryset.distinct()

        # Pagination
        page = int(request.query_params.get("page", 1))
        page_size = 25
        total_count = queryset.count()
        start = (page - 1) * page_size
        end = start + page_size
        paginated_queryset = queryset[start:end]

        serializer = BookSerializer(paginated_queryset, many=True)
        return Response({
            "count": total_count,
            "next": f"page={page + 1}" if end < total_count else None,
            "previous": f"page={page - 1}" if page > 1 else None,
            "results": serializer.data,
        })
