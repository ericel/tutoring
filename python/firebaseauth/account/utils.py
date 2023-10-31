import random
import string
import logging
import re
from django.utils import timezone
from firebase_admin import auth
from rest_framework import status  # Importing the status module from DRF
from rest_framework.response import Response
from django.utils.translation import gettext as _
from django.contrib.auth import login
from account.models import CustomUser

# Random username generator
letters = string.ascii_lowercase
random_username = "".join(random.choice(letters) for i in range(10))

# Constants
GOOGLE_AUTH_TRUE = "true"
GOOGLE_AUTH_FALSE = "false"

# Utility Function to get firebase user
def get_firebase_user_by_uid(uid):
    """Fetches the Firebase user object using uid."""
    return auth.get_user(uid)

def createdjangouserobject(username, uid, email, first_name, last_name, is_verified):
    """ Function to create a Django User object and save it to the database """
    return CustomUser.objects.create(
        username=username,
        uid=uid,
        email=email,
        first_name=first_name,
        last_name=last_name,
        is_verified=is_verified,
        created_at=timezone.localtime(timezone.now()),
        updated_at=timezone.localtime(timezone.now()),
        last_login=timezone.localtime(timezone.now()),
    )


def handle_authentication(self, current_user, uid):
    """ Function to handle authentication """
    try:
        user = CustomUser.objects.get(uid=uid)
        if user.is_active:
            user.is_verified = current_user.email_verified
            user.save()
            login(self.request, user)
            next_ = self.request.GET.get("next", "/")
            return Response({"next": next_}, status=status.HTTP_200_OK)  # Using DRF's status
        else:
            return Response({"message": _("Make sure you have your account verified! Check your account email.")}, status=status.HTTP_401_UNAUTHORIZED)  # Using DRF's status
    except CustomUser.DoesNotExist:
        try:
            username = re.sub("[^A-Za-z0-9]+", "", (current_user.display_name).lower())
        except:
            nameme = current_user.email.split("@")
            username = nameme[0]
            logging.info(_("Could not get display name, create user name"))
        
        namearray = (current_user.display_name).split(" ", 1) if current_user and current_user.display_name else ['First Name', 'Last Name']
       
        if CustomUser.objects.filter(username=username.lower()).exists():
            username = random_username
        
        first_name = namearray[0]
        last_name = namearray[1]
        is_verified = current_user.email_verified
        email = current_user.email if current_user.email else random_username + "@no_email.com"

        if CustomUser.objects.filter(email=email).exists():
            return Response({"message": _("User with this email already exists.")}, status=status.HTTP_401_UNAUTHORIZED) 

        user = createdjangouserobject(username, uid, email, first_name, last_name, is_verified)

        return Response({"message": _("You successfully signed up! Check your email to verify your account.")}, status=status.HTTP_200_OK)  # Using DRF's status
    except Exception as e:
        logging.critical(e, exc_info=True)
        logging.error(f"HELPER ERROR IN Authentication Final: {e}")
        return Response({"message": _("Something went wrong! Try again")}, status=status.HTTP_401_UNAUTHORIZED)  
    return Response({"message": _("Something went wrong! Try again")}, status=status.HTTP_401_UNAUTHORIZED) 
