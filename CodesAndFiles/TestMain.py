import unittest
import face_recognition

class FaceRecognitionTest(unittest.TestCase):

    def setUp(self):
        # Load the known face encodings
        known_faces = face_recognition.load_image_file('Testing Resources/known.png')
        self.known_face_encoding = face_recognition.face_encodings(known_faces)[0]

    def test_detect_face(self):
        # Load an image containing a face
        image = face_recognition.load_image_file('Testing Resources/Test face.jpg')

        # Detect the face in the image
        face_locations = face_recognition.face_locations(image)

        # Check that a face was detected
        self.assertEqual(len(face_locations), 1)

    def test_identify_face(self):
        # Load an image containing a known face
        image = face_recognition.load_image_file('Testing Resources/Test face.jpg')

        # Detect the face in the image
        face_locations = face_recognition.face_locations(image)

        # Encode the face
        face_encoding = face_recognition.face_encodings(image, face_locations)[0]

        # Compare the face encoding to the known face encoding
        is_match = face_recognition.compare_faces([self.known_face_encoding], face_encoding)

        # Check that the face was correctly identified
        self.assertTrue(is_match[0])

if __name__ == '__main__':
    unittest.main()