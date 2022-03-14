from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.pagination import PageNumberPagination


# unify response model schema
class CustomRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context['response'].status_code
        response = {
            "status": "success",
            "code": status_code,
            "data": data,
            "message": None
        }
        if not str(status_code).startswith('2'):
            response["status"] = "error"
            response["data"] = None

            if 'detail' in data:
                response["message"] = data["detail"]
            else:
                response['message'] = dict2string(data)

        return super(CustomRenderer, self).render(response, accepted_media_type, renderer_context)


# pagination default class
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


# convert serializer error into json error
def dict2string(data):
    msg = ""
    for key in data.keys():
        if key == "non_field_errors":
            msg += data[key][0] + "\n\r"
        else:
            msg += key + ": " + data[key][0] + "\n\r"
    return msg
