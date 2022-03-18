from rest_framework_simplejwt.views import TokenViewBase
from .serializers import *
from .utils import *

# login with email and password
class LoginView(TokenViewBase):
    serializer_class = LoginSerializer
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]
