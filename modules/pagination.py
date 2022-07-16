from rest_framework.response import Response


def get_paginated_response(*, pagination_class, serializer_class,
                           queryset, request, view, do_sort=False, sort_by=None, context={}):
    """

    :param pagination_class: pagination class
    :param serializer_class: serializer class
    :param queryset: QuerySet
    :param request: request object
    :param view:
    :param do_sort: if you want to sort serializer data based on some key
    :param sort_by: key - by which sorting will be done
    :return: Json Response
    """
    paginator = pagination_class()

    page = paginator.paginate_queryset(queryset, request, view=view)

    if page is not None:
        serializer = serializer_class(page, many=True, context=context)
        if do_sort and sort_by:
            data = sorted(serializer.data, reverse=True, key=lambda k: k[sort_by])
        else:
            data = serializer.data
        return paginator.get_paginated_response(data)

    serializer = serializer_class(queryset, many=True, context=context)

    return Response(data=serializer.data)