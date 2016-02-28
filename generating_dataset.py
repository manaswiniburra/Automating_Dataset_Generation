import os
import subprocess
import re
import numpy as np
from StringIO import StringIO
import pickle

WRITE_DIR ="/home/aditya/Desktop/CCBDNeuralNetworks/Training_Data"
OPENSMILE_DIR = "/home/aditya/CCBD_Sound_Internship/openSMILE-2.1.0/bin/linux_x64_standalone_static"

# Populates the dummy final.arff file
def populate_finalfile(filename):
	f = open(filename, 'w')
	f.write('@relation (null)\n\n@attribute pcm_fftMag_mfcc[1] numeric\n@attribute pcm_fftMag_mfcc[2] numeric\n@attribute pcm_fftMag_mfcc[3] numeric\n@attribute pcm_fftMag_mfcc[4] numeric\n@attribute pcm_fftMag_mfcc[5] numeric\n@attribute pcm_fftMag_mfcc[6] numeric\n@attribute pcm_fftMag_mfcc[7] numeric\n@attribute pcm_fftMag_mfcc[8] numeric\n@attribute pcm_fftMag_mfcc[9] numeric\n@attribute pcm_fftMag_mfcc[10] numeric\n@attribute pcm_fftMag_mfcc[11] numeric\n@attribute pcm_fftMag_mfcc[12] numeric\n@attribute pcm_LOGenergy numeric\n@attribute pcm_fftMag_mfcc_de[1] numeric\n@attribute pcm_fftMag_mfcc_de[2] numeric\n@attribute pcm_fftMag_mfcc_de[3] numeric\n@attribute pcm_fftMag_mfcc_de[4] numeric\n@attribute pcm_fftMag_mfcc_de[5] numeric\n@attribute pcm_fftMag_mfcc_de[6] numeric\n@attribute pcm_fftMag_mfcc_de[7] numeric\n@attribute pcm_fftMag_mfcc_de[8] numeric\n@attribute pcm_fftMag_mfcc_de[9] numeric\n@attribute pcm_fftMag_mfcc_de[10] numeric\n@attribute pcm_fftMag_mfcc_de[11] numeric\n@attribute pcm_fftMag_mfcc_de[12] numeric\n@attribute pcm_LOGenergy_de numeric\n@attribute pcm_fftMag_mfcc_de_de[1] numeric\n@attribute pcm_fftMag_mfcc_de_de[2] numeric\n@attribute pcm_fftMag_mfcc_de_de[3] numeric\n@attribute pcm_fftMag_mfcc_de_de[4] numeric\n@attribute pcm_fftMag_mfcc_de_de[5] numeric\n@attribute pcm_fftMag_mfcc_de_de[6] numeric\n@attribute pcm_fftMag_mfcc_de_de[7] numeric\n@attribute pcm_fftMag_mfcc_de_de[8] numeric\n@attribute pcm_fftMag_mfcc_de_de[9] numeric\n@attribute pcm_fftMag_mfcc_de_de[10] numeric\n@attribute pcm_fftMag_mfcc_de_de[11] numeric\n@attribute pcm_fftMag_mfcc_de_de[12] numeric\n@attribute pcm_LOGenergy_de_de numeric\n\n@data\n\n')
	f.close()

# Finds the number of instances in the given arff file
def getNumInstances(filename):
	# Method to get the number of instances in a given arff file
	num = 0
	s = "java -cp /usr/share/java/weka.jar weka.core.Instances "+filename
	out = subprocess.check_output(s, shell=True)
	out_str = out.decode('utf-8')
	m = re.search(r'(Num Instances:)?(\d+).*', out_str)
	if (m):
		print m.group(0)
		num = int(m.group(2))
	else:
		print "Could not generate the number of instances"
		print "Number of instances : " + str(out_str)

	return num

# Generates plain text file from the file containing arff attributes
def generate_plaintext(file_to_read, file_to_write):
	f1 = open(file_to_read, 'r')
	f2 = open(file_to_write, 'w')

	line = f1.readline()
	while line != '@data'+'\n':
		line = f1.readline()
	f1.readline()

	lines = f1.readlines() 		# Reads all lines till end of file
	for line in lines:
		f2.write(line)

	# Close the files
	f1.close()
	f2.close()

# Merges all final.arff files
def merge_arff(filenames):
	# Method to append the contents of all the files seen in filenames
	i = 1
	os.system("touch " + WRITE_DIR+"/final/TEMP_FINAL.arff")
	for file_name in filenames:
		if (os.stat(file_name).st_size==0):
			continue
		if (i==1):
			os.system("cat " + file_name + " > " + WRITE_DIR+"/final/FINAL.arff")
		else:
			os.system("java -cp /usr/share/java/weka.jar weka.core.Instances append " + WRITE_DIR+"/final/FINAL.arff " + file_name + " > " + WRITE_DIR+"/final/TEMP_FINAL.arff")
			os.system("cat " + WRITE_DIR+"/final/TEMP_FINAL.arff > " + WRITE_DIR+"/final/FINAL.arff")
		i += 1

# Replaces the commas in the file with spaces
def create_commalessFile(filename, commalessFile):
	with open(filename, 'r') as data:
		plaintext = data.read()

	plaintext = plaintext.replace(',', ' ')
	os.system("touch " + commalessFile)
	ftw = open(commalessFile, 'w')
	for line in plaintext:
		ftw.write(line)

