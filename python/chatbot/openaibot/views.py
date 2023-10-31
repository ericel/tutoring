import logging
import json
from django.views.generic import View
from core.account.http_utils import LazyEncoder
from django.http import HttpResponse
from django.contrib.auth import logout
from django.utils.translation import gettext as _
from openaibot.utils import welcome_text, prompt_completion


class ChatBotView(View):
    """ChatBot View
    Args:
        View (_type_): _description_
    """
    def post(self, request, *args, **kwargs):
        '''
        if request.user.is_authenticated:
            print("You are already authenticated")
            logout(request)
        '''
        if self.request.headers.get('POST-TYPE') == 'entry_home':
            # Get chatbot welcome text and frequently asked questions
            return welcome_text(self)
        if self.request.headers.get('POST-TYPE') == 'prompt_completion':
            # Get prompt completion from openai
            prompt = request.POST.get("prompt")
            return prompt_completion(self, prompt)
        # try:
        #     # Get Token from request
        #     token = request.POST.get("token")
            
        # except Exception as e:
        #     logging.error(f"CHATBOT Error Final: {e}")
        #     return HttpResponse(json.dumps({'message': f"CHATBOT Error Final: {e}"}, cls=LazyEncoder), status=401, content_type="application/json")
        return HttpResponse(json.dumps({'message': _('Something went wrong! Try again.')}, cls=LazyEncoder), status=401, content_type="application/json")