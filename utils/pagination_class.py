from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    page_size = 10  # default limit
    page_query_param = 'page'
    page_size_query_param = 'limit'  # 👈 use `limit` instead of `page_size`
    max_page_size = 100
    # def __init__(self,message):
    #     self.message=message
    #     super().__init__() 
    def get_paginated_response(self, data,message):
        return Response({
            "message": message,
            "pagination": {
                "total": self.page.paginator.count,
                "pages": self.page.paginator.num_pages,
                "current_page": self.page.number,
                "limit": self.page.paginator.per_page,  # 👈 show current limit
                # "next": self.get_next_link(),
                # "previous": self.get_previous_link(),
            },
            "data": data
        })
