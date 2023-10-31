import logging
import json
from django.views.generic import View
from google.oauth2 import id_token
from google.auth.transport import requests
from firebase_admin import auth
from core.account.http_utils import LazyEncoder
from django.http import HttpResponse
from django.conf import settings
from core.account.utils import handle_authentication
from django.contrib.auth import logout
from django.utils.translation import gettext as _


class AuthenticateViewSocial(View):
    # Post method to get firebase auth Id token
    def post(self, request, *args, **kwargs):
        
        if request.user.is_authenticated:
            print("You are already authenticated")
            logout(request)
        try:
            # Get Token from request
            token = request.POST.get("token")
            # If token is not none, then authorize user
            uid = ""
            current_user = None
            if token is not None:
                # Verify token
                # Check if it is Main Google Auth Flow
                if request.POST.get("GoogleAuth") == "true":
                    try:
                        # Supplied by g_id_onload
                        tokenid = request.POST.get(
                            "token"
                        )
                        idinfo = id_token.verify_oauth2_token(
                            tokenid, requests.Request(), settings.GOOGLE_CLIENT_ID
                        )
                        try:
                            user = auth.get_user_by_email(idinfo["email"])
                            uid = user.uid
                            current_user = auth.get_user(uid)
                            return handle_authentication(self, current_user, uid)
                        except Exception as e:
                            logging.error(f"Firebase User Not Found, creating one!! {e}")
                            displayname = idinfo["email"].replace("@", " ")
                            user = auth.create_user(
                                email=idinfo["email"],
                                email_verified=False,
                                display_name=displayname,
                                disabled=False,
                            )
                            uid = user.uid
                            # Current_user holds the firebase auth object
                            current_user = auth.get_user(uid)
                            return handle_authentication(self, current_user, uid)
                    except Exception as e:
                        logging.error(f"GOOGLE IDENTITY SERVICE AUTH ERROR {e}")
                        return HttpResponse(json.dumps({'message': _('ERROR in user Authentication! Try again.')}, cls=LazyEncoder), status=401, content_type="application/json")
                elif request.POST.get("GoogleAuth") == "false":
                    decoded_token = auth.verify_id_token(token)
                    uid = decoded_token["uid"]
                    # Current_user holds the firebase auth object
                    current_user = auth.get_user(uid)
                    return handle_authentication(self, current_user, uid)
        # Return invalide token error
        except auth.InvalidIdTokenError as e:
            logging.error(f"ERROR IN Authentication - Wrong Token: {e}")
            return HttpResponse(json.dumps({'message': _('Verification Error! Try again.')}, cls=LazyEncoder), status=401, content_type="application/json")
        except Exception as e:
            logging.error(f"ERROR IN Authentication Final: {e}")
            return HttpResponse(json.dumps({'message': _('Verification Error! Try again.')}, cls=LazyEncoder), status=401, content_type="application/json")
        return HttpResponse(json.dumps({'message': _('Something went wrong! Try again.')}, cls=LazyEncoder), status=401, content_type="application/json")