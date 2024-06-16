import tkinter as tk
from tkinter import Canvas, Button, Label, filedialog
from PIL import Image, ImageTk, ImageDraw
import numpy as np
from keras.models import load_model
import os

# Define the folder path where the model is located
model_folder_path='C:\\Users\\91970\\'
model_filename='First Model.h5'

# Load your trained model
model=load_model(os.path.join(model_folder_path,model_filename))

#Mapping dictionary for converting predicted indices to Hindi characters
hindi_mapping={
    1: "क", 2: "ख", 3: "ग", 4: "घ", 5: "ङ", 
    6: "च", 7: "छ", 8: "ज", 9: "झ", 10: "ञ",
    11: "ट", 12: "ठ", 13: "ड", 14: "ढ", 15: "ण",
    16: "त", 17: "थ", 18: "द", 19: "ध", 20: "न",
    21: "प", 22: "फ", 23: "ब", 24: "भ", 25: "म",
    26: "य", 27: "र", 28: "ल", 29: "व", 30: "श",
    31: "ष", 32: "स", 33: "ह", 34: "क्ष", 35:"त्र", 
    36: "ज्ञ", 37: "0", 38: "1", 39: "2", 40: "3",
    41: "4", 42: "5", 43: "6", 44: "7", 45: "8", 46: "9",
}

# Funtion to recognize the selected image
def recognize_image():
    #open a file dialog for selecting an image file
    file_path=filedialog.askopenfilename()
    if file_path:
        # Load the selected image
        img= Image.open(file_path)
        #resize the image to 32x32
        img_resized=img.resize((32,32))
        #convert to gray scale
        img_resized=img_resized.convert('L')
        # convert to numpy array
        img_array=np.array(img_resized)
        # normalize the image
        img_array=img_array/255.0
        # reshape to match model input shape
        img_input=img_array.reshape((1,32,32,1))
        # predict using the model
        prediction=model.predict(img_input)
        # get the predicted character index
        predicted_index=np.argmax(prediction)
        # get the predicted devanagari character
        predicted_char=hindi_mapping.get(predicted_index,'Unknown')
        # update the label with predicted character
        lb1_result.config(text="Predicted Character:"+predicted_char)
        #display the character with large font size
        lb1_predicted_char.config(text=predicted_char, font=("Helvetica",48)) # Adjust font size as needed
        #display the selected image on the canvas
        canvas.img=ImageTk.PhotoImage(img)
        canvas.create_image(0,0,anchor=tk.NW, image=canvas.img)
#create the main window
root=tk.Tk()
root.title("Devanagari Handwritten Character Recognition")
root.geometry("500x650") #set window size

#canvas for displaying selected image
canvas=Canvas(root,width=300,height=300,bg="white")
canvas.pack(expand=True, fill='both')

#Button for recognizing the selected image
btn_recognize=Button(root,text="Recognize Image",command=recognize_image)
btn_recognize.pack()

#Label for displaying result
lb1_result=Label(root,text="")
lb1_result.pack()

#label for displaying the predicted character
lb1_predicted_char=Label(root,text="",font=("Helvetica", 48))
lb1_predicted_char.pack()

root.mainloop()
