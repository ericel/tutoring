# for command line arguements.
import sys
import json

# SETTING UP YOUR VIRTUAL ENVIRONMENT
# For Mac
# pip install virtualenv
# virtualenv <your-env>
# source tutoring/bin/activate
# tutoring/bin/pip install google-cloud-firestore

# For Window
# pip install virtualenv
# virtualenv <your-env>
# <your-env>\Scripts\activate
# <your-env>\Scripts\pip.exe install google-cloud-firestore
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import timeit
# Use a service account
cred = credentials.Certificate('service-account.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

class UploadJsonFileToFirestore:
    def __init__(self) -> None:
        # Get class running time
        self.start = timeit.default_timer()
        # Check to make sure the command line arguements 
        # are atleast 3 arguements
        if len(sys.argv[1:]) != 3:
            print(f'ERROR: Check your command line arguments!,\n 3 arguements expected [file=filepath, method=[set or add], collectionname=[firestore collection name]')
            return None
        
        # Initialize instance variables
        self.json_data = sys.argv[1:][0]
        self.method = sys.argv[1:][1]
        self.collectionname = sys.argv[1:][2]
    
    def __str__(self) -> str:
        return (f'Uploading ****{self.file}***** JSON items to firestore!')
    
    # Firestore upload method getter method
    @property
    def method(self):
        return self._method
    
    # Firestore upload method setter method
    @method.setter
    def method(self, val):
        if val == 'set' or val == 'add':
            self._method = val
        else:
            print(f'Wrong method {val}, use set or add')
    
    # Get Json file path property
    @property
    def json_data(self):
        return self._json_data
    
    # Set and process Json file path property
    @json_data.setter
    def json_data(self, val):
        if val:
            try:
                # Opening JSON file
                f = open(val,)
                
                # returns JSON object as a dictionary
                data = json.load(f)
                
                # make sure to close file
                f.close()
                self._json_data = data
            except Exception as e:
                print(f'FILE EXCEPTION: {str(e)}')
        else:
            print(f'Wrong file path {val}')

    # Main class method to populate firestore 
    # With the said data
    def upload(self):
        if  self.json_data and self.method:
           
            # Iterating through the json list
            for idx, item in enumerate(self.json_data):
                '''
                 START FOR JUST FOR DEMO REASONS
                '''
                from pygments import highlight
                from pygments.lexers import JsonLexer
                from pygments.formatters import TerminalFormatter
              
                json_str = json.dumps(item, indent=4, sort_keys=True)
                print(highlight(json_str, JsonLexer(), TerminalFormatter()))
                '''
                 END FOR JUST FOR DEMO REASONS
                '''
             
                if self.method == 'set':
                    self.set(item)
                else:
                    self.add(item)
                # Successfully got to end of data;
                # print success message
                if idx == len(self.json_data)-1:
                    # All the program statements
                    stop = timeit.default_timer()
                    print('**************************\n****SUCCESS UPLOAD*****\n**************************')
                    print("Time taken "+str(stop - self.start))
    
    # Collection Add method
    # Adds all data under a collection
    # With firebase firestore auto generated IDS
    def add(self, item):
        return db.collection(self.collectionname).add(item)
    
    # Collection document set method
    # Adds all data under a collection
    # With custom document IDS 
    def set(self, item):
        return db.collection(self.collectionname).document(str(item['id'])).set(item)

uploadjson = UploadJsonFileToFirestore()
uploadjson.upload()      