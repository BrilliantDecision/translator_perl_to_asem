from stack import Stack


class OPZ:
    # Таблица приоритетов
    priority = {
        'r4': 0, # (
        'r9': 0, # [
        'r0': 0, # {
        'w0': 0, # print
        'w1': 0, # sub
        'w3': 0, # if
        'w13':0, # do
        'w6': 0, # while
        'w7': 0, # for
        'АЭМ': 0,
        'F': 0,
        'r1': 1, # }
        'r2': 1, # ;
        'r5': 1, # )
        'r3': 1, # ,
        'r10': 1, # ]
        'r13': 1, # .
        'p1': 1, # @
        'w4': 1, # else
        'o6': 2, # =
        'w2': 2, # return
        'w5': 2, # goto
        'o14': 2, # ||
        'o15': 3, # &&
        'o8': 4, # !
        'o5': 5, # >
        'o4': 5, # <
        'o13': 5, # >=
        'o12': 5, # <=
        'o10': 5, # ==
        'o11': 5, # !=
        'o0': 6, # +
        'o1': 6, # -
        'o2': 7, # *
        'o3': 7, # /
        'o9': 8, # **
        'o7': 9 # :
    }

    def __init__(self):
        self.__reversed_text = []

# поступает [[],[],[]]
    def returner_opz(self, text_list: list):
        dijkstra = Stack()
        depth = 0
        cycle_number = 0
        function_number = 0
        ind_count = 0
        goto_check = False
        metka_number = 0
        last_leksem = 'J0'
        function_name = ''
        terminate_by_skobka = False
        function_started = False
        waiting_for_function_name = False
        waiting_for_mas_begin = False
        waiting_for_mas_end = False
        func_count = 0
        variable_count = 0
        for i in text_list:
            is_processed = False
            stack_top = ''
            if dijkstra.size() > 0:
                stack_top = dijkstra.peek()
            # Идентификаторы
            if not is_processed and (i[0] == 'i' or i[0:3] == 'num' or i[0:3] == 'con'):
                if not waiting_for_function_name:
                    self.__reversed_text.append(i)
                else:
                    function_name = i
                    waiting_for_function_name = False
                if goto_check:
                    self.__reversed_text.append("UT")
                    goto_check = False
                is_processed = True
            # @
            if not is_processed and i == 'p1':
                waiting_for_mas_begin = True
                is_processed = True
            if not is_processed and i == 'w13':
                cycle_number += 1
                dijkstra.push(i)
                is_processed = True
            if not is_processed and i == 'w7':
                cycle_number += 1
                dijkstra.push(i)
                is_processed = True
            if not is_processed and i == 'w6':
                if dijkstra.size() == 0 or dijkstra.peek() != 'w13':
                    cycle_number += 1
                    dijkstra.push(i)
                is_processed = True
            if not is_processed and i == 'w1':
                function_number += 1
                dijkstra.push(i)
                function_started = True
                waiting_for_function_name = True
                is_processed = True
            if not is_processed and i == 'w5':
                goto_check = True
                is_processed = True
            if not is_processed and i == 'w3':
                dijkstra.push(i)
                is_processed = True
            if not is_processed and i == 'w4':
                metka_number += 1
                self.__reversed_text.insert(len(self.__reversed_text) - 1, 'M' + str(metka_number))
                self.__reversed_text.insert(len(self.__reversed_text) - 1, 'UT')
                dijkstra.push('w3')
                is_processed = True
            if not is_processed and i == 'r2':
                while dijkstra.size() > 0 and dijkstra.peek() != 'w3' and dijkstra.peek() != 'r4' and dijkstra.peek() != 'w1' and dijkstra.peek() != 'w7' and dijkstra.peek() != 'w13' and dijkstra.peek() != 'w6':
                    self.__reversed_text.append(dijkstra.pop())
                if dijkstra.size() > 0 and dijkstra.peek() == 'w3':
                    if not terminate_by_skobka:
                        self.__reversed_text.append('M' + str(metka_number) + ':')
                        dijkstra.pop()
                is_processed = True
            if not is_processed and i == 'r4':
                if waiting_for_mas_begin:
                    ind_count = 2
                    dijkstra.push('AEA')
                    waiting_for_mas_begin = False
                    waiting_for_mas_end = True
                elif not function_started and last_leksem[0] == 'i':
                    dijkstra.push('F')
                    func_count = 1
                else:
                    dijkstra.push(i)
                is_processed = True
            if not is_processed and i == 'r5':
                if waiting_for_mas_end:
                    while dijkstra.size() > 0 and 'AEA' not in dijkstra.peek():
                        self.__reversed_text.append(dijkstra.pop())
                    self.__reversed_text.append(str(ind_count) + dijkstra.pop())
                    ind_count = 0
                    waiting_for_mas_end = False
                    is_processed = True
                else:
                    while dijkstra.size() > 0 and dijkstra.peek() != 'r4' and dijkstra.peek() != 'F':
                        self.__reversed_text.append(dijkstra.pop())
                    if not is_processed and not function_started and dijkstra.peek() == 'F':
                        func_count += 1
                        self.__reversed_text.append(str(func_count) + 'F')
                        func_count = 0
                        is_processed = True
                    dijkstra.pop()
                    if not is_processed and dijkstra.size() > 0 and dijkstra.peek() == 'w3':
                        metka_number += 1
                        self.__reversed_text.append('M' + str(metka_number))
                        self.__reversed_text.append('FT')
                        is_processed = True
                    if not is_processed and dijkstra.size() > 0 and dijkstra.peek() == 'w1':
                        self.__reversed_text.append(function_name)
                        self.__reversed_text.append(str(function_number))
                        self.__reversed_text.append(str(depth))
                        self.__reversed_text.append('FS')
                        function_name = ''
                        is_processed = True
                    if not is_processed and dijkstra.size() > 0 and dijkstra.peek() == 'w6':
                        self.__reversed_text.append(str(cycle_number))
                        self.__reversed_text.append(str(depth))
                        self.__reversed_text.append('CS')
                        self.__reversed_text.append('FT')
                        is_processed = True
                    if not is_processed and dijkstra.size() > 0 and dijkstra.peek() == 'w7':
                        self.__reversed_text.append(str(cycle_number))
                        self.__reversed_text.append(str(depth))
                        self.__reversed_text.append('CS')
                        self.__reversed_text.append('FT')
                        is_processed = True
                    if not is_processed and dijkstra.size() > 0 and dijkstra.peek() == 'w13':
                        self.__reversed_text.append('CE')
                        dijkstra.pop()
                        is_processed = True
                    function_started = False
                    is_processed = True
            if not is_processed and i == 'r9':
                ind_count = 2
                dijkstra.push('AEA')
                is_processed = True
                if waiting_for_mas_begin:
                    waiting_for_mas_begin = False
            if not is_processed and i == 'r3':
                while dijkstra.size() > 0 and 'AEA' not in dijkstra.peek() and 'F' not in dijkstra.peek() and dijkstra.peek() != 'r4' and dijkstra.peek() != 'p1':
                    self.__reversed_text.append(dijkstra.pop())
                current_leks = dijkstra.peek()
                if current_leks == 'AEA':
                    ind_count += 1
                if not function_started and current_leks == 'F':
                    func_count += 1
                is_processed = True
            if not is_processed and i == 'r10':
                while dijkstra.size() > 0 and 'AEA' not in dijkstra.peek():
                    self.__reversed_text.append(dijkstra.pop())
                self.__reversed_text.append(str(ind_count) + dijkstra.pop())
                ind_count = 0
                is_processed = True
            if not is_processed and i == 'r0':
                ###
                if dijkstra.size() > 0 and dijkstra.peek() == 'w1' and last_leksem != 'r5':
                    self.__reversed_text.append(function_name)
                    self.__reversed_text.append(str(function_number))
                    self.__reversed_text.append(str(depth))
                    self.__reversed_text.append('FS')
                    function_name = ''
                    function_started = False
                self.__reversed_text.append('PS')
                if dijkstra.peek() == 'w3':
                    terminate_by_skobka = True
                if not is_processed and dijkstra.size() > 0 and dijkstra.peek() == 'w13':
                    self.__reversed_text.append(str(cycle_number))
                    self.__reversed_text.append(str(depth))
                    self.__reversed_text.append('CS')
                    self.__reversed_text.append('FT')
                depth += 1
                is_processed = True
            if not is_processed and i == 'r1':
                self.__reversed_text.append('PE')
                if terminate_by_skobka:
                    self.__reversed_text.append('M' + str(metka_number) + ':')
                    print(self.__reversed_text)
                    dijkstra.pop()
                    terminate_by_skobka = False
                if dijkstra.size() > 0 and dijkstra.peek() == 'w1':
                    self.__reversed_text.append('FE')
                    dijkstra.pop()
                if dijkstra.size() > 0 and dijkstra.peek() == 'w7':
                    self.__reversed_text.append('CE')
                    dijkstra.pop()
                if dijkstra.size() > 0 and dijkstra.peek() == 'w6':
                    self.__reversed_text.append('CE')
                    dijkstra.pop()
                depth -= 1
                is_processed = True
            if not is_processed and dijkstra.size() == 0:
                dijkstra.push(i)
                is_processed = True
            if not is_processed and self.priority[dijkstra.peek()] < self.priority[i]:
                dijkstra.push(i)
                is_processed = True
            if not is_processed and self.priority[dijkstra.peek()] >= self.priority[i]:
                while dijkstra.size() > 0 and self.priority[dijkstra.peek()] >= self.priority[i]:
                    self.__reversed_text.append(dijkstra.pop())
                dijkstra.push(i)
                is_processed = True
            last_leksem = i
        return self.__reversed_text

    @property
    def reversed_text(self):
        return self.__reversed_text

    @reversed_text.setter
    def reversed_text(self, text):
        self.__reversed_text = text

    def clear(self):
        self.__reversed_text = []
