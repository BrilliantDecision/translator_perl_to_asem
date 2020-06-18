from stack import Stack
from lexical_analyzer import Lexical


class Translator:

    def __init__(self, data: list, lexical: Lexical):
        # Служебные слова
        self.__w = {
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
        # операции
        self.__operators = {
            '+': 'o0',
            '-': 'o1',
            '*': 'o2',
            '/': 'o3',
            '<': 'o4',
            '>': 'o5',
            '=': 'o6',
            ':': 'o7',
            '!': 'o8',
            '**': 'o9',
            '==': 'o10',
            '!=': 'o11',
            '<=': 'o12',
            '>=': 'o13',
            '||': 'o14',
            '&&': 'o15'
        }
        # Разделители
        self.__r = {
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
        self.__main_text = []
        self.__identifiers = {value: key for key, value in lexical.ident.items()}
        self.__numbers = {value: key for key, value in lexical.num.items()}
        self.__chars = {value: key for key, value in lexical.con.items()}

        self.__gf = self.__lf = self.__ef = self.__nf = False

        self.__cur_function_name = []
        self.__data = data
        self.__translated_data = []
        self.__dijkstra = Stack()
        self.__added_ident = []
        self.__declaration = []
        self.__metki = []

    @staticmethod
    def is_number(variable: str):
        o = True
        try:
            int(variable)
        except ValueError:
            o = False
        return o

    def find_identifiers(self, leksem: str):
        res = ''
        if leksem in self.__identifiers:
            res = self.__identifiers.get(leksem)
        if leksem in self.__numbers:
            res = self.__numbers.get(leksem)
        if leksem in self.__chars:
            res = self.__chars.get(leksem)
        return res

    def add_to_declaration(self, variable: str):
        if not self.is_number(variable):
            if variable not in self.__added_ident:
                self.__added_ident.append(variable)
                line = 'extern ' + variable + ':DB'
                self.__declaration.append(line)

    def basic_operation(self, my_type: int, is_num: bool, first_oper: str, second_oper: str):
        op = ''
        if my_type == 1:
            op = 'add'
        elif my_type == 2:
            op = 'sub'
        elif my_type == 3:
            op = 'imul'
        elif my_type == 4:
            op = 'idiv'
        elif my_type == 12:
            op = 'mov'

        line = 'mov ax,[' + first_oper + ']'
        self.__translated_data.append(line)
        if not is_num:
            line = 'mov bx,[' + second_oper + ']'
            self.__translated_data.append(line)
            line = op + ' ax,bx'
        else:
            line = op + ' ax,' + second_oper
        self.__translated_data.append(line)
        line = 'mov [' + first_oper + '],ax'
        self.__translated_data.append(line)

    def compare_operator(self, my_type: int, is_num: bool, first_oper: str, second_oper: str):
        if my_type == 1:
            self.__gf = True
        elif my_type == 2:
            self.__lf = True
        elif my_type == 3:
            self.__ef = True
        elif my_type == 4:
            self.__ef = True
            self.__nf = True
        elif my_type == 5:
            self.__lf = True
            self.__ef = True
        elif my_type == 6:
            self.__gf = True
            self.__ef = True

        line = 'mov ax,[' + first_oper + ']'
        self.__translated_data.append(line)
        if not is_num:
            line = 'mov bx,[' + second_oper + ']'
            self.__translated_data.append(line)
            line = 'cmp ax,bx'
        else:
            line = 'cmp ax,' + second_oper
        self.__translated_data.append(line)

    def jump_operation(self, metka: str, clear_flags: bool):
        oper = 'j'
        ch = False
        if self.__nf:
            ch = True
            oper = 'n'
            self.__nf = not clear_flags
        if self.__gf:
            ch = True
            oper += 'g'
            self.__gf = not clear_flags
        if self.__lf:
            ch = True
            oper += 'l'
            self.__lf = not clear_flags
        if self.__ef:
            ch = True
            oper += 'e'
            self.__ef = not clear_flags
        if not ch:
            oper = 'jump'
        self.__translated_data.append(oper + ' ' + metka)

    def translate_operation(self, operation: str):
        second = self.__dijkstra.pop()
        first = self.__dijkstra.pop()
        first_oper = self.find_identifiers(first)
        second_oper = self.find_identifiers(second)
        self.add_to_declaration(first_oper)
        self.add_to_declaration(second_oper)
        is_num = self.is_number(second_oper)
        compare = False
        if operation == 'o0':
            self.basic_operation(1, is_num, first_oper, second_oper)
        elif operation == 'o1':
            self.basic_operation(2, is_num, first_oper, second_oper)
        elif operation == 'o2':
            self.basic_operation(3, is_num, first_oper, second_oper)
        elif operation == 'o3':
            self.basic_operation(4, is_num, first_oper, second_oper)
        elif operation == 'o6':
            self.basic_operation(12, is_num, first_oper, second_oper)

        elif operation == 'o4':
            self.compare_operator(1, is_num, first_oper, second_oper)
            compare = True
        elif operation == 'o5':
            self.compare_operator(2, is_num, first_oper, second_oper)
            compare = True
        elif operation == 'o10':
            self.compare_operator(3, is_num, first_oper, second_oper)
            compare = True
        elif operation == 'o11':
            self.compare_operator(4, is_num, first_oper, second_oper)
            compare = True
        elif operation == 'o12':
            self.compare_operator(5, is_num, first_oper, second_oper)
            compare = True
        elif operation == 'o13':
            self.compare_operator(6, is_num, first_oper, second_oper)
            compare = True
        if not compare:
            self.__dijkstra.push(first)

    def translate_jump(self, jump_type: str):
        if jump_type == 'FT':
            self.jump_operation(self.__metki[len(self.__metki) - 1], True)
        if jump_type == 'UT':
            self.jump_operation(self.__metki[len(self.__metki) - 1], False)

    def translate_metka(self, metka: str):
        metka = metka.replace(':', '')
        if metka in self.__metki:
            self.__metki.remove(metka)
            self.__translated_data.append(metka + ': ')
        else:
            self.__metki.append(metka)

    def translate_number(self, number: str):
        self.__dijkstra.push(number)

    def translate_cs(self):
        second = self.__dijkstra.pop()
        first = self.__dijkstra.pop()
        metka = 'M' + first + second
        self.__metki.append(metka)

    def translate_ret(self):
        arguments = []
        while self.__dijkstra.size() > 0 and (self.__dijkstra.peek()[0] == 'i' or self.__dijkstra.peek()[0:3] == 'num' or self.__dijkstra.peek()[0:3] == 'con'):
            arguments.append(self.__dijkstra.pop())
        for i in range(len(arguments)):
            arguments[i] = self.find_identifiers(arguments[i])
        for i in arguments:
            self.add_to_declaration(i)
            self.__translated_data.append('mov ax,[' + i + ']')
            self.__translated_data.append('push ax')
        self.__translated_data.append('ret')

    def translate_fs(self):
        self.__dijkstra.pop()
        self.__dijkstra.pop()
        self.__cur_function_name = self.find_identifiers(self.__dijkstra.pop())
        # arguments = []
        # while self.__dijkstra.size() > 0 and (self.__dijkstra.peek()[0] == 'i' or self.__dijkstra.peek()[0:3] == 'num' or self.__dijkstra.peek()[0:3] == 'con'):
        #     arguments.append(self.__dijkstra.pop())
        # for i in range(len(arguments)):
        #     arguments[i] = self.find_identifiers(arguments[i])
        self.__translated_data.append(self.__cur_function_name + ' proc')
        # for i in arguments:
        #     self.add_to_declaration(i)
        self.__translated_data.append('pop ax')
        self.__translated_data.append('mov [_], ax')

    def translate_fe(self):
        self.__translated_data.append(self.__cur_function_name + ' endp')

    def translate_ce(self):
        metka = self.__metki[len(self.__metki) - 1]
        metka2 = metka + str(len(self.__metki))
        index = 0
        for i in range(len(self.__translated_data)):
            if 'cmp' in self.__translated_data[i]:
                index = i
        index -= 2
        self.__translated_data[index] = metka2 + ': ' + self.__translated_data[index]
        self.__translated_data.append('jump ' + metka2)
        self.__translated_data.append(metka + ': ')
        self.__metki.remove(metka)

    def translate_function(self, func: str):
        count = int(str(func[0]))
        arguments = []
        while count > 1:
            arguments.append(self.__dijkstra.pop())
            count -= 1
        for i in range(len(arguments)):
            arguments[i] = self.find_identifiers(arguments[i])
        func_name = self.find_identifiers(self.__dijkstra.pop())
        for i in arguments:
            self.add_to_declaration(i)
            self.__translated_data.append('mov ax,[' + i + ']')
            self.__translated_data.append('push ax')
        self.__translated_data.append('call ' + func_name)
        self.__translated_data.append('pop ax')
        self.__translated_data.append('mov [' + arguments[0] + '],ax')
        arrg = ''
        o = True
        for key, value in self.__identifiers.items():
            if value == arguments[0] and o:
                arrg = key
                o = False
        self.__dijkstra.push(arrg)

    def translate(self):
        self.__declaration.append('extern _:DB')
        for i in range(len(self.__data)):
            is_produced = False
            if not is_produced and self.is_number(self.__data[i]):
                self.translate_number(self.__data[i])
                is_produced = True
            if not is_produced and (self.__data[i][0] == 'i' or self.__data[i][0:3] == 'num' or self.__data[i][0:3] == 'con'):
                self.__dijkstra.push(self.__data[i])
                is_produced = True
            if not is_produced and self.__data[i][0] == 'o':
                self.translate_operation(self.__data[i])
                is_produced = True
            if not is_produced and (self.__data[i] == 'FT' or self.__data[i] == 'UT'):
                self.translate_jump(self.__data[i])
                is_produced = True
            if not is_produced and self.__data[i][0] == 'M':
                self.translate_metka(self.__data[i])
                is_produced = True
            if not is_produced and self.__data[i] == 'CS':
                self.translate_cs()
                is_produced = True
            if not is_produced and self.__data[i] == 'CE':
                self.translate_ce()
                is_produced = True
            if not is_produced and self.__data[i] == 'FS':
                self.translate_fs()
                is_produced = True
            if not is_produced and self.__data[i] == 'FE':
                self.translate_fe()
                is_produced = True
            if not is_produced and self.__data[i] == 'w2':
                self.translate_ret()
                is_produced = True
            if not is_produced and len(self.__data[i]) > 1 and self.__data[i][1] == 'F':
                self.translate_function(self.__data[i])
                is_produced = True
        self.__declaration.append('.code')
        self.__declaration += self.__translated_data
        self.__declaration.append('ret')
        self.__main_text = self.__declaration
        return self.__declaration

    def invertDictionary(self, orig_dict):
        result = {}  # or change to defaultdict(list)
        for k, v in orig_dict.iteritems():
            result.setdefault(v, []).append(k)
        return result













