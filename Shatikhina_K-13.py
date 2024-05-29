import random
import time
import copy
from tkinter import PhotoImage, Tk, Canvas, NW, messagebox, mainloop

gl_window=Tk()#создаём окно
gl_window.title('Шашки')#заголовок окна
board=Canvas(gl_window, width=800,height=800,bg='#FFFFFF')
board.pack()

n2_list=()#конечный список ходов компьютера
ur=3#количество предсказываемых компьютером ходов
k_rez=0#!!!
o_rez=0
poz1_x=-1#клетка не задана
f_hi=True#определение хода игрока(да)

def pawn_images():#загружаем изображения пешек
    global pawns
    i1=PhotoImage(file="res\\1b.gif")
    i2=PhotoImage(file="res\\1bk.gif")
    i3=PhotoImage(file="res\\1h.gif")
    i4=PhotoImage(file="res\\1hk.gif")
    pawns=[0,i1,i2,i3,i4]

def new_game():#начинаем новую игру
    global field
    field=[[0,3,0,3,0,3,0,3],
          [3,0,3,0,3,0,3,0],
          [0,3,0,3,0,3,0,3],
          [0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0],
          [1,0,1,0,1,0,1,0],
          [0,1,0,1,0,1,0,1],
          [1,0,1,0,1,0,1,0]]

def conclusion(x_poz_1,y_poz_1,x_poz_2,y_poz_2):#рисуем игровое поле
    global pawns
    global field
    global kr_frame,zel_frame
    k=100
    x=0
    board.delete('all')
    kr_frame = board.create_rectangle(-5, -5, -5, -5,outline="red",width=5)
    zel_frame = board.create_rectangle(-5, -5, -5, -5,outline="green",width=5)

    while x<8*k:  #рисуем доску
        y=1*k
        while y<8*k:
            board.create_rectangle(x, y, x+k, y+k,fill="black")
            y+=2*k
        x+=2*k
    x=1*k
    while x<8*k:  #рисуем доску
        y=0
        while y<8*k:
            board.create_rectangle(x, y, x+k, y+k,fill="black")
            y+=2*k
        x+=2*k
    
    for y in range(8):  #рисуем стоячие пешки
        for x in range(8):
            z=field[y][x]
            if z:  
                if (x_poz_1,y_poz_1)!=(x,y):   #стоячие пешки
                    board.create_image(x*k,y*k, anchor=NW, image=pawns[z]) 
                    
    #рисуем активную пешку  
    
    z=field[y_poz_1][x_poz_1]
    if z:
        board.create_image(x_poz_1*k,y_poz_1*k, anchor=NW, image = pawns[z],tag='ani')
    #вычисление коэф. для анимации
    kx = 1 if x_poz_1<x_poz_2 else -1
    ky = 1 if y_poz_1<y_poz_2 else -1
    for i in range(abs(x_poz_1-x_poz_2)):   #анимация перемещения пешки
        for ii in range(33):
            board.move('ani',0.03*k*kx,0.03*k*ky)
            board.update()   #обновление
            time.sleep(0.01)

def soobseniemessage(s):
    global f_hi
    z='Игра завершена'
    if s==1:
        i=messagebox.askyesno(title=z, message='Вы победили!\nНажми "Да" что бы начать заново.',icon='info')
    if s==2:
        i=messagebox.askyesno(title=z, message='Вы проиграли!\nНажми "Да" что бы начать заново.',icon='info')
    if s==3:
        i=messagebox.askyesno(title=z, message='Ходов больше нет.\nНажми "Да" что бы начать заново.',icon='info')
    if i:
        new_game()
        conclusion(-1,-1,-1,-1)   #рисуем игровое поле
        f_hi=True   #ход игрока доступен

def position_1(event):    #выбор клетки для хода 1
    x,y=(event.x)//100,(event.y)//100    #вычисляем координаты клетки
    board.coords(zel_frame,x*100,y*100,x*100+100,y*100+100)    #рамка в выбранной клетке

