package google;

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import com.google.auth.oauth2.GoogleCredentials;
import com.google.cloud.firestore.Firestore;

import com.google.firebase.FirebaseApp;
import com.google.firebase.FirebaseOptions;

public class UploadJSONToFirestore {
	public String filepath;
    public String method;
    public String collectionname;

	/**
	 * 
	 */
	public UploadJSONToFirestore(String filepath, String method, String collectionname) {
        this.filepath = filepath;
        this.method = method;
        this.collectionname = collectionname;
    }
	
	// Main CLass method
    // Processes JSON File and uploads 
    // Data to Firestore using 'set' or 'add' method.
    @SuppressWarnings("unchecked")
	public void upload(){
        JSONParser jsonParser = new JSONParser();
        try (FileReader reader = new FileReader(this.filepath))
        {
            //Read JSON file
            Object obj = jsonParser.parse(reader);
 
            JSONArray dataList = (JSONArray) obj;
             
            //Iterate over employee array
            dataList.forEach(item -> { 
            	if(this.method.equals("add")) {
            		add((JSONObject) item);
            	} else if(this.method.equals("set")) {
            		set((JSONObject) item);
            	}
            });
           
 
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } catch (ParseException e) {
            e.printStackTrace();
        }
        
    }
    
    // Adds a collection to firestore
    // Firebase Firestore auto-generated ids
    public void add(JSONObject item){
    	System.out.print("hello");

    }

    // Sets documents to a collection on firestore
    // Uses custom IDS, in this case our json object ID field
    public void set(JSONObject  item){
    	System.out.print(item);
    }

	/**
	 * @param args
	 */
	 public static void main(String[] args) throws Exception {
	        if(args.length != 3){
	           throw new Exception("EXCEPTION: Arguements don't match!");
	        }
	        UploadJSONToFirestore uploadJSONFILEFIRESTORE = new UploadJSONToFirestore(args[0], args[1], args[2]);
	        uploadJSONFILEFIRESTORE.upload();
	        System.out.println("Hello");
	    }

}

//java jsonfirestore/UploadJSONFILEFIRESTORE.java jsonfirestore/data.json set demo-users