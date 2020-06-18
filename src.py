import lexical_analyzer
import opz
import translator
from tkinter import *
from tkinter import filedialog
import os

# Лексический анализатор
analyzer_one = lexical_analyzer.Lexical()
reversed_polish_one = opz.OPZ()
main_text = []

# Отслеживает положение кнопки по lexical analyzer
button_index = 0

# Положение кнопки между классами
button_big = 0


def main():

    # Запуск анализатора
    def come_on():
        result_l['text'] = 'Lexical text'
        global button_index
        button_index = 0
        global button_big
        button_big = 0
        global analyzer_one
        global reversed_polish_one
        analyzer_one.clear()
        reversed_polish_one.clear()
        messenger.config(state=NORMAL)
        messenger.delete(1.0, END)
        messenger.insert(END, "Welcome! Translator ver. 1.0\n")
        messenger.config(state=DISABLED)
        text = program_text_box.get(1.0, END)
        text_list = []
        i = 0
        sub_text = ''
        while i < len(text):
            if text[i] != '\n':
                sub_text += text[i]
            else:
                text_list.append(sub_text)
                sub_text = ''
            i += 1
        i = 0
        ex = False
        column = 0
        while i < len(text_list) and not ex:
            ex, column = analyzer_one.analyzer(text_list[i])
            i += 1
        text_list = []
        for i in analyzer_one.main_text:
            for j in i:
                text_list.append(j)
        text_list = check_symbols(text_list)
        text_list = reversed_polish_one.returner_opz(text_list)
        global main_text
        translator_one = translator.Translator(text_list, analyzer_one)
        main_text = translator_one.translate()
        if ex:
            messenger.config(state=NORMAL)
            messenger.insert(END, "\nProcess finished with exit code 1\n\n")
            messenger.insert(END, "An exception has occurred in line {} column {}!\n".format(i, column))
            messenger.config(state=DISABLED)
        else:
            messenger.config(state=NORMAL)
            messenger.insert(END, "\nProcess finished with exit code 0\n\n")
            messenger.config(state=DISABLED)
        analyze_list = analyzer_one.main_text
        output_list(analyze_list)

    # Открыть файл
    def open_file():
        try:
            file_name = filedialog.askopenfilename(filetypes=[("TXT files", ".txt")])
            with open(file_name, "r") as file:
                text_list = file.readlines()
            program_text_box.delete(1.0, END)
            for i in range(len(text_list)):
                program_text_box.insert(END, text_list[i])
            program_l['text'] = file_name
        except OSError:
            messenger.config(state=NORMAL)
            messenger.insert(END, "Can't open a file!\n")
            messenger.config(state=DISABLED)

    # Сохранить в файл
    def save_file():
        try:
            dir_name = 'C:/Users/Angel/PycharmProjects/task_perl_to_assem/lexical_assets'
            os.mkdir(dir_name)
            global analyzer_one
            file_name = dir_name + '/lexical_text.txt'
            with open(file_name, "w") as file:
                text_list = analyzer_one.main_text
                for i in range(len(text_list)):
                    line = ' '.join(text_list[i])
                    line += '\n'
                    file.write(line)

            file_name = dir_name + '/identifier_table.txt'
            for i in range(3):
                if i == 0:
                    file_name = dir_name + '/identifier_table.txt'
                    text_list = analyzer_one.ident
                elif i == 1:
                    file_name = dir_name + '/numerical_table.txt'
                    text_list = analyzer_one.num
                elif i == 2:
                    file_name = dir_name + '/string_table.txt'
                    text_list = analyzer_one.con
                with open(file_name, "w") as file:
                    for in_dict in text_list:
                        file.write(text_list[in_dict] + ': ' + str(in_dict) + '\n')
            messenger.config(state=NORMAL)
            messenger.insert(END, "Your files was saved in task_perl_to_assem/lexical_assets directory\n")
            messenger.config(state=DISABLED)
        except OSError:
            messenger.config(state=NORMAL)
            messenger.insert(END, "Can't save a file!\n")
            messenger.config(state=DISABLED)

    # Кнопка прокрутки вперёд
    def forward():
        # if asdf:
            global button_index
            if button_index < 3:
                button_index += 1
            back_forward(button_index)

    # Кнопка прокрутки назад
    def back():
        # if combo_program.cget():
            global button_index
            if button_index > 0:
                button_index -= 1
            back_forward(button_index)

    # Выбор индекса кнопки
    def back_forward(i: int):
        global analyzer_one
        if i == 0:
            result_l['text'] = "Lexical text"
            # Текст лексем
            analyze_list = analyzer_one.main_text
            output_list(analyze_list)
        elif i == 1:
            result_l['text'] = "Identifier"
            # Идентификаторы
            analyze_list = analyzer_one.ident
            output_dict(analyze_list)
        elif i == 2:
            result_l['text'] = "Numerical constants"
            # Числовые константы
            analyze_list = analyzer_one.num
            output_dict(analyze_list)
        elif i == 3:
            result_l['text'] = "String constants"
            # Строковые константы
            analyze_list = analyzer_one.con
            output_dict(analyze_list)

    # Выводит текст лексем
    def output_list(analyze_list: list):
        lex_text_box.config(state=NORMAL)
        lex_text_box.delete(1.0, END)
        for i in range(len(analyze_list)):
            line = ' '.join(analyze_list[i])
            line += '\n'
            lex_text_box.insert(END, line)
        lex_text_box.config(state=DISABLED)

    # Выводит текст словарей
    def output_dict(analyze_list: dict):
        lex_text_box.config(state=NORMAL)
        lex_text_box.delete(1.0, END)
        for in_dict in analyze_list:
            lex_text_box.insert(END, analyze_list[in_dict] + ': ' + str(in_dict) + '\n')
        lex_text_box.config(state=DISABLED)

    # Кнопка прокрутки вперёд
    def forward_class():
        # if asdf:
        global button_big
        if button_big < 2:
            button_big += 1
        back_forward_class(button_big)

    # Кнопка прокрутки назад
    def back_class():
        # if combo_program.cget():
        global button_big
        if button_big > 0:
            button_big -= 1
        back_forward_class(button_big)

    # Выбор индекса кнопки
    def back_forward_class(i: int):
        global analyzer_one
        global reversed_polish_one
        global main_text
        if i == 0:
            result_l['text'] = "Lexical text"
            # Текст лексем
            analyze_list = analyzer_one.main_text
            output_list(analyze_list)
        elif i == 1:
            result_l['text'] = "OPZ"
            # опз
            reversed_list = reversed_polish_one.reversed_text
            lex_text_box.config(state=NORMAL)
            lex_text_box.delete(1.0, END)
            line = ' '.join(reversed_list)
            line += '\n'
            lex_text_box.insert(END, line)
            lex_text_box.config(state=DISABLED)
        elif i == 2:
            result_l['text'] = "Assembler"
            # Ассемблер
            lex_text_box.config(state=NORMAL)
            lex_text_box.delete(1.0, END)
            line = main_text
            for i in line:
                lex_text_box.insert(END, i + '\n')
            lex_text_box.config(state=DISABLED)

    def check_symbols(text_list: list):
        i = 0
        while i < len(text_list):
            if text_list[i] == 'p0' or text_list[i] == 'p2' or text_list[i] == 'r7' or text_list[i] == 'r8':
                del text_list[i]
            else:
                i += 1
        return text_list

    root = Tk()
    root.title("Translator")
    root.resizable(False, False)
    root.configure(background="#eee")

    # Кнопка запуска целиком
    button_all_program = Button(text="Запуск", width=7, height=1)
    button_all_program.config(command=come_on)
    button_all_program.place(x=1227, y=2)

    # Кнопки переключения между таблицами
    button_forward = Button(text=">", width=4, height=1, background="#aaa")
    button_forward.config(command=forward)
    button_forward.place(x=980, y=514)

    button_back = Button(text="<", width=4, height=1, background="#aaa")
    button_back.config(command=back)
    button_back.place(x=920, y=514)

    # Кнопки переключения между таблицами классов
    button_forward_class = Button(text=">", width=4, height=1, background="#aaa")
    button_forward_class.config(command=forward_class)
    button_forward_class.place(x=1180, y=514)

    button_back_class = Button(text="<", width=4, height=1, background="#aaa")
    button_back_class.config(command=back_class)
    button_back_class.place(x=1120, y=514)

    # Главное меню
    above_menu = Menu(root)
    root.config(menu=above_menu)

    # Меню в "Файл"
    file_menu = Menu(above_menu, tearoff=0)
    file_menu.add_command(label="Открыть", command=open_file)
    file_menu.add_command(label='Сохранить', command=save_file)
    file_menu.add_command(label='Выход')

    # Объединение меню
    above_menu.add_cascade(label='Файл', menu=file_menu)
    above_menu.add_command(label='Помощь')

    # Textbox входной программы
    program_text_box = Text(width=78, height=30, wrap=NONE, relief=SOLID)
    program_text_box.place(x=10, y=30)

    # Textbox входной программы
    lex_text_box = Text(width=78, height=30, wrap=WORD, relief=SOLID)
    lex_text_box.config(state=DISABLED)
    lex_text_box.place(x=658, y=30)

    # Messenger
    messenger = Text(width=159, height=9, fg="#002aff", relief=SOLID)
    messenger.pack(fill=BOTH)
    messenger.place(x=10, y=543)
    messenger.insert(END, "Welcome! Translator ver. 1.0\n")
    messenger.config(state=DISABLED)

    # Метки
    program_l = Label(text="Default program", height=1)
    program_l.config()
    program_l.place(x=10, y=7)

    result_l = Label(text="Result text", height=1)
    result_l.config()
    result_l.place(x=657, y=7)

    # Размер и положение окна
    window_height = 700
    window_width = 1300

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x_cord = int((screen_width / 2) - (window_width / 2))
    y_cord = int((screen_height / 2) - (window_height / 2))

    root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cord, y_cord - 50))

    root.mainloop()


if __name__ == '__main__':
    main()
