import copy,os,time,datetime,copy,readchar,threading,queue,datetime
from random import randrange

block_1=[["H","H"],
         ["H","H"]]

block_2=[[" "," "," "," "],
         ["H","H","H","H"],
         [" "," "," "," "],
         [" "," "," "," "]]

block_3=[["H","H","H"],
         ["H"," "," "],
         [" "," "," "]]

block_4=[["H","H","H"],
         [" "," ","H"],
         [" "," "," "]]

block_5=[[" ","H"," "],
         ["H","H","H"],
         [" "," "," "]]

block_6=[["H","H"," "],
         [" ","H","H"],
         [" "," "," "]]

block_7=[[" ","H","H"],
         ["H","H"," "],
         [" "," "," "]]

list_block=[block_1,block_2,block_3,block_4,block_5,block_6,block_7]

color = [
    "\033[0;31;41m $\033[0m",    #Text: Red, Background: Red
    "\033[0;32;42m $\033[0m",    #Text: Green, Background: Green
    "\033[0;33;43m $\033[0m",    #Text: Yellow, Background: Yellow
    "\033[0;34;44m $\033[0m",    #Text: Blue, Background: Blue
    "\033[0;35;45m $\033[0m",    #Text: Purple, Background: Purple
    "\033[0;36;46m $\033[0m",    #Text: Cyan, Background: Cyan
    "\033[0;37;47m $\033[0m"    #Text: White, Background: White
]

def init_screen(row,colum):
  row_scr=[]
  for row_s in range(colum):
    row_scr.append(" ")
  screen=[]
  for colum_s in range(row):
    row_screen=copy.deepcopy(row_scr)
    screen.append(row_screen)
  return screen
#chon ngau nhien 1 khoi de hien thi
#in:danh_sach_cac_block[]
#out:block[][]string
def random_block(list_block):
  new_block=list_block[randrange(0,len(list_block))]
  number=randrange(0,7)
  for row in range(len(new_block)):
    for colum in range(len(new_block[row])):
      if new_block[row][colum]!=" ":
        new_block[row][colum]=number
  return new_block

#hien thi ra man hinh laptop
#in:screen [][]string 
#out: ".........."
def display_screen(screen,color,score):
  os.system("clear") 
  thread_println("YOUR SCORE:"+str(score[0]))
  frame=""
  for colum in range(len(screen)+2):
    frame=frame+"_"
  thread_println(frame)    
  for row in range(len(screen)):
    print("\r|",end = "")
    for colum in range(len(screen[row])):
      if screen[row][colum]!=" ":
        num=screen[row][colum]
        print(color[num],end = "")
      else:
        print(" ",end = " ")
    print("|")   
  thread_println(frame)      
  thread_println("Ps: w: rotate, a: move left, s: down faster d: move right")
  thread_println("Ps: x and Ctrl + z to exit the program")
  # time.sleep(0.001)


#dat_block_vao_screen
#in:screen=[][]string & block=[][]string & coordinate=[0,3]
#out:screen_contain_block=[][]string
#test ok,but con van de ra ngoai pham vi 2 bien
def place_block_in_screen(screen,block,coordinate):
  screen_contain_block=copy.deepcopy(screen)
  for row in range(len(block)):
    block_row=block[row]
    for colum in range(len(block_row)):
      if block_row[colum]!=" ":
          if (row+coordinate[0])<20:
            # print(block_row[colum])/
            screen_contain_block[row+coordinate[0]][colum+coordinate[1]]=block_row[colum]
  return screen_contain_block

#kiem tra co trung voi khoi xuat hien continue hay khong?
#in:  2 screen_before[][]string 
#out: True or False
#test ok
def test_block_next(MainScreen,next_screen):
  linhcanh=0
  for i in range(len(MainScreen)):
    for j in range(len(MainScreen[i])):
      if next_screen[i][j]!=" ":
        if MainScreen[i][j]!=" ":
          linhcanh=1
  if linhcanh==0:
    return False
  else:
    return True
#dich chuyen toa do xuong 1 dong
#in: screen=[][]string & block=[][]string & toa_do
#out: toa_do
def down_1_row_by_toa_do(EmptyScreen,block,toa_do):
  range_new=copy.deepcopy(toa_do)
  block_new=copy.deepcopy(block)
  last_row=0
  for row in range(len(block_new)):
    # print(block_new)
    for colum in range(len(block_new[row])):
      if block_new[row][colum]!=" ":
        last_row=row
  if range_new[0]<len(EmptyScreen)-last_row-1:
    range_new[0]+=1
    return range_new
  else:
    return range_new

