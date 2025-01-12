from core_app.pagination import PageLimitPagination


class UsersPageLimitPagination(PageLimitPagination):
    page_size = 20
    max_page_size = 100
