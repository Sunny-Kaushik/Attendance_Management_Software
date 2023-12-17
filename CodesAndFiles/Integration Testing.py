import unittest
import firebase_admin
from firebase_admin import credentials, db,storage

class TestFirebaseIntegration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Initialize Firebase app for testing
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(
            cred, {'databaseURL': "https://faceattendancerealtime-df07b-default-rtdb.firebaseio.com/",
                   'storageBucket':"faceattendancerealtime-df07b.appspot.com" })
    def test_upload_and_download_image(self):
            # Reference to the Firebase Storage bucket
            bucket = storage.bucket()

            # Specify the path to the image in Firebase Storage
            image_path = "Images/test_image.jpg"

            # Upload a test image to Firebase Storage
            local_image_path = "Testing Resources/test_image.jpg"
            blob = bucket.blob(image_path)
            blob.upload_from_filename(local_image_path)

            # Download the uploaded image from Firebase Storage
            downloaded_image_path = "Images/test_image.jpg"
            blob.download_to_filename(downloaded_image_path)

            # Perform assertions based on the downloaded image data
            self.assertTrue(blob.exists())  # Check if the blob (image) exists in Firebase Storage
            self.assertTrue(blob.size > 0)   # Check if the uploaded image has non-zero size
           

    def test_data_insertion(self):
        # Reference to the 'Students' node
        ref = db.reference('Students')

        # Data to be inserted
        data = {
            "987654": {
                "name": "John Doe",
                "major": "Computer Science",
                "starting_year": 2019,
                "total_attendance": 15,
                "standing": "A",
                "year": 3,
                "last_attendance_time": "2023-12-01 12:00:00"
            }
        }

        # Insert data into Firebase
        for key, value in data.items():
            ref.child(key).set(value)

        # Retrieve the inserted data from Firebase
        retrieved_data = ref.get()

        # Check if the inserted data is present in the retrieved data
        self.assertIn("987654", retrieved_data)
        self.assertEqual(data["987654"], retrieved_data["987654"])

    @classmethod
    def tearDownClass(cls):
        # Clean up (delete test data)
        ref = db.reference('Students')
        ref.child("987654").delete()
        
        # Reference to the Firebase Storage bucket
        bucket = storage.bucket()

        # Specify the path to the image in Firebase Storage
        image_path = "Images/test_image.jpg"

        # Delete the uploaded test image from Firebase Storage
        blob = bucket.blob(image_path)
        blob.delete()

if __name__ == '__main__':
    unittest.main()
