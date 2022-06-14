import time
from tkinter import *
import tkinter.messagebox
from random import sample
from collections import Counter
from PIL import Image, ImageTk

root = Tk()

root.title("Генератор судоку")
root["bg"] = "white"
root.geometry("1000x700")
root.resizable(width=False, height=False)

# открывает изображение
image = ImageTk.PhotoImage(Image.open('sydoku.png'))

# функция, которая создаёт основное меню
def menu() -> None:

    # создание основного меню

    # создаёт frame для основного меню
    frame = Frame(root, bg="white", width=1000, height=700)
    frame.pack()

    # функция, которая уничтожает главное окно и создаёт окно с правилами игры
    def how_play() -> None:
        frame.destroy()
        rules()

    # функция, которая уничтожает главное окно и создаёт окно с полем судоку
    def play() -> None:
        frame.destroy()
        game()

    # создаёт кнопки, картинку и надпись
    Label(frame, bg="white", fg="black", text="Генератор Судоку", font=("Arial", 25)).place(relheight=0.1, relwidth=0.3,
                                                                                            rely=0.05, relx=0.35)

    canvas = Canvas(frame, width=400, height=400)
    canvas.create_image(2, 2, anchor=NW, image=image)
    canvas.place(rely=0.18, relx=0.3)

    btn_play = Button(frame, text="Начать играть", bg="grey", fg="black", bd=0, font=("Arial", 20), command=play)
    btn_play.place(relwidth=0.3333, relheight=0.1, relx=0.111111, rely=0.8)

    btn_rules = Button(frame, text="Правила игры", bg="grey", fg="black", bd=0, font=("Arial", 20), command=how_play)
    btn_rules.place(relwidth=0.3333, relheight=0.1, relx=0.5555, rely=0.8)


# создаёт окно с правилами игры
def rules() -> None:

    #создание окна с правилами

    # создаёт frame для окна с правилами
    frame = Frame(root, bg="white", width=1000, height=700)
    frame.pack()

    # функция, которая удаляет окно с правилами и создаёт окно с самой игрой
    def back() -> None:
        frame.destroy()
        menu()

    # создаёт текст с правилом и кнопку "назад"
    rule = Text(frame, bg="white", bd=0, wrap=WORD, font=("Arial", 20))
    rule.insert(END,
                r"Игровое поле представляет собой квадрат размером 9x9, разделённый на меньшие квадраты стороной в 3 клетки. Таким образом, всё игровое поле состоит из 81 клетки. В них уже в начале игры стоят некоторые числа (от 1 до 9), называемые подсказками. От игрока требуется заполнить свободные клетки цифрами от 1 до 9 так, чтобы в каждой строке, в каждом столбце и в каждом малом квадрате 3x3 каждая цифра встречалась бы только один раз.")
    rule["state"] = "disable"
    rule.place(relwidth=0.8, relheight=0.6, rely=0.1, relx=0.1)

    btn_back = Button(frame, text="Назад", bg="grey", fg="black", bd=0, font=("Arial", 20), command=back)
    btn_back.place(relwidth=0.3333, relheight=0.1, relx=0.3333, rely=0.8)


