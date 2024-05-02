from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 12
    page_query_param = "page"
    max_page_size = 12