def position_2(event):    #выбор клетки для хода 2
    global poz1_x, poz1_y, poz2_x, poz2_y
    global f_hi
    x,y=(event.x)//100,(event.y)//100    #вычисляем координаты клетки
    if field[y][x]==1 or field[y][x]==2:    #проверяем пешку игрока в выбранной клетке
        board.coords(kr_frame,x*100,y*100,x*100+100,y*100+100)    #рамка в выбранной клетке
        poz1_x, poz1_y=x,y
    else:
        if poz1_x!=-1:    #клетка выбрана
            poz2_x,poz2_y=x,y
            if f_hi:    #ход игрока
                move_player()
                if not(f_hi):
                    time.sleep(0.5)
                    move_comp()    #передаём ход компьютеру
                    #gl_okno.after(500, move_comp(0))    #передаём ход компьютеру
            poz1_x=-1    #клетка не выбрана
            board.coords(kr_frame,-5,-5,-5,-5)    #рамка вне поля              
     
def motion_comp():
    global f_hi
    global n2_list
    check_hk(1,(),[])
    if n2_list:    #проверяем наличие доступных ходов
        kh=len(n2_list)    #количество ходов
        th=random.randint(0,kh-1)    #случайный ход
        dh=len(n2_list[th])    #длина хода
        for h in n2_list:    #для отладки
            h=h    #для отладки
        for i in range(dh-1):
            #выполняем ход
            list = move(1,n2_list[th][i][0],n2_list[th][i][1],n2_list[th][1+i][0],n2_list[th][1+i][1])
        n2_list=[]    #очищаем список ходов
        f_hi=True    #ход игрока доступен

    #определяем победителя 
    s_k,s_i=skan()
    if not(s_i):
            message(2)
    elif not(s_k):
            message(1)
    elif f_hi and not(list_hi()):
            message(3)
    elif not(f_hi) and not(list_hk()):
            message(3)

def list_hk():    #составляем список ходов компьютера
    list = viewing_moves_k1([])    #здесь проверяем обязательные ходы
    if not(list):
        list = viewing_moves_k2([])    #здесь проверяем оставшиеся ходы
    return list

def check_hk(tur,n_list, list):#!!!
    global field
    global n2_list
    global l_rez,k_rez,o_rez
    if not(list):    #если список ходов пустой...
        list=list_hk()    #заполняем

    if list:
        k_field=copy.deepcopy(field)    #копируем поле
        for ((poz1_x,poz1_y),(poz2_x,poz2_y)) in list:    #проходим все ходы по списку
            t_list= move(0,poz1_x,poz1_y,poz2_x,poz2_y)
            if t_list:    #если существует ещё ход
                check_hk(tur,(n_list+((poz1_x,poz1_y),)),t_list)
            else:
                check_hi(tur,[])
                if tur==1:
                    t_rez=o_rez/k_rez
                    if not(n2_list):    #записыаем если пустой
                        n2_list=(n_list+((poz1_x,poz1_y),(poz2_x,poz2_y)),)
                        l_rez=t_rez    #сохряняем наилучший результат
                    else:
                        if t_rez==l_rez:
                            n2_list=n2_list+(n_list+((poz1_x,poz1_y),(poz2_x,poz2_y)),)
                        if t_rez>l_rez:
                            n2_list=()
                            n2_list=(n_list+((poz1_x,poz1_y),(poz2_x,poz2_y)),)
                            l_rez=t_rez    #сохряняем наилучший результат
                    o_rez=0
                    k_rez=0

            field=copy.deepcopy(k_field)    #возвращаем поле
    else:
        s_k,s_i=skan()    #подсчёт результата хода
        o_rez+=(s_k-s_i)
        k_rez+=1

def list_hi():    #составляем список ходов игрока
    list = viewing_moves_i1([])    #здесь проверяем обязательные ходы
    if not(list):
        list = viewing_moves_i2([])    #здесь проверяем оставшиеся ходы
    return list
    
def check_hi(tur,list):
    global field,k_rez,o_rez
    global ur
    if not(list):
        list = list_hi()

    if list:    #проверяем наличие доступных ходов
        k_field=copy.deepcopy(field)    #копируем поле
        for ((poz1_x,poz1_y),(poz2_x,poz2_y)) in list:                    
            t_list = move(0,poz1_x,poz1_y,poz2_x,poz2_y)
            if t_list:    #если существует ещё ход
                check_hi(tur,t_list)
            else:
                if tur<ur:
                    check_hk(tur+1,(),[])
                else:
                    s_k,s_i=skan()    #подсчёт результата хода
                    o_rez+=(s_k-s_i)
                    k_rez+=1

            field=copy.deepcopy(k_field)    #возвращаем поле
    else:    #доступных ходов нет
        s_k,s_i=skan()    #подсчёт результата хода
        o_rez+=(s_k-s_i)
        k_rez+=1

