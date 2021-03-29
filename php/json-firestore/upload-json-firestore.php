<?php
require('vendor/autoload.php');

#https://cloud.google.com/php/grpc#php-implementation
# Follow the implementation instructions in the above link 
# to get grpc installed and running in your system
# is not you won't be able to get cloud-firestore
# installed with composer
#composer require "grpc/grpc:^v1.27.0"
# composer require google/cloud-firestore
use Google\Cloud\Firestore\FirestoreClient;

class UploadJSONFILEFIRESTORE
{
    protected $db;

    public $json_file_path;
    public $method;
    public $collectionname;

    public $data = array();

    public function __construct()
    {
        # Get execution start time
        $this->time_start = microtime(true);

        #  INIT / CONFIG Firebase
        $this->db = new FirestoreClient([
            "projectId" => "otcollect-demos",
            "keyFile" => json_decode(file_get_contents('./../python/service-account.json'), true)
        ]);

        # Check is argv length is 4
        if (count($_SERVER['argv']) != 4) {
            throw new Exception('ARGV EXCEPTION: Check your command line arguements!');
        }

        # GET COMMAND LINE ARGv AND ASSIGN TO INSTANCE VARIABLES
        $this->json_file_path  = $_SERVER['argv'][1];
        $this->method          = $_SERVER['argv'][2];
        $this->collectionname  = $_SERVER['argv'][3];


        # check to make sure method is either set or add
        # the contructor may not be the exact place for this 
        # control structures, but this is a simple class
        # so there is no much appetide here for writting alot of code here
        # getters and setters are not really that waranted here.

        if ($this->method != 'set' && $this->method != 'add') {
            throw new Exception('WRONG ARGUEMENT EXCEPTION: set or add are only acceptable methods!');
        }
    }

    # Main class method
    # process JSON DATA
    # Uploads data to firestore backend
    public function upload()
    {
        # Read Json file
        $file = file_get_contents($this->json_file_path);
        # Decode Json string to associative array
        $this->data = json_decode($file, true);
        $i = 0;
        foreach ($this->data as $key => $value) {
            # Upload based on method
            print_r($value);
            if ($this->method == 'set') {
                $this->set($value);
            } elseif ($this->method == 'add') {
                $this->add($value);
            }

            # Check if this is last item to be uploaded
            # Log a success message of uploads
            if ($i == count($this->data) - 1) {
                echo '**************************' . "\r\n" . '****SUCCESS UPLOAD*****' . "\r\n" . '**************************' . "\r\n" . '';
                $time_end = microtime(true);
                echo ('Time taken ' . number_format((float) $time_end - $this->time_start, 3) . ' secs');
            }
            $i++;
        }
    }

    # Adds a collection to firestore
    # Firebase Firestore auto-generated ids
    public function add($value)
    {
        $docRef = $this->db->collection($this->collectionname);
        $docRef->add($value);
    }

    # Sets documents to a collection on firestore
    # Uses custom IDS, in this case our json object ID field
    public function set($value)
    {
        $docRef = $this->db->collection($this->collectionname)->document($value['id']);
        $docRef->set($value);
    }
}

$uploadjsonfirestore = new UploadJSONFILEFIRESTORE;
$uploadjsonfirestore->upload();

# php json-firestore/upload-json-firestore.php json-firestore/data.json set demo-users