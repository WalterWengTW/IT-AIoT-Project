# -*- coding: utf-8 -*-
#********************************************************************************************
#***                                  Module Importing                                    ***
#********************************************************************************************

from darkflow.net.build import TFNet
import cv2
import numpy as np
import winsound
import tkinter as tk 
from PIL import Image, ImageTk

#********************************************************************************************
#***                                  Global Variable                                     ***
#********************************************************************************************
global center_x, center_y
global x_rate, y_rate
center_x, center_y = 320, 240
x_rate, y_rate = 0.1, 0.1



global ArrowXtop, ArrowXbtm, ArrowYtop, ArrowYbtm
ArrowXtop, ArrowXbtm, ArrowYtop, ArrowYbtm = 180, 460, 120, 360

global Ready
Ready = False

global Direct
Direct = 0

global WaveCount, Hand_Left, Hand_Right, Hand_Left_pre, Hand_Right_pre, DelayCount
WaveCount = 0
Hand_Left = 0
Hand_Right = 0
Hand_Left_pre = 0
Hand_Right_pre = 0
DelayCount = 0

#********************************************************************************************
#***                                  Function Define                                     ***
#********************************************************************************************
def NetInitialize():
    
    options = {"pbLoad": "tiny-yolo-hand-detect.pb", "threshold": 0.4, 
               "metaLoad": "tiny-yolo-hand-detect.meta", "gpu": 1.0}
    
    return TFNet(options)

def GetOnlyOneBox(predictions):
    
    MaxConfidenceSet = {'label': ' ', 'top_x': 0.0, 'top_y': 0.0, 'btm_x': 0.0, 'btm_y': 0.0, 'confidence' : 0.0}
    for result in predictions:
        if result['confidence']>MaxConfidenceSet['confidence']:
            MaxConfidenceSet['label'] = result['label']
            MaxConfidenceSet['top_x'] = result['topleft']['x']
            MaxConfidenceSet['top_y'] = result['topleft']['y']
            MaxConfidenceSet['btm_x'] = result['bottomright']['x']
            MaxConfidenceSet['btm_y'] = result['bottomright']['y']
            MaxConfidenceSet['confidence'] = round(result['confidence'], 3)

    return MaxConfidenceSet

