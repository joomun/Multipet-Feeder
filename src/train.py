import os
import cv2
import numpy as np
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Activation, MaxPooling2D, Flatten, Dense, Dropout


# Define the base directory where the folders are located
base_dir = './resources/Images/'

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
                print(image_path)
                image = cv2.imread(image_path)
                image = cv2.resize(image, (224, 224))  # Resize the image to fit the model input
                images.append(image)
                labels.append(breed_tag)

# Convert lists to NumPy arrays
images = np.array(images)
labels = np.array(labels)

# Normalize pixel values to be between 0 and 1
images = images / 255.0

# Encode the labels into integers
label_encoder = LabelEncoder()
integer_encoded_labels = label_encoder.fit_transform(labels)
# Convert integer encoded labels to one hot encoded
one_hot_encoded_labels = to_categorical(integer_encoded_labels)

# Split the dataset into training and test sets
X_train, X_test, y_train, y_test = train_test_split(images, one_hot_encoded_labels, test_size=0.2, random_state=42)

# The number of unique breeds
num_classes = y_train.shape[1]

print(num_classes)

# Define a simple CNN model
model = Sequential([
    Conv2D(32, (3, 3), input_shape=(224, 224, 3)),
    Activation('relu'),
    MaxPooling2D(pool_size=(2, 2)),

    Conv2D(64, (3, 3)),
    Activation('relu'),
    MaxPooling2D(pool_size=(2, 2)),

    Conv2D(128, (3, 3)),
    Activation('relu'),
    MaxPooling2D(pool_size=(2, 2)),

    Flatten(),
    Dense(512),
    Activation('relu'),
    Dropout(0.5),
    Dense(num_classes),
    Activation('softmax')
])

# Compile the model
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

# Define batch size
batch_size = 13  # You can adjust the batch size according to your system's memory

# Train the model with batch processing
model.fit(X_train, y_train, batch_size=batch_size, validation_data=(X_test, y_test), epochs=10)

# Evaluate the model
score = model.evaluate(X_test, y_test)
print('Test accuracy:', score[1])
