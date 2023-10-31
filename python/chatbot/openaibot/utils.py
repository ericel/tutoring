"""Module to support chatbot app"""
import json
import openai
import requests
from bs4 import BeautifulSoup
from django.conf import settings
from django.http import HttpResponse
from core.account.http_utils import LazyEncoder
from fuzzywuzzy import fuzz
openai.api_key = settings.OPENAIAPI_KEY


def welcome_text(self):
    """Returns welcome text and frequently asked questions"""
    result = {
        "message": f"Hi! I'm {settings.CHATBOT_NAME} a chatbot. How can I help you today?",
        "bot_faqs": ["Is this app free?", "How is my data secured?", "How many resumes can I create?", "How many resumes can I create?", "How to upgrade my account?"]
    }
    return HttpResponse(json.dumps(result, cls=LazyEncoder), status=200, content_type="application/json")

conversation = []



def crawl_website(url):
    """Crawl the website and extract relevant content"""
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract relevant content from the website
    extracted_content = ""

    # Modify the code below to extract the specific content relevant to your chatbot
    # You can use BeautifulSoup methods to find and extract specific HTML elements

    # Example:
    extracted_content += soup.find('div', class_='content').get_text()
    
    print(extracted_content)
    return extracted_content


def prompt_completion(self, prompt):
    """Do a completion request prompt to openai and return the results"""
    # print(type(classify_greetings_thankyou_goodbye(prompt)))
    # if classify_greetings_thankyou_goodbye(prompt) and classify_greetings_thankyou_goodbye(prompt) != 'None':
    #     return HttpResponse(json.dumps({"completion": classify_greetings_thankyou_goodbye(prompt).replace('assistant:', '')}, cls=LazyEncoder), status=200, content_type="application/json")
    #     # if classify_greetings_thankyou_goodbye(prompt).lower() == "#thankyou":
    #     #     prompt = "#thankyou"
    #     # if classify_greetings_thankyou_goodbye(prompt).lower().strip() == "#greeting":
    #     #     prompt = "#greeting"
    #     # if classify_greetings_thankyou_goodbye(prompt).lower() == "#goodbye":
    #     #     prompt = "#goodbye" 
    print('got here')
    global conversation
    
    # greetings_prompt = f"""
    # First identify the following text  \
    # delimited by tripple backsticks as a greeting or thank you or goodbye:```{prompt}```. Then reply appropriately. \
    # If it is first greetings, as for user name to better personalize the conversation. If is a goodbye, \
    # make a summary of the chat in not more than 50 words and present to the user with a goodbye message. 
    # """
    # If it is not a greeting or thank you or goodbye, then return a python None
    # Append the user's input to the conversation
    #conversation.append({'role': 'assistant', 'content': greetings_prompt})
    user_account_info = {
        'name': 'Oj Obasi',
        'email': 'ericel@gmial.com',
        'number of resumes downloads per quota': "10/20",
        'number of cover letters downloads per quota': "10/20",
        'number of resumes': 1,
        'number of cover letters': 1,
        'account type': "free membership account"
    }
    content = '''
   The only 100% Free Resume Maker online. 
Free Cover Letter Editor and Downloader. 
We give you the tools you need to get ready for your next job interview. 
Create, edit and download your free resume and cover letter.
Frequently asked:
1. Is Freeresumemaker truly free? 
Freeresumemaker is the only 100% free resume editor and download tool online. With a free Freeresumemaker account, you can edit and download your resume for free. Each resume you create with us, also has a free short URL that can be easily shared online.
2. How secured is your information with us?
We make use of Google Cloud App Engine. This means your information is secured within Google secured infrastructures. We value your data and make sure every bit of your data with us is well secured.
3. What are the supported formats?
We offer two download format options, PDF and Microsoft word formats. We intend to add more useful formats in the near future.
4. How many resumes and covers letters with a free account?
With a free account, you can only edit and download one free resume and one free cover letter. If you are in need of more resumes, coverletters, then you will need to get one of our premium account membership subscriptions.
5. How can you contribute to Freeresumemaker
As you have noticed, unlike other resume apps online, we offer a free service. We rely on donations from our service users to pay the bills and continue to service Freeresumemaker. You can always chip in something at <a href="https://www.freeresumemaker.io/en/donate"> Donate</a>
6. Do you have a resume upload service?
For now we have no resume uploading service. We are still undecided on whether such a feature is necessary.

To Sign up / login to an account, go to <a href="https://www.freeresumemaker.io/login/">Freeresumemaker Accounts</a>

When you use our services, you’re trusting us with your information. We understand this is a big responsibility and work hard to protect your information and put you in control.

This Privacy Policy is meant to help you understand what information we collect, why we collect it, and how you can update, manage, export, and delete your information.

We collect information to provide better services to all our users — from figuring out basic stuff like which language you speak. The information Freeresumemaker collects, and how that information is used, depends on how you use our services and how you manage your privacy controls.

We also collect the content you create, upload, or receive from others when using our services. This includes things like the job you post, the buy and sell products you post on our website, mobile apps, the discussions you start or participate in, photos you save to your profile.

Your name
Your email
Location
etc.
When you’re signed in, at Freeresumemaker we also collect information that we store with your Freeresumemaker Account, which we treat as personal information.

How to delete your account
We allow our users to permanently delete their accounts at any time. This functionality is available both on our mobile apps and websites.

To request account delete, go to your account settings page both on Mobile and website, check for Request Account Close(Delete Account) function. NOTE: Once you start the account close process, your account status is immediately set to closed. 2 Weeks from the Account close date, if you didn't sign back into any of our services, your account and any information about you will be permanently deleted from all our Freeresumemaker services!

If you have any questions, donot hesitate to <a href="https://www.freeresumemaker.io/contact/">Contact Us</a>

Free resume, cover letter editor and download.
Designed as a free service for job seekers.


Payment methods

We accept Secured stripe for upgrades and donations.



To upgrate your account go to <a href="https://www.freeresumemaker.io/en/upgrade_now">Contact Us</a>

    '''
    if not conversation:
        conversation = [
    {
        'role': 'system',
        'content': f'''
            You are a helpful assistant providing information about Freeresumemaker.
            Your initial task is to greet the customer and check if their user information is provided within triple backticks: ```{user_account_info}```.
            If the `user_account_info` does not contain user information, personalize the greeting by asking for their name, e.g., "May I have your name, please?"
            If the ```user_account_info``` contains user information, use it to personalize the chat, e.g., "Hello, [User Name]. You have one resume in your account."
            Ask the user how you can be of help.
            Utilize the content provided within triple backticks: ```{content}``` as a source of information.
            Also, make use of the user info provided in triple backticks: ```{user_account_info}```.
            If the source above does not contain instructions related to the user prompt specified within triple backticks: ```{prompt}```, reply with "No information found about this."
            If the user provides an email, thank them and inform them about the usage context of the email.
            If someone faces an issue related to account access or downloading resumes/cover letters, apologize and suggest remedies.
            For account login issues, provide password recovery steps.
            For download issues, suggest checking the download quota (20 downloads per day) and upgrading the account or waiting for 24 hours if necessary.
            If the download issue is unrelated to the download quota, suggest browser-related technical remedies.
            For subscription charge issues, direct the user to check their account page or provide contact details if available.
            If the ```{user_account_info}``` contains contact details, state those details and mention that a human agent will reach out soon.
            Otherwise, request the user to leave their contact details for prompt resolution.
            After they provide contact details, ask if they need further assistance.
        '''
    }
]
    
    #crawl_website("https://www.freeresumemaker.io/")
    
    # Construct the prompt by concatenating the conversation history
    #prompt = f"{content}\n +You are a helpful assistant that provides information.\n\n"
    '''
    prompt = f"""

A website that allows users to edit and download their resumes and coverletters. \
You will be provided with text delimited by triple backticks. \
That you should use to answer questions about freeresumemaker. \
If the text does not contain a sequence of instructions related to the question, \
then simply write \"No information found about this. please leave your email and a human agent will get back to you.\"
{prompt}
```{content}```
"""
    for message in conversation:
        role = message['role']
        content = message['content']
        #prompt += f"{role}: {content}\n"
    '''
    # Append the user's input to the conversation
    conversation.append({'role': 'user', 'content': prompt})
    # Make the API call
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=conversation,
        temperature=1
    )

    # Extract the chatbot's response
    bot_response = response.choices[0].message["content"].strip()

    
    # Check for error handling or clarification
    if is_response_unclear(bot_response):
        bot_response = handle_unclear_response(bot_response)

    # Append the chatbot's response to the conversation
    conversation.append({'role': 'assistant', 'content': bot_response})       
    return HttpResponse(json.dumps({"completion": bot_response.replace('assistant:', '')}, cls=LazyEncoder), status=200, content_type="application/json")


