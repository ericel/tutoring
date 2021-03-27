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

# Use a service account
cred = credentials.Certificate('service-account.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

class UploadJsonFileToFirestore:
    def __init__(self) -> None:
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


    def upload(self):
        if  self.json_data and self.method:
            print(len(self.json_data))
            print(self.method)
        
            # Iterating through the json list
            for i in self.json_data:
                print(i)
                doc_ref = db.collection(u'users-demos').add(i)
        try:
            # doc_ref = db.collection(u'users').document(u'alovelace')
            # doc_ref.set({
            #     u'first': u'Ada',
            #     u'last': u'Lovelace',
            #     u'born': 1815
            # })

            # Then query for documents
            users_ref = db.collection(u'users')

            for doc in users_ref.stream():
                print(u'{} => {}'.format(doc.id, doc.to_dict()))
        except Exception as e:
            print(e)
        pass

    

uploadjson = UploadJsonFileToFirestore()
uploadjson.upload()      