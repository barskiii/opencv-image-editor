from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from sys import exit as wexit
from os import remove, path
from random import randrange
import numpy as np
import cv2

class Root(Tk):

	def __init__(self):
		super(Root, self).__init__()
		#self.title = "Slike"
		self.minsize(1000, 500) 
		self.maxsize(1000, 500)
		self.canvas = Canvas(self, height=500, width=1000)
		self.canvas.pack()
		self.frame = Frame(self)
		self.frame.place(relwidth=1, relheight=1)
		self.filename = None
		self.newImage = None
		self.newImageSetted = 0
		self.randInt = randrange(1, 1000)
		self.n = 0

		self.browse()
		self.showOptions()
		self.empty_image_label()

	def showOptions(self):
		self.newXY()
		self.resetBtn()
		self.saveBtn()
		self.invertBtn()
		self.sepiaBtn()
		self.grayBtn()
		self.coldBtn()
		self.blackWhiteBtn()
		self.rotateBtn()
		self.blurButton()
		self.sharpButton()
		self.showCrop()


##############################################################################################################################
##############################################################################################################################
	def empty_image_label(self):
		self.imageLabel = Label(self.frame, bg="#DADADA")
		self.imageLabel.pack()
		self.imageLabel.place(x=20, y=70, width=720, height=405)


	def browse(self):
		# Label za browse button
		self.openFileLabel = Label(self.frame, text="Open image")
		self.openFileLabel.pack()
		self.openFileLabel.place(x=20, y=10)

		# Browse button
		self.openFileButton = Button(self.frame, text="Browse", command= self.openImage)
		self.openFileButton.pack()
		self.openFileButton.place(x=20, y=30)


	def openImage(self):
		if (self.filename == None):

			self.filename = filedialog.askopenfilename(initialdir="/", title="Izaberite sliku", filetype=(("jpeg", "*.jpg"), ("PNG", "*.png"), ("All files", "*.*")) )
			self.nFilename, self.file_extension = path.splitext(self.filename)

			self.newImage = "new_image_" + str(self.randInt) + self.file_extension
			

		self.tmpFile = self.createTmpImage()
		self.showImage()
		self.showSize()

	def createTmpImage(self):
		if (self.newImageSetted == 0):
			self.img = cv2.imread(self.filename)
			self.newImageSetted = 1
			cv2.imwrite(self.newImage, self.img)
			self.img = cv2.imread(self.newImage)
		else: 
			self.img = cv2.imread(self.newImage)

		if(self.img.shape[1] > self.img.shape[0]):

			rsp = 720 / self.img.shape[1] * 100
			width = 720
			height = int(self.img.shape[0] * rsp / 100)
		else:

			rsp = 360 / self.img.shape[0] * 100
			height = 360
			width = int(self.img.shape[1] * rsp / 100)
		
		dim = (width, height)

		resized = cv2.resize(self.img, dim, interpolation = cv2.INTER_AREA)

		cv2.imwrite('tmp' + self.file_extension, resized)

		return 'tmp' + self.file_extension


	def showImage(self):
		self.pilImage = Image.open(self.tmpFile)
		self.image = ImageTk.PhotoImage(self.pilImage)
		self.imageLabel = Label(self.frame, image=self.image)
		self.imageLabel.pack()
		self.imageLabel.place(x=20, y=70, width=720)


	def showSize(self):
		self.showXY = "Width: " + str(self.img.shape[1]) + "px       Height: " + str(self.img.shape[0]) + "px"
		self.x = Label(self.frame, text=self.showXY)
		self.x.pack()
		self.x.place(x=20, y=480)