#xoa hang day va dich nhung hang chua day o phia tren hang day xuong vi tri da bi xoa
#in: screen_kt=[][]string & row_i
#out: screen_after_clear=[][]string
def clear_row_full(screen_main,row_i):
  for colum in range(len(screen_main[row_i])):
    screen_main[row_i][colum]=" "
  for row in range(row_i,0,-1):
    for colum in range(len(screen_main[row])):
      screen_main[row][colum]=screen_main[row-1][colum]
  return screen_main


#kiem tra hang day va xoa cac hang day di 
#in:screen=[][]string & block=[][]string & toa_do=[0,3]
#out:screen_main
def kiem_tra_hang_day(MainScreen,score):
  for row in range(len(MainScreen)):
      linh_canh=1
      for colum in range(len(MainScreen[row])):
          if MainScreen[row][colum]==" ":
              linh_canh=0
      if linh_canh==1:
        score[0]+=1
        MainScreen=clear_row_full(MainScreen,row)
  return MainScreen


#kiem tra dieu kien game_over
#in:screen_main=[][]string & block=[][]string
#out:True or False
#test ok
def test_game_over(screen_main,block):  
  for colum in range(3,3+len(block),1):
    if screen_main[0][colum]!=" ":
      return True
  return False


# vong lap so sanh de nhay xuoong 1 dong
#in: MainScreen[][]string & block[][]string & toa_do[x,y]
#out: toa_do[x',y'] & block[][]string
def compare_screen_jump_dow(MainScreen,block,toa_do,score):
  while True:
    toa_do_next=down_1_row_by_toa_do(EmptyScreen,block,toa_do)
    screen_empty_add_block=place_block_in_screen(EmptyScreen,block,toa_do_next)
    if toa_do==toa_do_next:
        break
    if test_block_next(MainScreen,screen_empty_add_block)==True:
        break
    toa_do=down_1_row_by_toa_do(EmptyScreen,block,toa_do)
    MainScreen=place_block_in_screen(MainScreen,block,toa_do)
    display_screen(MainScreen,color,score)
  return toa_do



def CompareToDropAllBock(MainScreen,block,coordinate,player,score):
  if player==" ":
    while True:
      NextCoordinate=down_1_row_by_toa_do(EmptyScreen,block,coordinate)
      if coordinate==NextCoordinate:
        break
      NextScreen=place_block_in_screen(EmptyScreen,block,NextCoordinate)
      if test_block_next(MainScreen,NextScreen)==True:
        break
      coordinate=NextCoordinate
    MainScreen=place_block_in_screen(MainScreen,block,coordinate)
    display_screen(MainScreen,color,score)
  return coordinate
def CompareToDropFaster(MainScreen,block,coordinate,player,score):
  if player=="s":
    # while True:
      NextCoordinate=down_1_row_by_toa_do(EmptyScreen,block,coordinate)
      if coordinate==NextCoordinate:
        return coordinate
      NextScreen=place_block_in_screen(EmptyScreen,block,NextCoordinate)
      if test_block_next(MainScreen,NextScreen)==True:
        return coordinate
      coordinate=NextCoordinate
      DisScreen=place_block_in_screen(MainScreen,block,coordinate)
      display_screen(DisScreen,color,score)
  return coordinate

#xoay cac block
#in:EmptyScreen[][]string &block[][]string &toa_do[x,y]
#out:block[][]string & toa_do[]
def RotateBlock90(EmptyScreen,Block,toa_do):
  Block1=copy.deepcopy(Block)
  Coordinate=copy.deepcopy(toa_do)
  if Coordinate[1]<0:
    Coordinate[1]=0
  if Coordinate[1]>len(EmptyScreen[0])-len(Block):
    Coordinate[1]=len(EmptyScreen[0])-len(Block)
  for row in range(len(Block1)):
    for colum in range(len(Block1[row])):
      Block1[colum][row]=Block[row][colum]
  Block2=copy.deepcopy(Block)
  for row in range(len(Block)):
    for colum in range(len(Block[row])):
      Block2[row][colum]=Block1[row][len(Block1[row])-1-colum]
  return Block2,Coordinate

