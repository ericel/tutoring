import random
import string
import logging
import json
from django.utils import timezone
from django.http import HttpResponse
from django.utils.translation import gettext as _
from django.contrib.auth import login
from django.conf import settings
from core.account.http_utils import LazyEncoder
from core.account.models import CustomUser
from firebase_admin import auth
# Random username generator
letters = string.ascii_lowercase
random_username = "".join(random.choice(letters) for i in range(10))


def createdjangouserobject(
        username,
        uid,
        email,
        first_name,
        last_name,
        is_verified
    ):
    """This function handles user creation. As user is saved to database"""
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
    """This function handles authentication"""
    try:
        
        user = CustomUser.objects.get(uid=uid)
        if user.is_active == True:
            user.is_verified = current_user.email_verified
            user.save()
            login(self.request, user)
            next_ = self.request.GET.get("next", "/")
            return HttpResponse(json.dumps({"next": next_}, cls=LazyEncoder), status=200, content_type="application/json")
        else:
            print('error here')
            return HttpResponse(json.dumps({"message": _("Make sure you have your account verified! Check your account email.")}, cls=LazyEncoder), status=401, content_type="application/json")
    # User doesn't exist in Django
    except CustomUser.DoesNotExist:
        try:
            # Removes all special characters/spaces from a string
            username = re.sub("[^A-Za-z0-9]+", "", (current_user.display_name).lower())
        except:
            # With an exception, lets create a username from the account email
            nameme = current_user.email.split("@")
            username = nameme[0]
            logging.info(_("Could not get display name, create user name"))
        # Name Array to hold lastname and firstname
        namearray = (current_user.display_name).split(" ", 1) if  current_user and current_user.display_name != None else ['First Name', 'Last Name']
       
        if CustomUser.objects.filter(username=username.lower()).exists():
            username = random_username
        
        first_name = namearray[0] if namearray != None else "New"
        last_name = namearray[1] if namearray != None else f"user"
        
        # Set User as Verified, if firebase has verified the email
        is_verified = True if current_user.email_verified == True else False
        
        # Handle a case where user lacks email
        # Possible occurance from social auth like facebook PHONE NUMBER authenticated users
        email = current_user.email if current_user.email else random_username + "@no_email.com"

         # Check Email
        if CustomUser.objects.filter(email=email).exists():
            return HttpResponse(json.dumps({"message": _("User with this email already exist.")}, cls=LazyEncoder), status=401, content_type="application/json")

        # Create Django User
        user = createdjangouserobject(
                        username,
                        uid,
                        email,
                        first_name,
                        last_name,
                        is_verified
                    )

        # If user has not been verified by firebase
        # We want Firebase to message them to verify their account
        '''
        if current_user.email_verified == False and email:
            action_code_settings = auth.ActionCodeSettings(
                url=f'{settings.SITE_URL}/verify_account/{current_user.uid}',
                handle_code_in_app=True,
            )
           
            email = current_user.email
            link = auth.generate_email_verification_link(email, action_code_settings)
            """ SET UP YOUR OWN MAILING HERE AS YOU HAVE HE VERIFICATION LINK """
            #****** YOU CAN SEND ACTIVATION LINK HERE TO USER EMAIL *****#
        '''    
        return HttpResponse(json.dumps({"message": _("You successfully signed up! Check your email to verify your account.")}, cls=LazyEncoder), status=200, content_type="application/json")
    except Exception as e:
        logging.critical(e, exc_info=True)
        logging.error(f"HELPER ERROR IN Authentication Final: {e}")
        return HttpResponse(json.dumps({"message": _("Something went wrong! Try again")}, cls=LazyEncoder), status=401, content_type="application/json")
    return HttpResponse(json.dumps({"message": _("Something went wrong! Try again")}, cls=LazyEncoder), status=401, content_type="application/json")