# функция создаёт окно с игрой
def game() -> None:

    # запуск окна с игрой

    # сохраняет время начала игры
    start_time = time.time()

    # создаёт canvas для этого окна
    canvas = Canvas(root, bg="white", bd=0)
    canvas.place(relheight=1, relwidth=1)

    # создаёт заполненное судоку
    base = 3
    side = 9

    def pattern(r: int, c: int) -> int:
        return (base * (r % base) + r // base + c) % side

    def shuffle(s: range) -> list:
        return sample(s, len(s))

    rBase = range(base)
    rows = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase)]
    cols = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase)]
    nums = shuffle(range(1, base * base + 1))
    board = [[nums[pattern(r, c)] for c in cols] for r in rows]

    # удаляет некокорые значения из судоку
    squares = side * side
    empties = squares * 3 // 4
    for p in sample(range(squares), empties):
        board[p // side][p % side] = 0

    # функция, которая проверяет правильность заполнения поля
    def check() -> None:
        # сохраняет то, что ввёл пользователь
        rez = {i: globals()[f"entry{i}"].get() for i in range(81)}

        # сортирует значение по строкам
        stroka = [{j + i * 9: rez[j + i * 9] for j in range(9)} for i in range(9)]
        # сортирует значение по столбикам
        stolb = [{j * 9 + i: stroka[j][j * 9 + i] for j in range(9)} for i in range(9)]
        # сортирует значение по квадратам
        kwad = []
        for q in range(0, 7, 3):
            for w in range(0, 7, 3):
                spis = {}
                for i in range(3):
                    for j in range(3):
                        spis[(i + q) * 9 + j + w] = stroka[i + q][(i + q) * 9 + j + w]
                kwad.append(spis)

        # проверяет строку и делает поле с цифрами белыми или красными
        rezstroka = True
        for i in stroka:
            vstroka = [v1 for k1, v1 in i.items()]
            c = Counter(vstroka)
            for k2, v2 in c.items():
                if v2 > 1 and k2 != "":
                    for k3, v3 in i.items():
                        if v3 == k2:
                            globals()[f"entry{k3}"].configure({"background": "red"})
                    rezstroka = False
                elif k2 == "":
                    for k3, v3 in i.items():
                        if v3 == k2:
                            globals()[f"entry{k3}"].configure({"background": "yellow"})
                    rezstroka = False
                elif v2 == 1:
                    for k3, v3 in i.items():
                        if v3 == k2:
                            globals()[f"entry{k3}"].configure({"background": "white"})

        # проверяет столбики и делает квадраты с неправильными числами красными
        rezstolb = True
        for i in stolb:
            vstolb = [v1 for k1, v1 in i.items()]
            c = Counter(vstolb)
            for k2, v2 in c.items():
                if v2 > 1 and k2 != "":
                    for k3, v3 in i.items():
                        if v3 == k2:
                            globals()[f"entry{k3}"].configure({"background": "red"})
                    rezstolb = False

        # проверяет квадраты и делает с неправильными числами красными
        rezkwad = True
        for i in kwad:
            vkwad = [v1 for k1, v1 in i.items()]
            c = Counter(vkwad)
            for k2, v2 in c.items():
                if v2 > 1:
                    for k3, v3 in i.items():
                        if v3 == k2 and k2 != "":
                            globals()[f"entry{k3}"].configure({"background": "red"})
                    rezkwad = False

        # если всё заполнено правильно, то показывает сообщение об этом, уничтожает это окно и создаёт меню
        if rezstroka and rezstolb and rezkwad:
            nonlocal canvas

            tkinter.messagebox.showinfo(title="Уровень пройден!",
                                        message=f"Поздравляю! Вы прошли судоку за {now_minutes} минут и {now_second} секунд!")

            canvas.destroy()
            menu()

    # функция уничтожает окно и создаёт меню
    def exit() -> None:
        nonlocal canvas

        canvas.destroy()
        menu()

    # функция, которая всё время обновляет значения времени
    def update_time() -> None:
        nonlocal lbl_time, canvas
        global now_minutes, now_second

        now_time = int(time.time() - start_time)
        now_minutes = now_time // 60
        now_second = now_time % 60

        if len(str(now_minutes)) <= 1: now_minutes = "0" + str(now_minutes)
        if len(str(now_second)) <= 1: now_second = "0" + str(now_second)

        lbl_time.configure(text=f"Прошло {now_minutes} : {now_second}")

        canvas.after(1000, update_time)

    # функция, которая очищает поле
    def clear() -> None:
        for i in range(81):
            exec(f"entry{i}.configure(background='white')\nentry{i}.delete(0, END)")

    # функция, которая проверяет, что ввели
    num = "1 2 3 4 5 6 7 8 9".split()
    def validate(new_value: str, old_value: str, action: str, widget: str) -> None:
        color = globals()[widget].cget("background")
        if  color == "red" or color=="yellow":
            globals()[widget].configure(background="white")

        return new_value == "" or new_value in num and len(old_value) < 1 or action == "0"

    # создаёт надпись и кнопки
    lbl_time = Label(canvas, bg="white", fg="black", bd=0, font=("Arial", 20))
    lbl_time.place(relwidth=0.25, relheight=0.1, relx=0.7125, rely=0.1)

    btn_restart = Button(canvas, text="Начать сначала", bg="grey", fg="black", bd=0, font=("Arial", 20),
                         command=clear)
    btn_restart.place(relwidth=0.25, relheight=0.1, relx=0.7125, rely=0.3)

    btn_exit = Button(canvas, text="Выйти", bg="grey", fg="black", bd=0, font=("Arial", 20), command=exit)
    btn_exit.place(relwidth=0.25, relheight=0.1, relx=0.7125, rely=0.5)

    btn_check = Button(canvas, text="Завершить", bg="grey", fg="black", bd=0, font=("Arial", 20), command=check)
    btn_check.place(relwidth=0.25, relheight=0.1, relx=0.7125, rely=0.7)

    # вызывает функцию, которая обновляет время
    update_time()

    # создаёт поле судоку
    y_entry = 25
    x_entry = 25
    number = 0
    for line in board:
        for i in line:
            exec(
                f"global entry{number}\nentry{number} = Entry(canvas, validate='key', validatecommand=(root.register(validate), '%S', '%s', '%d', 'entry{number}'), bg='white', fg='black', justify=CENTER, font=('Arial', 20), relief=FLAT)\nentry{number}.place(width=70, height=70, x=x_entry, y=y_entry)")
            if i != 0:
                exec(f"entry{number}.insert(END, {i})")
                exec(f"entry{number}['state'] = 'disable'")

            x_entry += 72
            number += 1
        x_entry = 25
        y_entry += 72

    # рисует линии по y между клетками поля
    x_line = 25
    for i in range(1, 9):
        if i % 3 == 0:
            canvas.create_line(x_line + 71, 25, x_line + 71, 672, width=2)
        else:
            canvas.create_line(x_line + 71, 25, x_line + 71, 672, width=1)
        x_line += 72

    # рисует линии по x между клетками поля
    y_line = 25
    for i in range(1, 9):
        if i % 3 == 0:
            canvas.create_line(25, y_line + 71, 672, y_line + 71, width=2)
        else:
            canvas.create_line(25, y_line + 71, 672, y_line + 71, width=1)
        y_line += 72

#запускает код
if __name__ == "__main__":
    menu()
    root.mainloop()