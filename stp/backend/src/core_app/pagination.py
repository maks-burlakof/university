from rest_framework.pagination import PageNumberPagination


class PageLimitPagination(PageNumberPagination):
    page_query_param = "page"
    page_size = 20
    page_size_query_param = "limit"
    max_page_size = 100
