
# Auto Attendance System by Face Recognition

Auto Attendance System using real time face recognition is designed to collect and manage student’s attendance records by taking pictures from camera devices installed in a class room. Based on the verification of students facial identification in the cameras, attendance will be updated in data base.


## Requirements & Libraries

* Desktop development with C++
* cmake
* dlib
* face_recognition
* numpy
* opencv-python
* tkinter
* sqlite3
## Detection & Recognition

Although many face recognition algorithms have been developed over the years, their speed and accuracy balance has not been optimal. But some recent advancements have shown promise. A good example is Facebook, where they are able to tag you and your friends with just a few images of training and with accuracy as high as 98%. So how does this work? Today we will try to replicate similar results using a face recognition library developed by Adam Geitgey. Let's look at the 4 problems he explained in his article.

#### Face recognition is a series of several problems:

* First, look at a picture and find all the faces in it
* Second, focus on each face and be able to understand that even if a face is turned in a weird direction or in bad lighting, it is still the same person.
* Third, be able to pick out unique features of the face that you can use to tell it apart from other people— like how big the eyes are, how long the face is, etc.
* Finally, compare the unique features of that face to all the people you already know to determine the person’s name.

#### Find Faces Locations and Encodings

We will use the proper functionality of the face recognition library. First, we will find the faces in our images. This is done using HOG (Histogram of Oriented Gradients) at the backend. Once we have the face they are warped to remove unwanted rotations. Then the image is fed to a pre-trained neural network that outputs 128 measurements that are unique to that particular face. The parts that the model measures are not known as this is what the model learns by itself when it was trained.

#### Compare Faces and Find Distance

Once we have the encodings for both faces, then we can compare these 128 measurements of these two faces to find similarities. Compare the package uses one of the most common machine learning methods linear SVM classifier. We can use the compare_faces function to find if the faces match. This function returns True or False. Similarly, we can use the face_distance function to find how likely the faces match in terms of numbers. This is helpful particularly when there are multiple faces to detect from.
## Screenshots

#### Home
![App Screenshot](https://github.com/sydtanvirali/Auto-Attendance-System-by-Face-Recognition/blob/main/Screenshots/homepage.jpg?raw=true)

#### Attendance Report
![App Screenshot](https://github.com/sydtanvirali/Auto-Attendance-System-by-Face-Recognition/blob/main/Screenshots/attendance.jpg?raw=true)

#### Student Registration
![App Screenshot](https://github.com/sydtanvirali/Auto-Attendance-System-by-Face-Recognition/blob/main/Screenshots/registerstudent.jpg?raw=true)

#### Add Lecture
![App Screenshot](https://github.com/sydtanvirali/Auto-Attendance-System-by-Face-Recognition/blob/main/Screenshots/addlecture.jpg?raw=true)

#### Student List
![App Screenshot](https://github.com/sydtanvirali/Auto-Attendance-System-by-Face-Recognition/blob/main/Screenshots/studentlist.jpg?raw=true)

#### Lecture List
![App Screenshot](https://github.com/sydtanvirali/Auto-Attendance-System-by-Face-Recognition/blob/main/Screenshots/lecturelist.jpg?raw=true)

#### Face Detection
![App Screenshot](https://github.com/sydtanvirali/Auto-Attendance-System-by-Face-Recognition/blob/main/Screenshots/detection.jpg?raw=true)