##########################################################################################################################
##########################################################################################################################



	def showCrop(self):
		self.crop_ico = PhotoImage(file="icons/crop.png")

		self.cropLabel = Label(self.frame, text="Cut")
		self.cropLabel.pack()
		self.cropLabel.place(x=400, y=15)

		self.cropBtn = Button(self.frame, image=self.crop_ico, bg="white", command=self.cropDialog)
		self.cropBtn.pack()
		self.cropBtn.place(x=380, y=35, width=80)

	def cropDialog(self):
		self.newC = Toplevel(self)

		self.fromX_l = Label(self.newC, text="From x-axis spot")
		self.fromX_l.pack()
		self.fromX_l.place(x=5, y=10)

		self.fromX_e = Entry(self.newC)
		self.fromX_e.pack()
		self.fromX_e.place(x=5, y=30, width=60)

		self.fromY_l = Label(self.newC, text="From y-axis spot")
		self.fromY_l.pack()
		self.fromY_l.place(x=5, y=50)

		self.fromY_e = Entry(self.newC)
		self.fromY_e.pack()
		self.fromY_e.place(x=5, y=70, width=60)

		self.toX_l = Label(self.newC, text="To x-axis spot")
		self.toX_l.pack()
		self.toX_l.place(x=70, y=10)

		self.toX_e = Entry(self.newC)
		self.toX_e.pack()
		self.toX_e.place(x=70, y=30, width=60)

		self.toY_l = Label(self.newC, text="To y-axis spot")
		self.toY_l.pack()
		self.toY_l.place(x=70, y=50)
		self.toY_e = Entry(self.newC)
		self.toY_e.pack()
		self.toY_e.place(x=70, y=70, width=60)

		self.cropD = Button(self.newC, text="Apply", bg="white", command=self.crop)
		self.cropD.pack()
		self.cropD.place(x=5, y=100, width=130)

	def crop(self):
		from_w = int(self.fromX_e.get())
		to_w = int(self.toX_e.get())

		from_h = int(self.fromY_e.get())
		to_h = int(self.toY_e.get())

		cropped = self.img[int(from_h):int(to_h), int(from_w):int(to_w)]

		cv2.imwrite(self.newImage, cropped)
		self.openImage()


###########################################################################################################################

	def sharpButton(self):
		self.sharp_ico = PhotoImage(file="icons/sharp.png")

		self.sharpLabel = Label(self.frame, text="Sharp")
		self.sharpLabel.pack()
		self.sharpLabel.place(x=490, y=15)

		self.sharpBtn = Button(self.frame, image=self.sharp_ico, bg="white", command=self.sharp)
		self.sharpBtn.pack()
		self.sharpBtn.place(x=470, y=35, width=80)

	def sharp(self):
		self.n = self.n + 1

		kernel_sharpening = np.array([[-1,-1,-1], 
                            		[-1, 9, -1],
                            		[-1,-1,-1]])

		sharp = cv2.filter2D(self.img, -2, kernel_sharpening)
		cv2.imwrite(self.newImage, sharp)
		self.openImage()

###########################################################################################################################

	def blurButton(self):
		self.blur_ico = PhotoImage(file="icons/blur.png")

		self.blurLabel = Label(self.frame, text="Blur")
		self.blurLabel.pack()
		self.blurLabel.place(x=580, y=15)

		self.blurBtn = Button(self.frame, image=self.blur_ico, bg="white", command=self.blur)
		self.blurBtn.pack()
		self.blurBtn.place(x=560, y=35, width=80)

	def blur(self):
		blur = cv2.blur(self.img, (5, 5))
		cv2.imwrite(self.newImage, blur)
		self.openImage()

###########################################################################################################################

	def rotateBtn(self):
		self.rotate_ico = PhotoImage(file="icons/rotate.png")

		self.rotateLabel = Label(self.frame, text="Rotate")
		self.rotateLabel.pack()
		self.rotateLabel.place(x=680, y=15)

		self.rotateOpn = Button(self.frame, image=self.rotate_ico, bg="white", command=self.rotateDialog)
		self.rotateOpn.pack()
		self.rotateOpn.place(x=660, y=35, width=80)

	def rotateDialog(self):
		self.newR = Toplevel(self)
		self.display = Label(self.newR, text="Rotate for *degrees*:")
		self.display.pack()

		self.rotateDig = Entry(self.newR)
		self.rotateDig.pack()

		self.rotateDeg = Button(self.newR, text="Apply", bg="white", command=self.rotate)
		self.rotateDeg.pack()


	def rotate(self):
		image_h, image_w = self.img.shape[:2]
		image_center = (image_w / 2, image_h / 2)

		rotation_mat = cv2.getRotationMatrix2D(image_center, int(self.rotateDig.get()), 1.)

		abs_cos = abs(rotation_mat[0, 0])
		abs_sin = abs(rotation_mat[0, 1])

		bound_w = int(image_h * abs_sin + image_w * abs_cos)
		bound_h = int(image_h * abs_cos + image_w * abs_sin)

		rotation_mat[0, 2] += bound_w / 2 - image_center[0]
		rotation_mat[1, 2] += bound_h / 2 - image_center[1]

		rotated = cv2.warpAffine(self.img, rotation_mat, (bound_w, bound_h))
		cv2.imwrite(self.newImage, rotated)
		self.openImage()
	
