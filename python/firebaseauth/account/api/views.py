import logging
import json
from rest_framework.views import APIView
from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from account.utils import handle_authentication, get_firebase_user_by_uid, GOOGLE_AUTH_TRUE, GOOGLE_AUTH_FALSE
from django.contrib.auth import logout
from django.utils.translation import gettext as _
from firebase_admin import auth

class AuthenticateViewSocial(APIView):
    # Post method to handle Firebase Auth ID token and Google Auth
    def post(self, request, *args, **kwargs):
        
        # Check if user is already authenticated
        if request.user.is_authenticated:
            logout(request)  # Log the user out
            return Response({'message': _('You are already logged in, You will be logged out!')},
                            status.HTTP_400_BAD_REQUEST)
        
        try:
            # Retrieve the token from the incoming request
            token = request.POST.get("token")
            
            # Initialize variables for later use
            uid = ""
            current_user = None
            
            # Check if the token exists
            if token:
                # Verify the token and determine the type of authentication
                
                # Case: Google's Main Auth Flow
                if request.POST.get("GoogleAuth") == GOOGLE_AUTH_TRUE:
                    try:
                        # Get token ID supplied by Google's g_id_onload
                        tokenid = request.POST.get("token")
                        
                        # Verify the Google token
                        idinfo = id_token.verify_oauth2_token(
                            tokenid, requests.Request(), settings.GOOGLE_CLIENT_ID
                        )
                        
                        try:
                            # Fetch Firebase user by email
                            user = auth.get_user_by_email(idinfo["email"])
                            uid = user.uid
                            
                            # Fetch current_user using utility function
                            current_user = get_firebase_user_by_uid(uid)
                            return handle_authentication(self, current_user, uid)
                        
                        except Exception as e:
                            # User not found in Firebase, create one
                            logging.error(f"Firebase User Not Found, creating one!! {e}")
                            displayname = idinfo["email"].replace("@", " ")
                            user = auth.create_user(
                                email=idinfo["email"],
                                email_verified=False,
                                display_name=displayname,
                                disabled=False,
                            )
                            uid = user.uid
                            
                            # Fetch current_user using utility function
                            current_user = get_firebase_user_by_uid(uid)
                            return handle_authentication(self, current_user, uid)
                    
                    except Exception as e:
                        # Handle Google Auth errors
                        logging.error(f"GOOGLE IDENTITY SERVICE AUTH ERROR {e}")
                        return Response({'message': _('ERROR in user Authentication! Try again.')},
                                        status.HTTP_400_BAD_REQUEST)
                
                # Case: Firebase Auth
                elif request.POST.get("GoogleAuth") == GOOGLE_AUTH_FALSE:
                    decoded_token = auth.verify_id_token(token)
                    uid = decoded_token["uid"]
                    
                    # Fetch current_user using utility function
                    current_user = get_firebase_user_by_uid(uid)
                    return handle_authentication(self, current_user, uid)
        
        # Handle invalid token errors
        except auth.InvalidIdTokenError as e:
            logging.error(f"ERROR IN Authentication - Wrong Token: {e}")
            return Response({'message': _('Verification Error! Wrong token. Try again.')},
                            status.HTTP_401_UNAUTHORIZED)
        
        # Handle any other exceptions
        except Exception as e:
            logging.error(f"ERROR IN Authentication Final: {e}")
            return Response({'message': _('Verification Error! Try again.')},
                            status.HTTP_401_UNAUTHORIZED)
        
        # Final fallback response
        return Response({'message': _('Something went wrong! Try again.')},
                        status.HTTP_400_BAD_REQUEST)
