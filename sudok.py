from tkinter import *
from random import sample
from PIL import Image, ImageTk

root = Tk()

root.title("Генератор судоку")
root["bg"] = "white"
root.geometry("1000x700")
root.resizable(width=False, height=False)

# открываем изображение
image = ImageTk.PhotoImage(Image.open('sydoku.png'))

# функция создаёт основное меню
def menu() -> None:

    # frame для основного меню
    frame = Frame(root, bg="white", width=1000, height=700)
    frame.pack()

    #  уничтожает меню и создаёт окно с правилами игры
    def how_play() -> None:
        frame.destroy()
        rules()

    # уничтожает меню и создаёт поле судоку
    def play() -> None:
        frame.destroy()
        choose_difficulty()

    # кнопки, картинка и надпись
    Label(frame, bg="white", fg="black", text="Генератор Судоку", font=("Arial", 25)).place(relheight=0.1, relwidth=0.4,
                                                                                            rely=0.05, relx=0.3)

    canvas = Canvas(frame, width=400, height=400)
    canvas.create_image(2, 2, anchor=NW, image=image)
    canvas.place(rely=0.18, relx=0.3)

    btn_play = Button(frame, text="Сгенерировать поле", bg="grey", fg="black", bd=0, font=("Arial", 20), command=play)
    btn_play.place(relwidth=0.3333, relheight=0.1, relx=0.111111, rely=0.8)

    btn_rules = Button(frame, text="Правила игры", bg="grey", fg="black", bd=0, font=("Arial", 20), command=how_play)
    btn_rules.place(relwidth=0.3333, relheight=0.1, relx=0.5555, rely=0.8)


# окно с правилами
def rules() -> None:

    # frame для окна с правилами
    frame = Frame(root, bg="white", width=1000, height=700)
    frame.pack()

    # удаляет окно с правилами и и выходит в меню
    def back() -> None:
        frame.destroy()
        menu()

    # текст с правилами и выход
    rule = Text(frame, bg="white", bd=0, wrap=WORD, font=("Arial", 20))
    rule.insert(END,
                r"Игровое поле представляет собой квадрат размером 9x9, разделённый на меньшие квадраты стороной в 3 клетки. Таким образом, всё игровое поле состоит из 81 клетки. В них уже в начале игры стоят некоторые числа (от 1 до 9), называемые подсказками. От игрока требуется заполнить свободные клетки цифрами от 1 до 9 так, чтобы в каждой строке, в каждом столбце и в каждом малом квадрате 3x3 каждая цифра встречалась бы только один раз.")
    rule["state"] = "disable"
    rule.place(relwidth=0.8, relheight=0.6, rely=0.1, relx=0.1)

    btn_back = Button(frame, text="Назад", bg="grey", fg="black", bd=0, font=("Arial", 20), command=back)
    btn_back.place(relwidth=0.3333, relheight=0.1, relx=0.3333, rely=0.8)

# окно с выбором сложности
def choose_difficulty() -> None:

    frame = Frame(root, bg="white", width=1000, height=700)
    frame.pack()

    # споле легкого уровня
    def lite():
        frame.destroy()
        game(6)

    # поле среднего уровня
    def medium():
        frame.destroy()
        game(5)

    # поле сложного уровня
    def hard():
        frame.destroy()
        game(4)

    # кнопки
    Label(frame, bg="white", bd=0, text="Выберете уровень сложности:", font=("Arial", 25)).place(relheight=0.11, relwidth=0.6,
                                                                                            rely=0.1, relx=0.25)
    Button(frame, bg="grey", text="Лёгкий", fg="black", font=("Arial", 20), bd=0, command=lite).place(relwidth=0.3333, relheight=0.1, relx=0.3333, rely=0.3)
    Button(frame, bg="grey", text="Средний", fg="black", font=("Arial", 20), bd=0, command=medium).place(relwidth=0.3333, relheight=0.1, relx=0.3333, rely=0.5)
    Button(frame, bg="grey", text="Сложный", fg="black", font=("Arial", 20), bd=0, command=hard).place(relwidth=0.3333, relheight=0.1, relx=0.3333, rely=0.7)

# окно поля
def game(difficulty) -> None:

    # создаём canvas для этого окна
    canvas = Canvas(root, bg="white", bd=0)
    canvas.place(relheight=1, relwidth=1)

    field = Canvas(canvas, bg='white', bd=0)
    field.place(relheight=1, width=626+72, x=0, y=0)

    # создает судоку
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

    # создает ответы
    global all_board
    all_board = []
    for x in board:
        all_board.extend(x if isinstance(x, list) else [x])

    # убирает лишние значения
    squares = side * side
    empties = squares * 3 // difficulty
    a = sample(range(squares), empties)
    for p in a:
        board[p // side][p % side] = 0

    def check() -> None:

        # сортировка по строкам
        stroka = [{j + i * 9: rez[j + i * 9] for j in range(9)} for i in range(9)]
        # сортировка по столбикам
        stolb = [{j * 9 + i: stroka[j][j * 9 + i] for j in range(9)} for i in range(9)]
        # сортировка по квадратам
        kwad = []
        for q in range(0, 7, 3):
            for w in range(0, 7, 3):
                spis = {}
                for i in range(3):
                    for j in range(3):
                        spis[(i + q) * 9 + j + w] = stroka[i + q][(i + q) * 9 + j + w]
                kwad.append(spis)


    # функция ответов
    def answer():
        for i in range(81):
            exec(f'v{i}.set(all_board[i])')
            exec(f'root.after_idle(lambda: entry{i}.config(validate="key"))')

    def validate() -> bool:
        return False

    def exit() -> None:
        nonlocal canvas

        canvas.destroy()
        menu()

    # кнопки
    btn_answer = Button(canvas, text="Ответы", bg="grey", fg="black", bd=0, font=("Arial", 20), command=answer)
    btn_answer.place(relwidth=0.25, relheight=0.1, relx=0.7125, rely=0.2666666666666667)

    btn_exit = Button(canvas, text="Выйти", bg="grey", fg="black", bd=0, font=("Arial", 20), command=exit)
    btn_exit.place(relwidth=0.25, relheight=0.1, relx=0.7125, rely=0.6333333333333334)

    # поле судоку
    y_entry = 25
    x_entry = 25
    number = 0
    for line in board:
        for i in line:
            exec(f'global v{number}\nv{number} = StringVar()')
            if i != 0:
                exec(f'v{number}.set(i)')
            exec(
                f"global entry{number}\nentry{number} = Entry(field, validate='key', validatecommand=(root.register(validate),), textvariable=v{number}, bg='white', fg='black', justify=CENTER, font=('Arial', 20), relief=FLAT)\nentry{number}.place(width=70, height=70, x=x_entry, y=y_entry)")
            if i != 0:
                exec(f"entry{number}['state'] = 'disable'")

            x_entry += 72
            number += 1
        x_entry = 25
        y_entry += 72

    # линии по y между клетками поля
    x_line = 25
    for i in range(1, 9):
        if i % 3 == 0:
            field.create_line(x_line + 71, 25, x_line + 71, 672, width=2)
        else:
            field.create_line(x_line + 71, 25, x_line + 71, 672, width=1)
        x_line += 72

    # линии по x между клетками поля
    y_line = 25
    for i in range(1, 9):
        if i % 3 == 0:
            field.create_line(25, y_line + 71, 672, y_line + 71, width=2)
        else:
            field.create_line(25, y_line + 71, 672, y_line + 71, width=1)
        y_line += 72

if __name__ == "__main__":
    menu()
    root.mainloop()