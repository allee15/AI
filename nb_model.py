# -*- coding: utf-8 -*-
"""NB_model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nmby7iy3aA_jBWhitmFn47H_fTCZgiXK
"""

#from google.colab import drive
#drive.mount('/content/drive')

#!unzip "/content/drive/MyDrive/unibuc-brain-ad.zip"


from pandas.core.dtypes.common import classes
import cv2
import numpy as np
import glob
from sklearn.naive_bayes import GaussianNB
import csv
from sklearn.preprocessing import StandardScaler
from sklearn.utils import shuffle
import os


standardScaler = StandardScaler()
#modelNB=MultinomialNB()-> 0.19
#gaussian -> 0.13
#bernoulli -> 0.233
#bernoulli, train_labels, val_labels concatenate -> 0,24
#alpha = 0.1, force_alpha=True, fit_prior=False -> fara astea -> 0,246 bernoulli
#fara hiperparam, gaussian -> 0,258
#fara hiperparam, multinomial -> 0,251
data_path = './data/data'

train_labels = np.genfromtxt('/content/data/train_labels.txt', delimiter=',', dtype='int')[1:]
train_labels = train_labels[:,1]
n_classes = len(np.unique(train_labels))
class_counts = np.bincount(train_labels)
class_priors = class_counts / len(train_labels)
modelNB =GaussianNB(priors = class_priors, var_smoothing = 0.001)

validation_labels = np.genfromtxt('/content/data/validation_labels.txt', delimiter=',', dtype='int')[1:]
validation_labels = validation_labels[:,1]

test_labels = np.genfromtxt('/content/data/sample_submission.txt', delimiter=',', dtype='int')[1:]
test_labels = test_labels[:,1]

# Extracting images in correct order
png_files = sorted(glob.glob(os.path.join(data_path, "*.png")), key=lambda x: int(os.path.basename(x).split(".")[0]))

train_images = png_files[:17000]
train_images,train_labels = shuffle(train_images,np.concatenate((train_labels, validation_labels), axis =0))

# Select a subset of the files starting from the 17001-th file
test_images = png_files[17000:]

batch_size = 100
for i in range(0, len(train_images), batch_size):
  image_batch = []
  for file in train_images[i:i+batch_size]:
    image = cv2.imread(file)
    image = image.flatten()
    image_batch.append(image) 
  norm_image_batch = standardScaler.fit_transform(image_batch) 
  modelNB.partial_fit(norm_image_batch,train_labels[i:i+batch_size], classes=[0, 1])

y_pred = []
batch_size = 50
for i in range(0, len(test_images)+1, batch_size):
  image_batch = []
  for file in test_images[i:i+batch_size]:
    image = cv2.imread(file)
    image = image.flatten()  # flatten the pixel array to a 1D vector
    image_batch.append(image)
  image_batch = standardScaler.fit_transform(image_batch)
  partialPredict = modelNB.predict(image_batch)
  y_pred.append(partialPredict) 

y_pred = np.concatenate(y_pred, axis=0)

print(np.shape(train_images), np.shape(validation_labels), np.shape(test_labels), test_images[0])

from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score

ids = np.genfromtxt('/content/data/sample_submission.txt', delimiter=',', dtype='int')[1:][:,0]

with open('nb_predictions.csv', mode='w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['id', 'class'])

    for i in range(len(test_images)):
        prediction = y_pred[i]
        writer.writerow([ids[i], prediction])
        


print("confusion matrix ",confusion_matrix(test_labels, y_pred))
print("accuracy ",accuracy_score(test_labels, y_pred))
print("precision ",precision_score(test_labels, y_pred))
print("recall score ",recall_score(test_labels, y_pred))
print("f1_score ", f1_score(test_labels, y_pred, labels=np.unique(test_labels)))

# import matplotlib.pyplot as plt
# import csv


# def calculam_l2(train_images, test_images):
#     dif = train_images - test_images
#     suma = np.sum(dif ** 2, axis=1)
#     return np.sqrt(suma)


# def calculam_l1(train_images, test_images):
#     dif = np.absolute(train_images - test_images)
#     return np.sum(dif, axis=1)


# class KnnClasifier:
#     def __init__(self, train_images, train_labels):
#         self.train_images = train_images
#         self.train_labels = train_labels

#     def classify_image(self, test_image, num_neighbors=3, metric="l2"):
#         if metric == "l2":
#             distances = calculam_l2(self.train_images, test_image)
#         else:
#             distances = calculam_l1(self.train_images, test_image)

#         knn_indici = np.argsort(distances)[:num_neighbors]
#         rez = np.bincount(self.train_labels[knn_indici])
#         return np.argmax(rez)

#     def predict(self, test_images, num_neighbors=3, metric="l2"):
#         predictions = []
#         for img in test_images:
#             img = img.reshape(-1) # Flatten the image
#             prediction = self.classify_image(img, num_neighbors=num_neighbors, metric=metric)
#             predictions.append(prediction)
#         return np.array(predictions)

#     def accuracy(self, test_images, test_labels, num_neighbors=3, metric="l2"):
#         predictions = self.predict(test_images, num_neighbors=num_neighbors, metric=metric)
#         correct = np.sum(predictions == test_labels)
#         accuracy = correct / len(test_labels) * 100
#         return accuracy

#     def f1_score(self, test_images, test_labels, num_neighbors=3, metric="l2"):
#         predictions = self.predict(test_images, num_neighbors=num_neighbors, metric=metric)
#         tp = np.sum((predictions == test_labels) & (test_labels == 1))
#         fp = np.sum((predictions != test_labels) & (predictions == 1))
#         fn = np.sum((predictions != test_labels) & (predictions == 0))
#         precision = tp / (tp + fp)
#         recall = tp / (tp + fn)
#         f1_score = 2 * precision * recall / (precision + recall)
#         return f1_score

# #test_labels = test_labels.astype(np.int)

# knn_classifier = KnnClasifier(train_images, train_labels)

# test_images_flattened = []
# for file in glob.glob("data/test/*.png"):
#     image = cv2.imread(file)
#     image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # convert to grayscale if necessary
#     image = image.flatten()  # flatten the pixel array to a 1D vector
#     test_images_flattened.append(image)

# test_images = np.array(test_images_flattened)

# with open('knn_predictions.csv', mode='w', newline='') as csv_file:
#     writer = csv.writer(csv_file)
#     writer.writerow(['id', 'prediction'])

#     for i in range(len(test_images)):
#         img_id = i + 1
#         img = test_images[i]
#         prediction = knn_classifier.classify_image(img, num_neighbors=3, metric='l2')
#         writer.writerow([img_id, prediction])


# test_accuracy = knn_classifier.accuracy(test_images, test_labels)
# test_f1_score = knn_classifier.f1_score(test_images, test_labels)

# print("Test accuracy: {:.2f}%".format(test_accuracy))
# print("Test F1 score: {:.2f}".format(test_f1_score))