def skan():    #подсчёт пешек на поле
    global field
    s_i=0
    s_k=0
    for i in range(8):
        for ii in field[i]:
            if ii==1:s_i+=1
            if ii==2:s_i+=3
            if ii==3:s_k+=1
            if ii==4:s_k+=3
    return s_k,s_i

def player_move():
    global poz1_x,poz1_y,poz2_x,poz2_y
    global f_hi
    f_hi=False    #считаем ход игрока выполненным
    list = list_hi()
    if list:
        if ((poz1_x,poz1_y),(poz2_x,poz2_y)) in list:    #проверяем ход на соответствие правилам игры
            t_list = move(1,poz1_x,poz1_y,poz2_x,poz2_y)    #если всё хорошо, делаем ход            
            if t_list:    #если есть ещё ход той же пешкой
                f_hi=True    #считаем ход игрока невыполненным
        else:
            f_hi=True#считаем ход игрока невыполненным
    board.update()    #обновление

def move(f,poz1_x,poz1_y,poz2_x,poz2_y):
    global field
    if f:conclusion(poz1_x,poz1_y,poz2_x,poz2_y)    #рисуем игровое поле
    #превращение
    if poz2_y==0 and field[poz1_y][poz1_x]==1:
        field[poz1_y][poz1_x]=2
    #превращение
    if poz2_y==7 and field[poz1_y][poz1_x]==3:
        field[poz1_y][poz1_x]=4
    #делаем ход           
    field[poz2_y][poz2_x]=field[poz1_y][poz1_x]
    field[poz1_y][poz1_x]=0

    #рубим пешку игрока
    kx=ky=1
    if poz1_x<poz2_x:kx=-1
    if poz1_y<poz2_y:ky=-1
    x_poz,y_poz=poz2_x,poz2_y
    while (poz1_x!=x_poz) or (poz1_y!=y_poz):
        x_poz+=kx
        y_poz+=ky
        if field[y_poz][x_poz]!=0:
            field[y_poz][x_poz]=0
            if f:conclusion(-1,-1,-1,-1)    #рисуем игровое поле
            #проверяем ход той же пешкой...
            if field[poz2_y][poz2_x]==3 or field[poz2_y][poz2_x]==4:    #...компьютера
                return viewing_moves_k1p([],poz2_x,poz2_y)    #возвращаем список доступных ходов
            elif field[poz2_y][poz2_x]==1 or field[poz2_y][poz2_x]==2:    #...игрока
                return viewing_moves_i1p([],poz2_x,poz2_y)    #возвращаем список доступных ходов
    if f:conclusion(poz1_x,poz1_y,poz2_x,poz2_y)    #рисуем игровое поле

def viewing_moves_k1(list):    #проверка наличия обязательных ходов
    for y in range(8):         #сканируем всё поле
        for x in range(8):
            list = viewing_moves_k1p(list,x,y)
    return list

def viewing_moves_k1p(list,x,y):
    if field[y][x]==3:     #пешка
        for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
            if 0<=y+iy+iy<=7 and 0<=x+ix+ix<=7:
                if field[y+iy][x+ix]==1 or field[y+iy][x+ix]==2:
                    if field[y+iy+iy][x+ix+ix]==0:
                        list.append(((x,y),(x+ix+ix,y+iy+iy)))     #запись хода в конец списка
    if field[y][x]==4:     #дамка
        for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
            osh=0    #определение правильности хода
            for i in  range(1,8):
                if 0<=y+iy*i<=7 and 0<=x+ix*i<=7:
                    if osh==1:
                        list.append(((x,y),(x+ix*i,y+iy*i)))    #запись хода в конец списка
                    if field[y+iy*i][x+ix*i]==1 or field[y+iy*i][x+ix*i]==2:
                        osh+=1
                    if field[y+iy*i][x+ix*i]==3 or field[y+iy*i][x+ix*i]==4 or osh==2:
                        if osh>0:list.pop()    #удаление хода из списка
                        break
    return list