#nhay sang trai 1 cot 
#in : emptyscreen[][]string & block[][]string &toa_do=[0,1]
#0ut: True or False
def jump_left(EmptyScreen,block,toa_do):
  toa_do_to_jump_left=copy.deepcopy(toa_do)
  screen_prepare_jump_left=place_block_in_screen(EmptyScreen,block,toa_do)
  for row in range(len(screen_prepare_jump_left)):
    if screen_prepare_jump_left[row][0]!=" ":
        return toa_do_to_jump_left
  toa_do_to_jump_left[1]-=1
  return toa_do_to_jump_left
  

def compare_screen_jump_left(MainScreen,block,toa_do,player,score):
  if player=="a":
    toa_do_to_jump_left=jump_left(EmptyScreen,block,toa_do)
    if toa_do!=toa_do_to_jump_left:
      screen_jump_left=place_block_in_screen(EmptyScreen,block,toa_do_to_jump_left)
      if test_block_next(MainScreen,screen_jump_left)==False:
        toa_do=toa_do_to_jump_left
        DisScreen=place_block_in_screen(MainScreen,block,toa_do)
        # time.sleep(0.001)
        display_screen(DisScreen,color,score)
  return toa_do 

#jump_right_1_colum
#in: EmptyScreen[][]string & block[][]string & toa_do[x,y]
#out: toa_do_right[x,y']
def jump_right(EmptyScreen,block,toa_do):
  toa_do_to_jump_right=copy.deepcopy(toa_do)
  screen_prepare_jump_right=place_block_in_screen(EmptyScreen,block,toa_do)
  for row in range(len(screen_prepare_jump_right)):
    if screen_prepare_jump_right[row][len(screen_prepare_jump_right[row])-1]!=" ":
      return toa_do_to_jump_right
  toa_do_to_jump_right[1]+=1
  return toa_do_to_jump_right


def compare_screen_jump_right(MainScreen,block,toa_do,player,score):
  if player=="d":
    toa_do_to_jump_right=jump_right(EmptyScreen,block,toa_do)
    if toa_do!=toa_do_to_jump_right:
      screen_jump_right=place_block_in_screen(EmptyScreen,block,toa_do_to_jump_right)
      if test_block_next(MainScreen,screen_jump_right)==False:
        toa_do=toa_do_to_jump_right
        DisScreen=place_block_in_screen(MainScreen,block,toa_do)
        # time.sleep(0.001)
        display_screen(DisScreen,color,score)
  return toa_do

#xoay block 90 ve ben phai
#in:
#out:
def rotate_block_90_right(EmptyScreen,block,toa_do):
  block_r=copy.deepcopy(block)
  toa_do_r=copy.deepcopy(toa_do)
  if toa_do_r[1]<0:
    toa_do_r[1]=0
  if toa_do_r[1]>len(EmptyScreen[0])-len(block):
    toa_do_r[1]=len(EmptyScreen[0])-len(block)
  for row in range(len(block)):
    for colum in range(len(block[row])):  
      block_r[colum][row]=block[row][colum]
  block_r_2=copy.deepcopy(block)
  for row in range(len(block)):
    for colum in range(len(block[row])):
      block_r_2[row][colum]=block_r[row][len(block[row])-1-colum]
  return block_r_2,toa_do_r


def rotate_down(MainScreen,EmptyScreen,block_r,toa_do_r):
  toa_do_r[0]=toa_do_r[0]-1
  screen_r=place_block_in_screen(EmptyScreen,block_r,toa_do_r)
  if test_block_next(MainScreen,screen_r)==True:
    toa_do_r[0]=toa_do_r[0]-1
  return block_r,toa_do_r


def rotate_left_right(MainScreen,EmptyScreen,block,toa_do,block_r,toa_do_r):
  if toa_do_r[1]<len(MainScreen[0])-len(block):
    toa_do_r[1]=toa_do_r[1]+1
  screen_r=place_block_in_screen(EmptyScreen,block_r,toa_do_r)
  if test_block_next(MainScreen,screen_r)==True:
    if toa_do_r[1]>1:
      toa_do_r[1]=toa_do_r[1]-2
  screen_r=place_block_in_screen(EmptyScreen,block_r,toa_do_r)
  if test_block_next(MainScreen,screen_r)==False:
    block=block_r
    toa_do=toa_do_r
  return block,toa_do