def Detecting(Image, predictions):
    global center_x, center_y
    global ArrowXtop, ArrowXbtm, ArrowYtop, ArrowYbtm
    global Ready
    global Direct
    global WaveCount, Hand_Left, Hand_Right, Hand_Left_pre, Hand_Right_pre, DelayCount
    
    MaxConfidenceSet = GetOnlyOneBox(predictions)
    top_x, top_y = MaxConfidenceSet['top_x'], MaxConfidenceSet['top_y']
    btm_x, btm_y = MaxConfidenceSet['btm_x'], MaxConfidenceSet['btm_y']
    box_x, box_y = (top_x+btm_x)/2, (top_y+btm_y)/2  
    
    
    if Ready:
        Image = cv2.line(Image, (center_x-10,center_y), (center_x+10,center_y), (0, 255, 0), 3)
        Image = cv2.line(Image, (center_x,center_y-10), (center_x,center_y+10), (0, 255, 0), 3)

        
    else:
        Image = cv2.line(Image, (center_x-10,center_y), (center_x+10,center_y), (0, 0, 255), 3)
        Image = cv2.line(Image, (center_x,center_y-10), (center_x,center_y+10), (0, 0, 255), 3)
    
    if Direct == 1:
        Image = cv2.line(Image, (ArrowXtop,center_y), (ArrowXtop-80 ,center_y), (0, 255, 0), 5)
        Image = cv2.line(Image, (ArrowXtop-80,center_y), (ArrowXtop-80+20 ,center_y-20), (0, 255, 0), 5)
        Image = cv2.line(Image, (ArrowXtop-80,center_y), (ArrowXtop-80+20 ,center_y+20), (0, 255, 0), 5)
        
        Image = cv2.line(Image, (ArrowXbtm,center_y), (ArrowXbtm+80 ,center_y), (0, 0, 0), 5)
        Image = cv2.line(Image, (ArrowXbtm+80,center_y), (ArrowXbtm+80-20 ,center_y-20), (0, 0, 0), 5)
        Image = cv2.line(Image, (ArrowXbtm+80,center_y), (ArrowXbtm+80-20 ,center_y+20), (0, 0, 0), 5)
    
        Image = cv2.line(Image, (center_x, ArrowYtop), (center_x ,ArrowYtop-80), (0, 0, 0), 5)
        Image = cv2.line(Image, (center_x, ArrowYtop-80), (center_x-20 ,ArrowYtop-80+20), (0, 0, 0), 5)
        Image = cv2.line(Image, (center_x, ArrowYtop-80), (center_x+20 ,ArrowYtop-80+20), (0, 0, 0), 5)
    
        Image = cv2.line(Image, (center_x, ArrowYbtm), (center_x, ArrowYbtm+80), (0, 0, 0), 5)
        Image = cv2.line(Image, (center_x, ArrowYbtm+80), (center_x-20, ArrowYbtm+80-20), (0, 0, 0), 5)
        Image = cv2.line(Image, (center_x, ArrowYbtm+80), (center_x+20, ArrowYbtm+80-20), (0, 0, 0), 5)
    elif Direct == 2:
        Image = cv2.line(Image, (ArrowXtop,center_y), (ArrowXtop-80 ,center_y), (0, 0, 0), 5)
        Image = cv2.line(Image, (ArrowXtop-80,center_y), (ArrowXtop-80+20 ,center_y-20), (0, 0, 0), 5)
        Image = cv2.line(Image, (ArrowXtop-80,center_y), (ArrowXtop-80+20 ,center_y+20), (0, 0, 0), 5)
        
        Image = cv2.line(Image, (ArrowXbtm,center_y), (ArrowXbtm+80 ,center_y), (0, 255, 0), 5)
        Image = cv2.line(Image, (ArrowXbtm+80,center_y), (ArrowXbtm+80-20 ,center_y-20), (0, 255, 0), 5)
        Image = cv2.line(Image, (ArrowXbtm+80,center_y), (ArrowXbtm+80-20 ,center_y+20), (0, 255, 0), 5)
    
        Image = cv2.line(Image, (center_x, ArrowYtop), (center_x ,ArrowYtop-80), (0, 0, 0), 5)
        Image = cv2.line(Image, (center_x, ArrowYtop-80), (center_x-20 ,ArrowYtop-80+20), (0, 0, 0), 5)
        Image = cv2.line(Image, (center_x, ArrowYtop-80), (center_x+20 ,ArrowYtop-80+20), (0, 0, 0), 5)
    
        Image = cv2.line(Image, (center_x, ArrowYbtm), (center_x, ArrowYbtm+80), (0, 0, 0), 5)
        Image = cv2.line(Image, (center_x, ArrowYbtm+80), (center_x-20, ArrowYbtm+80-20), (0, 0, 0), 5)
        Image = cv2.line(Image, (center_x, ArrowYbtm+80), (center_x+20, ArrowYbtm+80-20), (0, 0, 0), 5)
    elif Direct == 3:
        Image = cv2.line(Image, (ArrowXtop,center_y), (ArrowXtop-80 ,center_y), (0, 0, 0), 5)
        Image = cv2.line(Image, (ArrowXtop-80,center_y), (ArrowXtop-80+20 ,center_y-20), (0, 0, 0), 5)
        Image = cv2.line(Image, (ArrowXtop-80,center_y), (ArrowXtop-80+20 ,center_y+20), (0, 0, 0), 5)
        
        Image = cv2.line(Image, (ArrowXbtm,center_y), (ArrowXbtm+80 ,center_y), (0, 0, 0), 5)
        Image = cv2.line(Image, (ArrowXbtm+80,center_y), (ArrowXbtm+80-20 ,center_y-20), (0, 0, 0), 5)
        Image = cv2.line(Image, (ArrowXbtm+80,center_y), (ArrowXbtm+80-20 ,center_y+20), (0, 0, 0), 5)
    
        Image = cv2.line(Image, (center_x, ArrowYtop), (center_x ,ArrowYtop-80), (0, 255, 0), 5)
        Image = cv2.line(Image, (center_x, ArrowYtop-80), (center_x-20 ,ArrowYtop-80+20), (0, 255, 0), 5)
        Image = cv2.line(Image, (center_x, ArrowYtop-80), (center_x+20 ,ArrowYtop-80+20), (0, 255, 0), 5)
    
        Image = cv2.line(Image, (center_x, ArrowYbtm), (center_x, ArrowYbtm+80), (0, 0, 0), 5)
        Image = cv2.line(Image, (center_x, ArrowYbtm+80), (center_x-20, ArrowYbtm+80-20), (0, 0, 0), 5)
        Image = cv2.line(Image, (center_x, ArrowYbtm+80), (center_x+20, ArrowYbtm+80-20), (0, 0, 0), 5)
    elif Direct == 4:
        Image = cv2.line(Image, (ArrowXtop,center_y), (ArrowXtop-80 ,center_y), (0, 0, 0), 5)
        Image = cv2.line(Image, (ArrowXtop-80,center_y), (ArrowXtop-80+20 ,center_y-20), (0, 0, 0), 5)
        Image = cv2.line(Image, (ArrowXtop-80,center_y), (ArrowXtop-80+20 ,center_y+20), (0, 0, 0), 5)
        
        Image = cv2.line(Image, (ArrowXbtm,center_y), (ArrowXbtm+80 ,center_y), (0, 0, 0), 5)
        Image = cv2.line(Image, (ArrowXbtm+80,center_y), (ArrowXbtm+80-20 ,center_y-20), (0, 0, 0), 5)
        Image = cv2.line(Image, (ArrowXbtm+80,center_y), (ArrowXbtm+80-20 ,center_y+20), (0, 0, 0), 5)
    
        Image = cv2.line(Image, (center_x, ArrowYtop), (center_x ,ArrowYtop-80), (0, 0, 0), 5)
        Image = cv2.line(Image, (center_x, ArrowYtop-80), (center_x-20 ,ArrowYtop-80+20), (0, 0, 0), 5)
        Image = cv2.line(Image, (center_x, ArrowYtop-80), (center_x+20 ,ArrowYtop-80+20), (0, 0, 0), 5)
    
        Image = cv2.line(Image, (center_x, ArrowYbtm), (center_x, ArrowYbtm+80), (0, 255, 0), 5)
        Image = cv2.line(Image, (center_x, ArrowYbtm+80), (center_x-20, ArrowYbtm+80-20), (0, 255, 0), 5)
        Image = cv2.line(Image, (center_x, ArrowYbtm+80), (center_x+20, ArrowYbtm+80-20), (0, 255, 0), 5)
    else:
        Image = cv2.line(Image, (ArrowXtop,center_y), (ArrowXtop-80 ,center_y), (0, 0, 0), 5)
        Image = cv2.line(Image, (ArrowXtop-80,center_y), (ArrowXtop-80+20 ,center_y-20), (0, 0, 0), 5)
        Image = cv2.line(Image, (ArrowXtop-80,center_y), (ArrowXtop-80+20 ,center_y+20), (0, 0, 0), 5)
        
        Image = cv2.line(Image, (ArrowXbtm,center_y), (ArrowXbtm+80 ,center_y), (0, 0, 0), 5)
        Image = cv2.line(Image, (ArrowXbtm+80,center_y), (ArrowXbtm+80-20 ,center_y-20), (0, 0, 0), 5)
        Image = cv2.line(Image, (ArrowXbtm+80,center_y), (ArrowXbtm+80-20 ,center_y+20), (0, 0, 0), 5)
    
        Image = cv2.line(Image, (center_x, ArrowYtop), (center_x ,ArrowYtop-80), (0, 0, 0), 5)
        Image = cv2.line(Image, (center_x, ArrowYtop-80), (center_x-20 ,ArrowYtop-80+20), (0, 0, 0), 5)
        Image = cv2.line(Image, (center_x, ArrowYtop-80), (center_x+20 ,ArrowYtop-80+20), (0, 0, 0), 5)
    
        Image = cv2.line(Image, (center_x, ArrowYbtm), (center_x, ArrowYbtm+80), (0, 0, 0), 5)
        Image = cv2.line(Image, (center_x, ArrowYbtm+80), (center_x-20, ArrowYbtm+80-20), (0, 0, 0), 5)
        Image = cv2.line(Image, (center_x, ArrowYbtm+80), (center_x+20, ArrowYbtm+80-20), (0, 0, 0), 5)
    if Direct != 0 and DelayCount > 0:
        DelayCount-=1
        
    
    if MaxConfidenceSet['confidence']> 0.4:
#        label = MaxConfidenceSet['label'] + " " + str(MaxConfidenceSet['confidence'])
#        Image = cv2.rectangle(Image, (top_x, top_y), (btm_x, btm_y), (255,0,0), 3)
#        Image = cv2.putText(Image, label, (top_x, top_y-5), cv2.FONT_HERSHEY_COMPLEX_SMALL , 0.8, (0, 230, 0), 1, cv2.LINE_AA)
        if (center_x > top_x and center_x < btm_x) and (center_y > top_y and center_y < btm_y):
            if not Ready and DelayCount <=0:
                winsound.PlaySound(r"./crrect_answer3.wav", winsound.SND_FILENAME|winsound.SND_ASYNC|winsound.SND_NOWAIT)
                Ready = True
                WaveCount = 0
                Direct = 0
                DelayCount = 20
        if box_x < ArrowXtop and (box_y>ArrowYtop and box_y<ArrowYbtm) and int(Ready):
            if not Direct:
                winsound.PlaySound(r"./left.wav", winsound.SND_FILENAME|winsound.SND_ASYNC|winsound.SND_NOWAIT)
                Direct = 1 #left
                Ready = False
        elif box_x > ArrowXbtm and (box_y>ArrowYtop and box_y<ArrowYbtm) and int(Ready):
            if not Direct:
                winsound.PlaySound(r"./right.wav", winsound.SND_FILENAME|winsound.SND_ASYNC|winsound.SND_NOWAIT)
                Direct = 2 #right
                Ready = False
        elif box_y < ArrowYtop and (box_x>ArrowXtop and box_x<ArrowXbtm) and int(Ready):
            if not Direct:
                winsound.PlaySound(r"./up.wav", winsound.SND_FILENAME|winsound.SND_ASYNC|winsound.SND_NOWAIT)
                Direct = 3 #top
                Ready = False
        elif box_y > ArrowYbtm and (box_x>ArrowXtop and box_x<ArrowXbtm) and int(Ready):
            if not Direct:
                winsound.PlaySound(r"./down.wav", winsound.SND_FILENAME|winsound.SND_ASYNC|winsound.SND_NOWAIT)
                Direct = 4 #bottom
                Ready = False
        else:
            Direct = Direct  
            
        if box_x < center_x-20 and int(Ready):
            Hand_Left = 1
            Hand_Right = 0
        elif box_x > center_x+20 and int(Ready):
            Hand_Left = 0
            Hand_Right = 1
        else:
            Hand_Left = 0
            Hand_Right = 0
        
        if Hand_Left != Hand_Left_pre and Hand_Left == 1 and int(Ready):
            WaveCount += 1
            Hand_Left_pre = Hand_Left
            Hand_Right_pre = Hand_Right
        if Hand_Right != Hand_Right_pre and Hand_Right == 1 and int(Ready):
            WaveCount += 1
            Hand_Left_pre = Hand_Left
            Hand_Right_pre = Hand_Right
        if WaveCount >= 4 and int(Ready):
            winsound.PlaySound(r"./NotClear.wav", winsound.SND_FILENAME|winsound.SND_ASYNC|winsound.SND_NOWAIT)
            Direct = 5
            WaveCount = 0
            Ready = False
            
    return Image



def video_loop():
    success, frame = camera.read() 
    if success:
        frame = cv2.flip(frame, 1)
        frame_pre = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_pre = cv2.cvtColor(frame_pre, cv2.COLOR_GRAY2BGR)
        result = tfnet.return_predict(frame_pre)
        frame_re = Detecting(frame,result)
        cv2image = cv2.cvtColor(frame_re, cv2.COLOR_BGR2RGBA)
        #cv2.imshow('frame',cv2image) 
        current_image = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=current_image)
        panel.imgtk = imgtk
        panel.config(image=imgtk)
        root.after(20, video_loop)

tfnet = NetInitialize()

camera = cv2.VideoCapture(1) 
cap = cv2.VideoCapture(1) 
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

root = tk.Tk()
root.title("opencv + tkinter")
root.geometry("1280x480")
#root.protocol('WM_DELETE_WINDOW', detector)

panel = tk.Label(root)  # initialize image panelq
panel.pack(padx=10, pady=10, side='right')

#root.config(cursor="arrow")



video_loop()

root.mainloop()
# 当一切都完成后，关闭摄像头并释放所占资源
camera.release()
cv2.destroyAllWindows()