# Creates a numpy ndarray from the file
def create_ndarray(filename):
	with open(filename, 'r') as data:
		plaintext = data.read()
	c = StringIO(plaintext)
	num_array = np.loadtxt(c, dtype='float')		# Create numpy array
	return num_array

# Populates an array with list_instances ocurring
def create_output(list_instances, list_nominal):
	num_arr = np.full(list_instances[0], list_nominal[0])
	i = 1
	while i < len(list_instances):
		num_arr = np.concatenate((num_arr, np.full(list_instances[i], list_nominal[i])))
		i += 1
	return num_arr

'''def merge_arff(files):
	for file_name in files:
		print(file_name)'''

def load_data():
	print("Neural Network Training")
	list_sounds = []		# Directories of sound containing wav files
	list_arff = []			# 
	list_sound_types = []	# Type of the sound
	list_nominal = []		# Output neuron value in the Neural Network
	list_instances = []		# Number of instances in final.arff files
	list_finals = []		# final.arff files for all the directories

	number_dirs = int(input("Enter the number of sound sources for training : "))
	for i in range(number_dirs):
		sound_dir = input("Enter the path of the sound directory : ")
		sound_type = input("Enter the type of the sound : ")
		nominal_value = int(input("Enter the output neuron value in Neural Network : "))

		list_sounds.append(sound_dir) 		# Hardcode all the directories
		list_sound_types.append(sound_type)	# Hardcode all the sound types
		list_nominal.append(nominal_value) 	# Output neuron value in Neural Network
		list_arff.append(WRITE_DIR+"/"+sound_type+"_output")

		# Make the output directory -> stores all the arff files
		os.system("mkdir " + WRITE_DIR+"/"+sound_type+"_output")

		# Iterate through all the .wav files in the sound directory
		print("Generating MFCCs. Please Wait ... ")
		j = 1
		for dir_path, dirnames, files in os.walk(sound_dir):
			for filename in files:
				# Get the absolute path of the wav file
				file_path = sound_dir+"/"+filename

				string = OPENSMILE_DIR+"/SMILExtract -C " + OPENSMILE_DIR+"/MFCC12_E_D_A.conf -I " + file_path + " -O " + WRITE_DIR + "/" + sound_type+"_output/arff"+str(j)+".arff"
				os.system(string)		# Creates the arff file for the sound file

				j += 1
		print("Combining files. Please Wait .... ")

		# Create the directory to store the final.arff and final_temp.arff files
		print("Creating Directory for storing final.arff file")
		os.system("mkdir " + WRITE_DIR+"/"+sound_type+"_final")

		# Creates a dummy final.arff file
		os.system("touch " + WRITE_DIR+"/"+sound_type+"_final/final.arff")
		populate_finalfile(WRITE_DIR+"/"+sound_type+"_final/final.arff")

		# Iteratively process all files and combine / merge into final.arff file
		for dir_path, dirnames, filenames in os.walk(WRITE_DIR+"/"+sound_type+"_output"):
			for filename in filenames:
				string = "java -cp /usr/share/java/weka.jar weka.core.Instances append " + WRITE_DIR+"/"+sound_type+"_output/"+filename + " " + WRITE_DIR+"/"+sound_type+"_final/final.arff > " + WRITE_DIR+"/"+sound_type+"_final/final_temp.arff"
				os.system(string)
				string = "cat " + WRITE_DIR+"/"+sound_type+"_final/final_temp.arff > " + WRITE_DIR+"/"+sound_type+"_final/final.arff"
				os.system(string)

		list_finals.append(WRITE_DIR+"/"+sound_type+"_final/final.arff")

		# Remove the final_temp.arff file
		os.system("rm " + WRITE_DIR+"/"+sound_type+"_final/final_temp.arff")

		# Calculates the number of instances in the final.arff file
		num_instances = getNumInstances(WRITE_DIR+"/"+sound_type+"_final/final.arff")
		list_instances.append(num_instances)

		print("Done generating Datasets for training")


	# Merge the contents of all the final.arff files (for all the directories)
	os.system("mkdir " + WRITE_DIR+"/final")		# Contains the merged final file
	
	# Merges the contents of the final files in the order in which they were added
	merge_arff(list_finals)

	# A plain text file without the arff attributes is generated
	generate_plaintext(WRITE_DIR+"/final/FINAL.arff", WRITE_DIR+"/final/FINAL")

	# Create a file without the commas from the final file
	file_commaless = create_commalessFile(WRITE_DIR+"/final/FINAL", WRITE_DIR+"/final/FINAL_PLAIN")

	# Create a numpy.ndarray from file_commaless
	ndarray_input = create_ndarray(WRITE_DIR+"/final/FINAL_PLAIN")

	# Generate the result of each instance 
	ndarray_result = create_output(list_instances, list_nominal)

	# Create a tuple consisting of ndarray_input, ndarray_result
	# Training data is prepared in a similar format as the mnist dataset
	training_data = (ndarray_input, ndarray_result)

	# return training_data

	# Pickle training_data for later use in testing
	pickle.dump(training_data, open(WRITE_DIR+"/"+"training_data.pkl", "wb"))