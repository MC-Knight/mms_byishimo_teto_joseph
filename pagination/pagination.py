from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 500

    def get_paginated_response(self, data, key="results"):
        return Response(
            {
                "message": "Success",
                "data": {
                    "total_pages": self.page.paginator.num_pages,
                    "total_count": self.page.paginator.count,
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                    key: data,
                },
            }
        )

    def paginate_queryset(self, queryset, request, view=None):
        all_records = request.query_params.get("all")
        if all_records is not None and all_records.lower() == "true":
            return None

        return super().paginate_queryset(queryset, request, view)