###########################################################################################################################

	def newXY(self):
		self.resize_ico = PhotoImage(file="icons/resize.png")

		self.sirinaLabel = Label(self.frame, text="Width: ")
		self.sirinaLabel.pack()
		self.sirinaLabel.place(x=750, y=60)
		
		self.newX = Entry(self.frame)
		self.newX.pack()
		self.newX.place(x=750, y=80, width=220)

		self.visinaLabel = Label(self.frame, text="Height: ")
		self.visinaLabel.pack()
		self.visinaLabel.place(x=750, y=100)
		
		self.newY = Entry(self.frame)
		self.newY.pack()
		self.newY.place(x=750, y=120, width=220)

		self.resize = Button(self.frame, image=self.resize_ico, bg="white", command=self.setXY)
		self.resize.pack()
		self.resize.place(x=750, y=140, width=220, height=24)

	def setXY(self):
		try:
			dim = (int(self.newX.get()), int(self.newY.get()))

			resized = cv2.resize(self.img, dim, interpolation = cv2.INTER_AREA)

			cv2.imwrite(self.newImage, resized)

			self.openImage()

		except:
			pass

	
###########################################################################################################################
###########################################################################################################################

	def invertBtn(self):
		self.invert = Button(self.frame, text="Negative", bg="white", command=self.invert)
		self.invert.pack()
		self.invert.place(x=750, y=200, width=110)

	def sepiaBtn(self):
		self.sepia = Button(self.frame, text="Sepia", bg="white", command=self.sepia)
		self.sepia.pack()
		self.sepia.place(x=860, y=200, width=110)

	def grayBtn(self):
		self.gray = Button(self.frame, text="Grey", bg="white", command=self.gray)
		self.gray.pack()
		self.gray.place(x=750, y=226, width=110)

	def coldBtn(self):
		self.cold = Button(self.frame, text="Cold", bg="white", command=self.cold)
		self.cold.pack()
		self.cold.place(x=860, y=226, width=110)

	def blackWhiteBtn(self):
		self.bnw = Button(self.frame, text="Black and white", bg="white", command=self.blackWhite)
		self.bnw.pack()
		self.bnw.place(x=750, y=252, width=220)

###########################################################################################################################

	def invert(self):
		self.invertOn = cv2.bitwise_not(self.img)
		cv2.imwrite(self.newImage, self.invertOn)
		self.openImage()

	def sepia(self, intensity=0.8):
		image = cv2.cvtColor(self.img, cv2.COLOR_BGR2BGRA)
		image_h, image_w, image_c = image.shape
		sepia_bgra = (20, 66, 112, 1)
		overlay = np.full((image_h, image_w, 4), sepia_bgra, dtype='uint8')
		cv2.addWeighted(overlay, intensity, image, 1.0, 0, image)

		cv2.imwrite(self.newImage, image)
		self.openImage()

	def gray(self):
		image = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
		cv2.imwrite(self.newImage, image)
		self.openImage()

	def cold(self, intensity=0.5):
		image = cv2.cvtColor(self.img, cv2.COLOR_BGR2BGRA)
		image_h, image_w, image_c = image.shape
		cold_bgra = (112, 66, 20, 1)
		overlay = np.full((image_h, image_w, 4), cold_bgra, dtype='uint8')
		cv2.addWeighted(overlay, intensity, image, 1.0, 0, image)

		cv2.imwrite(self.newImage, image)
		self.openImage()

	def blackWhite(self):
		grayimage = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
		(thresh, image) = cv2.threshold(grayimage, 127, 255, cv2.THRESH_BINARY)

		cv2.imwrite(self.newImage, image)
		self.openImage()

###########################################################################################################################
###########################################################################################################################

	def resetBtn(self):
		self.reset_ico = PhotoImage(file="icons/reset.png")

		self.reset = Button(self.frame, image=self.reset_ico, bg="white", command=self.reset)
		self.reset.pack()
		self.reset.place(x=750, y=465, width=110)

	def saveBtn(self):
		self.save_ico = PhotoImage(file="icons/save.png")

		self.save = Button(self.frame, image=self.save_ico, bg="white", command=self.saveImage)
		self.save.pack()
		self.save.place(x=860, y=465, width=110)

	def reset(self):
		if (self.filename != None):
			self.newImageSetted = 0
			self.openImage()

	def saveImage(self):
		cv2.imwrite(self.filename, self.img)

###########################################################################################################################

	def close_window(self):
		try:
			remove('tmp' + self.file_extension)
			remove(self.newImage)
			wexit()
		except:
			wexit()



if __name__ == "__main__":
	root = Root()
	root.protocol("WM_DELETE_WINDOW", root.close_window)
	root.mainloop()