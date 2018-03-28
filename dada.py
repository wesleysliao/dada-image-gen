import face_recognition
from PIL import Image, ImageDraw, ImageOps, ImageTk
from os import listdir
from random import randint
import tkinter
import time
from sys import exit

def keypress(event):
	exit();

def showPIL(pilImage):
    root = tkinter.Toplevel()
    w, h = 900, 900#root.winfo_screenwidth(), root.winfo_screenheight()
    root.overrideredirect(1)
    root.geometry("%dx%d+0+0" % (w, h))
    root.focus_set()    
    root.bind("<Key>", keypress)
    canvas = tkinter.Canvas(root,width=w,height=h)
    canvas.pack()
    canvas.configure(background='black')
    imgWidth, imgHeight = pilImage.size
    if imgWidth > w or imgHeight > h:
        ratio = min(w/imgWidth, h/imgHeight)
        imgWidth = int(imgWidth*ratio)
        imgHeight = int(imgHeight*ratio)
        pilImage = pilImage.resize((imgWidth,imgHeight), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(pilImage)
    imagesprite = canvas.create_image(w/2,h/2,image=image)
    root.update()
    
class FaceImage:
	def __init__(self, imagepath, crop, croppadding = 0.0):
		imagearray = face_recognition.load_image_file(imagepath)
		self.image = Image.fromarray(imagearray)

		location = face_recognition.face_locations(imagearray)

		if len(location)>0:
			faceindex = randint(0, len(location)-1)
			if crop:
				width = abs(location[faceindex][0]-location[faceindex][2])
				height = abs(location[faceindex][1]-location[faceindex][3])
				self.face_location = (int(width*croppadding),
									  int(height*croppadding),
									  width+int(width*croppadding),
									  height+int(height*croppadding))

				location = ( location[faceindex][3]-int(width*croppadding),
						 location[faceindex][0]-int(height*croppadding),
						 location[faceindex][1]+int(width*croppadding),
						 location[faceindex][2]+int(height*croppadding))
				self.image = self.image.crop(location)
			else:
				location = (location[faceindex][3], location[faceindex][0], location[faceindex][1], location[faceindex][2])
				self.face_location = location
		else:
			self.face_location = (0,0,self.image.size[0], self.image.size[1])

		self.face_w = abs(self.face_location[0] - self.face_location[2])
		self.face_h = abs(self.face_location[1] - self.face_location[3])

bgfiles = listdir('./photos')
facefiles = listdir('./faces')


img = Image.new('L', (10,10), 0)

while(1):
	showPIL(img)
	
	bgfile = bgfiles[randint(0, len(bgfiles)-1)]

	orig_image = face_recognition.load_image_file('./photos/'+bgfile)
	orig_face_locations = face_recognition.face_locations(orig_image, number_of_times_to_upsample=2)

	num_faces = len(orig_face_locations)

	faces =[]
	for i in range(len(orig_face_locations)):
		faces.append(FaceImage('./faces/'+facefiles[randint(0, len(facefiles)-1)], True, croppadding = 0.25))

	background = Image.fromarray(orig_image)

	background = background.convert("RGBA")
	d = ImageDraw.Draw(background)

	if num_faces>0:
		for i in range(num_faces):
			location = orig_face_locations[i]
			face = faces[i]

			face_loc = (location[3],location[0],location[1],location[2])
			# d.rectangle(face_loc, fill=255)
			orig_face_w = abs(face_loc[0] - face_loc[2])
			orig_face_h = abs(face_loc[1] - face_loc[3])

			copyface = face.image.resize((int(face.image.size[0]*(orig_face_w/face.face_w)),int(face.image.size[1]*(orig_face_h/face.face_h))), Image.ANTIALIAS)

			offset = (face_loc[0]-int(face.face_location[0]*(orig_face_w/face.face_w)), face_loc[1]-int(face.face_location[1]*(orig_face_h/face.face_h)))

			background.paste(copyface, offset)
	# background.show()

	background.save("./out/"+str(randint(1000000,9999999))+".png")
	showPIL(background)
	time.sleep(6)