def is_response_unclear(response):
    # Implement your own logic to determine if the response is unclear or ambiguous
    # For example, you can check for certain keywords or patterns indicating ambiguity
    if 'I did not understand' in response:
        return True
    return False


def handle_unclear_response(response):
    # Implement your own logic to handle unclear responses
    # You can ask for clarifications, provide suggestions, or take other appropriate actions
    clarification_prompt = "I'm sorry, but I didn't understand. Can you please provide more details or rephrase your question?"
    return clarification_prompt


def classify_greetings_thankyou_goodbye(text):
    """This function classifies greeting, thank you, and goodbye."""
    # Define the classification prompt
    prompt = f"""
    goodbye should be classified as a goodbye not greetings.Your role is to identify the following text  \
    delimited by tripple backsticks as a greeting or thank you or goodbye:```{text}```. Then reply appropriately. \
    If it is first greetings, as for user name to better personalize the conversation. If is a goodbye, \
    make a summary of the chat in not more than 50 words and present to the user with a goodbye message. \
    If it is not a greeting or thank you or goodbye, then return a python None"""
    # Append the user's input to the conversation
    conversation.append({'role': 'assistant', 'content': prompt})
    # Generate completion using GPT-3.5 model
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=conversation,
        temperature=1
    )

    # Extract the generated completion choice (category)
    completion_text = response.choices[0].message["content"].strip()
    return completion_text
    '''
    if completion_text == 'None':
        return None
    # Define category labels
    category_labels = {
        "greeting": "#greetings",
        "thank you": "#thankyou",
        "goodbye": "#goodbye"
    }

    # Find the best matching category label using fuzzy matching
    best_match = max(category_labels.keys(), key=lambda label: fuzz.ratio(label, completion_text))

    # Return the generated category or the best matching label
    category = category_labels.get(best_match, completion_text)
    return category
    '''