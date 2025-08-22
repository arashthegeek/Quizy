from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.exceptions import AuthenticationFailed
from web.models import CustomUser as User
from django.contrib.auth.models import AnonymousUser
#from django.shortcuts import redirect
#from django.http import HttpResponse

class JWTMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        token = request.COOKIES.get('access')
        
        if token:
            try:
                access_token = AccessToken(token)
                user_id = access_token.payload.get('user_id')
                request.user = User.objects.get(id=user_id)
                
            except Exception as e:
                request.user = AnonymousUser()
                response = self.get_response(request)
                response.delete_cookie('refresh')
                response.delete_cookie('access')
                return response
        else:
            request.user = AnonymousUser()
        response = self.get_response(request)
        return response
