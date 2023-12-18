import os
import cv2
import numpy as np
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential

# Define the base directory where the folders are located
base_dir = '../resources/Images/'

# Initialize lists to hold the images and labels
images = []
labels = []

# Loop over the folders
for folder_name in os.listdir(base_dir):
    folder_path = os.path.join(base_dir, folder_name)
    # Make sure it's a directory
    if os.path.isdir(folder_path):
        # The tag for the breed is the first section of the folder name
        breed_tag = folder_name.split('-')[0]

        # Loop over the files in the folder
        for image_file in os.listdir(folder_path):
            image_path = os.path.join(folder_path, image_file)
            # Make sure it's a file and not a directory
            if os.path.isfile(image_path):
                # Read and preprocess the image
                image = cv2.imread(image_path)
                image = cv2.resize(image, (224, 224))  # Resize the image to fit the model input
                images.append(image)
                labels.append(breed_tag)

# Convert lists to NumPy arrays
images = np.array(images)
labels = np.array(labels)

# Encode the labels into integers
label_encoder = LabelEncoder()
integer_encoded_labels = label_encoder.fit_transform(labels)
# Convert integer encoded labels to one hot encoded
one_hot_encoded_labels = to_categorical(integer_encoded_labels)

# Split the dataset into training and test sets
X_train, X_test, y_train, y_test = train_test_split(images, one_hot_encoded_labels, test_size=0.2, random_state=42)

# Define your model (this is just a placeholder, you'll need to define your actual model architecture)
model = Sequential([
    # Your model layers go here
])

# Compile your model (placeholder values, you'll need to choose the actual loss function and optimizer)
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train your model
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10)

# Evaluate your model
score = model.evaluate(X_test, y_test)
print('Test accuracy:', score[1])
