# -*- coding: UTF-8 -*-
import os
import numpy as np

from keras.applications.imagenet_utils import preprocess_input
from keras.models import load_model
from utils import RotNetDataGenerator, angle_error


class Analyze():

	def __init__(self):
		pass

	def loadModel(self):
		print('Loading model...')
		model_location = load_model("./models/rotnet_street_view_resnet50_keras2.hdf5",
		                            custom_objects={'angle_error': angle_error}, compile=False)
		return model_location

	def rotateVerificationCode(self, model, input_path,
	                           batch_size=64, crop=True):
		image_paths = [input_path]
		predictions = model.predict_generator(
			RotNetDataGenerator(
				image_paths,
				input_shape=(224, 224, 3),
				batch_size=batch_size,
				one_hot=True,
				preprocess_func=preprocess_input,
				rotate=False,
				crop_largest_rect=True,
				crop_center=True
			),
			verbose=1
		)

		predicted_angles = np.argmax(predictions, axis=1)
		print(predicted_angles)
		return predicted_angles
