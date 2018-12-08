from firebase import firebase
import cv2
import threading
import time
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import time
from functools import partial


#streamimg : x = 642 y= 482

#전역변수들
videoframe = None

#root gui
root = Tk()
root.title("너의 음식이 보여")
root.geometry('900x482')
root.resizable(width = False, height = False)

Login_frame = Frame(root,width = 900, height = 482)
Guest_frame = Frame(root,width = 900, height = 482)
Admin_frame = Frame(root,width = 900, height = 482)


#Login_frame gui
IDlabel = Label(Login_frame, text="ID : ")
IDlabel.grid(row=0,column=0)

ID = Entry(Login_frame, width = 50)
ID.grid(row = 0, column = 1)

IDlabel = Label(Login_frame, text="Password : ")
IDlabel.grid(row=1,column=0)

PASS = Entry(Login_frame, width = 50)
PASS.grid(row = 1, column = 1)

Combobox_AG = ttk.Combobox(Login_frame, width = 20, values = ('고객','관리자'),state='readonly')
Combobox_AG.set("고객? 관리자?")
Combobox_AG.grid(row=2, column = 1,sticky = 'w')

def Login() :
  if Combobox_AG.get() == '고객? 관리자?' :
    messagebox.showinfo("선택","고객과 관리자중 선택하세요 ")
    return
  elif Combobox_AG.get() == '고객' :
    if ID.get() == 'man' and PASS.get() == 'man':
      O_idlabel = Label(order_frame, text="ID : ")
      O_idlabel.grid(row=0,column=0, sticky = 'nw')
      Guest_frame.grid()
    else :
      messagebox.showinfo("실패","아이디와 비밀번호를 확인하세요")
      return
  elif Combobox_AG.get() == '관리자' :
    if ID.get() == 'admin' and PASS.get() == 'admin':
      Admin_frame.grid()
      A_Start_stream()
    else :
      messagebox.showinfo("실패","아이디와 비밀번호를 확인하세요")
      return 
  
btn = Button(Login_frame, text="Login",command=Login)
btn.grid(row=2,column=1, sticky = 'e')

Login_frame.place(x=0, y=0)


#Guest_frame

first_img = ImageTk.PhotoImage(file = "first.png")
img_label = Label(Guest_frame, image = first_img)
img_label.place(x = 0 , y= 0)

def G_update_img():
  img_label.configure(image = videoframe)
  img_label.after(1,G_update_img)
def G_Check_ok() :
  G_update_img()
  G_update_img()
#btn = Button(Guest_frame, text="Check_signal",command=G_Check_ok)
#btn.place(x=700, y= 400)

#order_frame
order_frame = Frame(Guest_frame,width = 258, height = 482 )
O_orlabel = Label(order_frame, text="주문:  ")
O_orlabel.grid(row=1,column=0, sticky = 'nw')
O_Combobox = ttk.Combobox(order_frame, width = 20, values = ('짜장면','짬뽕','탕수육'),state='readonly')
O_Combobox.grid(row = 1, column = 1,sticky = 'nw')
O_orinfolabel = Label(order_frame, text = '내 주문정보')
O_orinfolabel.grid(row=4,column = 0,stick = 'w')

ID2 = Entry(order_frame, width = 10)
ID2.grid(row = 0, column = 1,sticky = 'nw')

def makeplace() :
  trash = []
  for i in range(20) :
    trash.append(Label(order_frame, text = '　'))
    trash[i].grid(row = 6+i, column = 0)
    
btn = Button(Guest_frame, text="Check_signal",command=G_Check_ok)
btn.place(x=700, y= 400)

makeplace()
infotext = []
camplace = 0
select_label = Label(order_frame, text= 'your selectinfo:' )
caminfolabel = Label(order_frame)
state_label = Label(order_frame)
givemecam = Button(order_frame, text='캠 줘')#,command = give_mecam)

def please_cam(count) :
  firebase0 = firebase.FirebaseApplication("https://foodfood-8393d.firebaseio.com/")
  select_label.place(x = 0, y= camplace)
  caminfolabel.configure(text= infotext[count])
  caminfolabel.place(x = 0, y= camplace+25)
  if firebase0.get('order/order%d' %count ,'cam') == None:
    state_label.configure(text = "조리대기중")
    state_label.place(x=150,y= camplace+50)
    givemecam.place(x=200 , y = 1000000)
  else :
    state_label.configure(text = "조리중")
    state_label.place(x=150,y= camplace+50)
    givemecam.place(x=200 , y = camplace + 50)
  
  
  
def makeinfo() :
  global infotext
  global camplace
  firebase0 = firebase.FirebaseApplication("https://foodfood-8393d.firebaseio.com/")
  count = 0
  O_orderlabel = []
  info_com = []
  ID1 = ID2.get()
  select_label.place(x = 0, y= 100000)
  caminfolabel.place(x = 0, y= 100000)
  givemecam.place(x=0 , y = 100000)
  state_label.place(x=0,y= 100000)

  
  for i in range(5) :
    if firebase0.get('order/order%d' %i ,'id') == ID1 :
      text1 = 'id:' + firebase0.get('order/order%d'%i ,'id') + ' '
      text1 += 'food:'+firebase0.get('order/order%d'%i ,'food')
      text1 += '(time:'+firebase0.get('order/order%d'%i ,'time')+')'
      infotext.append(text1)
      info_com.append(partial(please_cam,count))
      O_orderlabel.append(Button(order_frame, text=text1,command = info_com[count]))
      O_orderlabel[count].place(x = 0, y= 115+(count*25))
      camplace = 160+(count*25)
      count+= 1

checkO_btn = Button(order_frame, text="내 주문 확인",command=makeinfo)
checkO_btn.grid(row=3,column=0, sticky = 'Nw')    
  
def O_order():
  now1 = time.localtime()
  now2 = str(now1.tm_hour) + ":" + str(now1.tm_min) +':'+ str(now1.tm_sec)
  ID1 = ID2.get()
  food1 = O_Combobox.get()
  firebase1 = firebase.FirebaseApplication("https://foodfood-8393d.firebaseio.com/")
  for i in range(10000) :
    if firebase1.get('order/order%d' %i ,'id') == None :
      firebase1.put('order/order%d' %i ,'id',ID1)
      firebase1.put('order/order%d' %i ,'food',food1)
      firebase1.put('order/order%d' %i ,'time',now2)
      firebase1.put('order/order%d' %i ,'state',0)
      firebase1.put('order/order%d' %i ,'cam',0)
      break

  
O_btn = Button(order_frame, text="주문하기",command=O_order)
O_btn.grid(row=2,column=1, sticky = 'NE')


order_frame.place(x=642,y=0)
#Admin_frame
img_label_A = Label(Admin_frame)
img_label_A.place(x=0,y=0)

def A_update_img():
  img_label_A.configure(image = videoframe)
  img_label_A.after(1,A_update_img)

def A_Start_stream() :
  A_update_img()
  A_update_img()
 

#make_stream_frame
def make_img():
  global videoframe
  s_video = cv2.VideoCapture('http://192.168.0.76:8090/?action=stream')
  ret, img = s_video.read()
  if ret == False :
    return 0
  else :
    videoframe = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)))
    
  timer = threading.Timer(0.01,make_img)
  timer.start()
make_img()


root.mainloop()

      

  