def viewing_moves_k2(list):    #проверка наличия остальных ходов
    for y in range(8):    #сканируем всё поле
        for x in range(8):
            if field[y][x]==3:    #пешка
                for ix,iy in (-1,1),(1,1):
                    if 0<=y+iy<=7 and 0<=x+ix<=7:
                        if field[y+iy][x+ix]==0:
                            list.append(((x,y),(x+ix,y+iy)))     #запись хода в конец списка
                        if field[y+iy][x+ix]==1 or field[y+iy][x+ix]==2:
                            if 0<=y+iy*2<=7 and 0<=x+ix*2<=7:
                                if field[y+iy*2][x+ix*2]==0:
                                    list.append(((x,y),(x+ix*2,y+iy*2)))     #запись хода в конец списка                  
            if field[y][x]==4:     #дамка
                for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
                    osh=0     #определение правильности хода
                    for i in range(1,8):
                        if 0<=y+iy*i<=7 and 0<=x+ix*i<=7:
                            if field[y+iy*i][x+ix*i]==0:
                                list.append(((x,y),(x+ix*i,y+iy*i)))     #запись хода в конец списка
                            if field[y+iy*i][x+ix*i]==1 or field[y+iy*i][x+ix*i]==2:
                                osh+=1
                            if field[y+iy*i][x+ix*i]==3 or field[y+iy*i][x+ix*i]==4 or osh==2:
                                break
    return list

def viewing_moves_i1(list):    #проверка наличия обязательных ходов
    list=[]    #список ходов
    for y in range(8):    #сканируем всё поле
        for x in range(8):
            list= viewing_moves_i1p(list,x,y)
    return list

def viewing_moves_i1p(list,x,y):
    if field[y][x]==1:     #пешка
        for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
            if 0<=y+iy+iy<=7 and 0<=x+ix+ix<=7:
                if field[y+iy][x+ix]==3 or field[y+iy][x+ix]==4:
                    if field[y+iy+iy][x+ix+ix]==0:
                        list.append(((x,y),(x+ix+ix,y+iy+iy))) #запись хода в конец списка
    if field[y][x]==2:     #дамка
        for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
            osh=0      #определение правильности хода
            for i in  range(1,8):
                if 0<=y+iy*i<=7 and 0<=x+ix*i<=7:
                    if osh==1:
                        list.append(((x,y),(x+ix*i,y+iy*i)))    #запись хода в конец списка
                    if field[y+iy*i][x+ix*i]==3 or field[y+iy*i][x+ix*i]==4:
                        osh+=1
                    if field[y+iy*i][x+ix*i]==1 or field[y+iy*i][x+ix*i]==2 or osh==2:
                        if osh>0:list.pop()    #удаление хода из списка
                        break
    return list

def viewing_moves_i2(list):    #проверка наличия остальных ходов
    for y in range(8):    #сканируем всё поле
        for x in range(8):
            if field[y][x]==1:     #пешка
                for ix,iy in (-1,-1),(1,-1):
                    if 0<=y+iy<=7 and 0<=x+ix<=7:
                        if field[y+iy][x+ix]==0:
                            list.append(((x,y),(x+ix,y+iy)))    #запись хода в конец списка
                        if field[y+iy][x+ix]==3 or field[y+iy][x+ix]==4:
                            if 0<=y+iy*2<=7 and 0<=x+ix*2<=7:
                                if field[y+iy*2][x+ix*2]==0:
                                    list.append(((x,y),(x+ix*2,y+iy*2)))    #запись хода в конец списка                  
            if field[y][x]==2:    #дамка
                for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
                    osh = 0     #определение правильности хода
                    for i in range(1,8):
                        if 0<=y+iy*i<=7 and 0<=x+ix*i<=7:
                            if field[y+iy*i][x+ix*i]==0:
                                list.append(((x,y),(x+ix*i,y+iy*i)))     #запись хода в конец списка
                            if field[y+iy*i][x+ix*i]==3 or field[y+iy*i][x+ix*i]==4:
                                osh+=1
                            if field[y+iy*i][x+ix*i]==1 or field[y+iy*i][x+ix*i]==2 or osh==2:
                                break
    return list

pawn_image()                            #здесь загружаем изображения пешек
new_game()                              #начинаем новую игру
conclusion(-1,-1,-1,-1)                 #рисуем игровое поле
board.bind("<Motion>", pozici_1)        #движение мышки по полю
board.bind("<Button-1>", pozici_2)      #нажатие левой кнопки

mainloop()