def compare_to_rotate(MainScreen,EmptyScreen,block,toa_do,player,down_flag,check_flag,score):
  if player=="w":
    block_r=copy.deepcopy(block)
    toa_do_r=copy.deepcopy(toa_do)
    block_r,toa_do_r=rotate_block_90_right(EmptyScreen,block,toa_do)
    last_row=0
    for row in range(len(block_r)):
      for colum in range(len(block_r[row])):
        if block_r[row][colum]!=" ":
          last_row=row
    if toa_do[0]<len(MainScreen)-last_row:
      screen_r=place_block_in_screen(EmptyScreen,block_r,toa_do_r)
      if test_block_next(MainScreen,screen_r)==False:
        block=block_r
        toa_do=toa_do_r
        dis_screen=place_block_in_screen(MainScreen,block,toa_do)
        # time.sleep(0.01)
        display_screen(dis_screen,color,score)
      else:
        block,toa_do=rotate_left_right(MainScreen,EmptyScreen,block,toa_do,block_r,toa_do_r)
        dis_screen=place_block_in_screen(MainScreen,block,toa_do)
        # time.sleep(0.01)
        display_screen(dis_screen,color,score)
    elif down_flag==1:
      block,toa_do=rotate_down(MainScreen,EmptyScreen,block_r,toa_do_r)
      dis_screen=place_block_in_screen(MainScreen,block,toa_do)
      # time.sleep(0.01)
      display_screen(dis_screen,color,score)
      check_flag=1
  return block,toa_do,check_flag  
def jump_next(MainScreen,block,toa_do,score):
  toa_do=down_1_row_by_toa_do(EmptyScreen,block,toa_do)
  DisScreen=place_block_in_screen(MainScreen,block,toa_do)
  display_screen(DisScreen,color,score)



# doc ki tu tu ban phim va nhac ki tu do vao ống hàng đợi (queue)
def read_character_from_keyborad():
  while True:
    key=readchar.readchar()
    input_queue.put(key)
    if key=="x":
      break


def thread_println(str):
  print('\r'+str)

def loop_down_1_line_and_get_input(MainScreen,block,toa_do,down_flag,score):
  level=0
  while True:
    time_count=0.0
    check_flag=0
    loop10=0
    while int(time_count+level)!=1:
      block,toa_do,check_flag=compare_character_input(MainScreen,block,toa_do,down_flag,check_flag)
      time_count+=0.001
      time.sleep(0.001)
    loop10+=1
    if loop10==10:
      slevel+=0.001
    if check_flag == 1:
      down_flag = 0

    toa_do_next=down_1_row_by_toa_do(EmptyScreen,block,toa_do)
    if toa_do==toa_do_next:
      break
    next_screen=place_block_in_screen(EmptyScreen,block,toa_do_next)
    if test_block_next(MainScreen,next_screen)==True:
      break
    toa_do=down_1_row_by_toa_do(MainScreen,block,toa_do)
    display_screen(place_block_in_screen(MainScreen,block,toa_do),color,score)
  return toa_do,block
def input_keyboard(MainScreen,block,toa_do,input_queue,score):
  while True:
    down_flag=1
    input_queue.queue.clear()
    toa_do=[0,3]
    block=random_block(list_block)
    DisScreen=place_block_in_screen(MainScreen,block,toa_do)
    display_screen(DisScreen,color,score)
    toa_do,block=loop_down_1_line_and_get_input(MainScreen,block,toa_do,down_flag,score)
    MainScreen=place_block_in_screen(MainScreen,block,toa_do)
    kiem_tra_hang_day(MainScreen,score)
  
    display_screen(MainScreen,color,score)
    if test_game_over(MainScreen,block)==True:
      break
  thread_println("game_over")

def compare_character_input(MainScreen,block,toa_do,down_flag,check_flag):
  if not input_queue.empty():
    player=input_queue.get()
    toa_do=compare_screen_jump_left(MainScreen,block,toa_do,player,score)
    toa_do=compare_screen_jump_right(MainScreen,block,toa_do,player,score)
    block,toa_do,check_flag=compare_to_rotate(MainScreen,EmptyScreen,block,toa_do,player,down_flag,check_flag,score)
    toa_do=CompareToDropAllBock(MainScreen,block,toa_do,player,score)
    toa_do=CompareToDropFaster(MainScreen,block,toa_do,player,score)
  return block,toa_do,check_flag
if __name__ == "__main__":
  toa_do=[0,3]
  screen=init_screen(20,10)
  score=[0]
  MainScreen=copy.deepcopy(screen)
  EmptyScreen=copy.deepcopy(screen)
  block=random_block(list_block)
  input_queue=queue.Queue()
  loop_input  =  threading.Thread(target = input_keyboard, args = (MainScreen,block,toa_do,input_queue,score))
  loop_read_character = threading.Thread(target = read_character_from_keyborad)
  loop_input.start()
  loop_read_character.start()
  