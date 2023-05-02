# Python program implementing Image Steganography

# PIL package allows modification of pixels in an image
from PIL import Image

# Convert encryption data into 8-bit binary
# create characters using ascii from 8 bit binary provided through manipulation of pixels
def generateData(data):

		# creating a list of binary codes from
		# user inputed data, encrypted into image file
		newData = []

		for i in data:
			newData.append(format(ord(i), '08b'))
		return newData

# Pixels are modified according to the 8 bit binary
# data and returned as text when decrypted or simply stored in image file when encrypted
def modifyPixels(pixels, data):

	datalist = generateData(data)
	lendata = len(datalist)
	imageData = iter(pixels)

	for i in range(lendata):

		# Extracting 3 pixels at a time 8th bit reads 1 or 0
        # 1 allows the file to keep being read 0 tells it to stop reading
		pixels = [value for value in imageData.__next__()[:3] +
								imageData.__next__()[:3] +
								imageData.__next__()[:3]]

		# Pixel value is created
		# odd for 1 and even for 0
		for j in range(0, 8):
			if (datalist[i][j] == '0' and pixels[j]% 2 != 0):
				pixels[j] -= 1

			elif (datalist[i][j] == '1' and pixels[j] % 2 == 0):
				if(pixels[j] != 0):
					pixels[j] -= 1
				else:
					pixels[j] += 1
				

		# Eighth pixel of every set tells
		# whether to stop or read further.
		# 0 means keep reading; 1 means the
		# message is over.
		if (i == lendata - 1):
			if (pixels[-1] % 2 == 0):
				if(pixels[-1] != 0):
					pixels[-1] -= 1
				else:
					pixels[-1] += 1

		else:
			if (pixels[-1] % 2 != 0):
				pixels[-1] -= 1

		pixels = tuple(pixels)
		yield pixels[0:3]
		yield pixels[3:6]
		yield pixels[6:9]

def encrypt_enc(newImage, data):
	w = newImage.size[0]
	(x, y) = (0, 0)

	for pixel in modifyPixels(newImage.getdata(), data):

		# Putting modified pixels in the new image
		newImage.putpixel((x, y), pixel)
		if (x == w - 1):
			x = 0
			y += 1
		else:
			x += 1

# Encode data into image
# image first is opened
# calls for user input to add secret message to be encrypted
# if data is not added for encryption raise exception
# generate new image with encrypted data
# create new file with name and extension in working directory
# new image saved with encrypted data 
def encrypt():
	img = input("Enter image name including extension -> ")
	image = Image.open(img, 'r')

	data = input("Enter your secret message : ")
	if (len(data) == 0):
		raise ValueError('image empty try again')

	newImage = image.copy()
	encrypt_enc(newImage, data)

	newImageName = input("Type the name of encrypted image including extension : ")
	newImage.save(newImageName, str(newImageName.split(".")[1].upper()))

# Decode the data in the image
def decrypt():
	img = input("Type encrypted image including extension -> ")
	image = Image.open(img, 'r')

	data = ''
	imageData = iter(image.getdata())

	while (True):
		pixels = [value for value in imageData.__next__()[:3] +
								imageData.__next__()[:3] +
								imageData.__next__()[:3]]

		# recreating string of binary data. Going through the binary and reading 
        # 8 bits at a time 0 for even 1 for odd and returning the associated ascii value
		binaryString = ''

		for i in pixels[:8]:
			if (i % 2 == 0):
				binaryString += '0'
			else:
				binaryString += '1'

		data += chr(int(binaryString, 2))
		if (pixels[-1] % 2 != 0):
			return data

# Main function prompts user input to either call the encrypt or decrypt functions
# catch error for invalid user inputs
def main():
	a = int(input("~~ Welcome to Image Encryption Tool ~~\n"
						"1. Encrypt\n2. Decrypt\n"))
	if (a == 1):
		encrypt()

	elif (a == 2):
		print("secret message : " + decrypt())
	else:
		raise Exception("Enter valid input")

# Driver
if __name__ == '__main__' :

	# executing main function
	main()
