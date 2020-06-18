class Lexical:
    # Служебные слова
    w = {
        'print': 'w0',
        'sub': 'w1',
        'return': 'w2',
        'if': 'w3',
        'else': 'w4',
        'goto': 'w5',
        'while': 'w6',
        'for': 'w7',
        'until': 'w8',
        'foreach': 'w9',
        'next': 'w10',
        'last ': 'w11',
        'redo': 'w12',
        'do': 'w13',
        'my': 'w14'
    }
    # Однолитерные операции
    o_one = {
        '+': 'o0',
        '-': 'o1',
        '*': 'o2',
        '/': 'o3',
        '<': 'o4',
        '>': 'o5',
        '=': 'o6',
        ':': 'o7',
        '!': 'o8'
    }
    # Двулитерные операции
    o_double = {
        '**': 'o9',
        '==': 'o10',
        '!=': 'o11',
        '<=': 'o12',
        '>=': 'o13',
        '||': 'o14',
        '&&': 'o15'
    }
    # Разделители
    r = {
        '{': 'r0',
        '}': 'r1',
        ';': 'r2',
        ',': 'r3',
        '(': 'r4',
        ')': 'r5',
        ' ': 'r6',
        '\n': 'r7',
        '\t': 'r8',
        '[': 'r9',
        ']': 'r10',
        '"': 'r11',
        "'": 'r12',
        '.': 'r13'
    }

    # Символы для переменных, массивов и функций
    p = {
        '$': 'p0',
        '@': 'p1',
        '&': 'p2'
    }
    # Буквы
    letters = ['_']
    # Цифры
    digits = []

    def __init__(self):
        # Идентификаторы
        self.__ident = {}
        # Числовые константы
        self.__num = {}
        # Символьные константы
        self.__con = {}
        # Выходной текст
        self.__main_text = []
        self.__functions = []

        Lexical.letters_and_digits(Lexical.letters, Lexical.digits)

    @staticmethod
    def letters_and_digits(letters, digits):
        for s in range(65, 91):
            letters.append(chr(s))
        for s in range(97, 123):
            letters.append(chr(s))
        for s in range(48, 58):
            digits.append(chr(s))

    def analyzer(self, text: str):
        self.__main_text.append([])
        i = 0
        text += '\n\n'
        ex = False
        while i < len(text) - 2 and not ex:
            j = i

            # переменные + идентификаторы
            if text[i] in Lexical.letters or text[i] in Lexical.p and not text[i] + text[i + 1] in Lexical.o_double:
                if text[i] in Lexical.p:
                    self.sem8_p(text[i])
                    i += 1
                    j = i
                    if text[i] == '&':
                        self.__functions.append(text[i + 1])
                while text[i] in Lexical.letters:
                    i += 1
                sub_text = text[j:i]
                if sub_text == '':
                    ex = True
                elif text[i] in Lexical.r or text[i] in Lexical.o_one or text[i] + text[i + 1] in Lexical.o_double:
                    self.sem2_find_w(sub_text)
                elif text[i] in Lexical.digits:
                    while text[i] in Lexical.digits or text[i] in Lexical.letters:
                        i += 1
                    sub_text = text[j:i]
                    if text[i] in Lexical.r or text[i] in Lexical.o_one or text[i] + text[i + 1] in Lexical.o_double:
                        self.sem1_find_id(sub_text)
                    else:
                        ex = True
                else:
                    ex = True

            # Все числа
            elif text[i] in Lexical.digits or text[i] == '.':
                done = False
                state = 0
                if state == 0:
                    if text[i] in Lexical.digits:
                        state = 1
                    elif text[i] == '.':
                        state = 7
                while not done and not ex:
                    if state == 1:
                        i += 1
                        while text[i] in Lexical.digits:
                            i += 1
                        if (text[i] in Lexical.r or text[i] in Lexical.o_one or text[i] + text[i + 1]
                                in Lexical.o_double) and text[i] != '.':
                            self.sem3_num(text[j:i])
                            done = True
                        elif text[i] == '.':
                            state = 2
                        elif text[i] == 'e' or text[i] == 'E':
                            state = 4
                        else:
                            ex = True
                    elif state == 2:
                        i += 1
                        if text[i] in Lexical.r or text[i] in Lexical.o_one or text[i] + text[i + 1] \
                                in Lexical.o_double:
                            self.sem3_num(text[j:i])
                            done = True
                        elif text[i] in Lexical.digits:
                            state = 3
                        else:
                            ex = True
                    elif state == 3:
                        i += 1
                        while text[i] in Lexical.digits:
                            i += 1
                        if text[i] == 'e' or text[i] == 'E':
                            state = 4
                        elif text[i] in Lexical.r or text[i] in Lexical.o_one or text[i] + text[i + 1] \
                                in Lexical.o_double:
                            self.sem3_num(text[j:i])
                            done = True
                        else:
                            ex = True
                    elif state == 4:
                        i += 1
                        if text[i] == '+' or text[i] == '-':
                            state = 5
                        elif text[i] in Lexical.digits:
                            state = 6
                        else:
                            ex = True
                    elif state == 5:
                        i += 1
                        if text[i] in Lexical.digits:
                            state = 6
                        else:
                            ex = True
                    elif state == 6:
                        i += 1
                        while text[i] in Lexical.digits:
                            i += 1
                        if text[i] in Lexical.r or text[i] in Lexical.o_one or text[i] + text[i + 1] \
                                in Lexical.o_double:
                            self.sem3_num(text[j:i])
                            done = True
                        else:
                            ex = True
                    elif state == 7:
                        i += 1
                        if text[i] in Lexical.digits:
                            state = 3
                        else:
                            ex = True

            # Комментарии семантическая процедура 0
            elif text[i] == '#':
                i = len(text)

            # Двулитерные операции
            elif text[i] + text[i + 1] in Lexical.o_double:
                self.sem5_o_double(text[i] + text[i + 1])
                i += 2

            # Однолитерные операции
            elif text[i] in Lexical.o_one:
                self.sem6_o_one(text[i])
                i += 1

            # Символьные и строковые константы
            elif text[i] == "'" or text[i] == '"':
                po = text.find(text[i], i + 1)
                if po != -1:
                    sub_text = text[i + 1: po]
                    self.sem7_con(sub_text)
                    i += po - i + 1
                else:
                    ex = True

            # Разделитель
            elif text[i] in Lexical.r:
                if text[i] != ' ':
                    self.sem4_r(text[i])
                i += 1

            else:
                ex = True

        return ex, i + 1

    def sem1_find_id(self, word: str):
        if word not in self.__ident:
            self.__ident[word] = 'i' + str(len(self.__ident))
        self.__main_text[len(self.__main_text) - 1].append(self.__ident[word])

    def sem2_find_w(self, word: str):
        if word in Lexical.w:
            self.__main_text[len(self.__main_text) - 1].append(Lexical.w[word])
        else:
            self.sem1_find_id(word)

    def sem3_num(self, number: str):
        if number not in self.__num:
            self.__num[number] = 'num' + str(len(self.__num))
        self.__main_text[len(self.__main_text) - 1].append(self.__num[number])

    def sem4_r(self, split_word: str):
        self.__main_text[len(self.__main_text) - 1].append(Lexical.r[split_word])

    def sem5_o_double(self, word: str):
        self.__main_text[len(self.__main_text) - 1].append(Lexical.o_double[word])

    def sem6_o_one(self, word: str):
        self.__main_text[len(self.__main_text) - 1].append(Lexical.o_one[word])

    def sem7_con(self, word: str):
        if word not in self.__con:
            self.__con[word] = 'con' + str(len(self.__con))
        self.__main_text[len(self.__main_text) - 1].append(self.__con[word])

    def sem8_p(self, word: str):
        self.__main_text[len(self.__main_text) - 1].append(Lexical.p[word])

    # get
    @property
    def ident(self):
        return self.__ident

    @property
    def num(self):
        return self.__num

    @property
    def con(self):
        return self.__con

    @property
    def main_text(self):
        return self.__main_text

    @property
    def functions(self):
        return self.__functions

    # set
    @ident.setter
    def ident(self, ident):
        self.__ident = ident

    @num.setter
    def num(self, num):
        self.__num = num

    @con.setter
    def con(self, con):
        self.__con = con

    @main_text.setter
    def main_text(self, main_text):
        self.__main_text = main_text

    @functions.setter
    def functions(self, functions):
        self.__functions = functions

    # Clear
    def clear(self):
        self.__ident = {}
        self.__num = {}
        self.__con = {}
        self.__main_text = []
