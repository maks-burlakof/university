from core_app.pagination import PageLimitPagination


class PostsPageLimitPagination(PageLimitPagination):
    page_size = 15
    max_page_size = 99
