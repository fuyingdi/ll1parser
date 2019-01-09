from pprint import pprint
import prettytable as pt
from collections import OrderedDict as odict


class Parser:
    '解析文法文件'

    lines = []
    terminal = set()  # 终结符
    nonterminal = set()  # 非终结符
    follow = {} # follow集
    first = {}
    start = ''
    pretable = odict() # 预测分析表
    can_be_empty = [] # 能推导出空串的非终

    def open(self, path):
        with open(path) as f:
            for line in f:
                self.lines.append(line.strip('\n').replace(' ',''))
                self.nonterminal.add(line[0])
            # 分割一遍
            _tosplit = []
            for line in self.lines:
                if '|' in line:
                    _tosplit.append(line)
            for _line in _tosplit:
                self._split(_line)

            # 初始化终结符和非终结符集
            for line in self.lines:
                for char in line.split('->')[1]:
                    if char not in self.nonterminal:
                        self.terminal.add(char)
            self.terminal.add('#')
            # 初始化可推导出空串的非终结符集合，两次扫描
            for line in self.lines:
                left, right = line.split('->')
                if right=='@':
                    self.can_be_empty.append(left)
            for line in self.lines:
                left, right = line.split('->')
                _flag = True
                for char in right:
                    if char not in self.can_be_empty:
                        _flag = False
                if _flag:
                    self.can_be_empty.append(left)




            left,right = self.lines[0].split('->')
            self.start = left

        for non in self.nonterminal:
            self.first[non] = [set(), set()]
            self.follow[non] = [set(), set(), set()] # 三个集合分别为，终结符集合，非终结符First集,非终结符Follow集
        for ter in self.terminal:
            self.pretable[ter] = odict()
            for non in self.nonterminal:
                self.pretable[ter][non] = 'error'


    def make_first(self):
        # 终结符直接放到第一个set，非终结符暂时放到第二个set
        for line in self.lines:
            left,right = line.split('->')
            if right[0] in self.terminal:
                assert isinstance(self.first[left][0], set)
                self.first[left][0].add(right[0])
            elif right[0] in self.nonterminal:
                # 如果第一个非终结符能推导出空串的情况
                if right[0] in self.can_be_empty:
                    self.first[left][1].add(right[1])
                self.first[left][1].add(right[0])

        #处理第二个set，将非终结符的first集合添加倒第一个set，移除非终结符，直到第二个set为空
        for item in self.nonterminal:
            while(len(self.first[item][1])>0):
                for _non in self.first[item][1].copy():
                    self.first[item][0] |= (self.first[_non][0]-{'@'})
                    # self.first[item][1] |= self.first[_non][1]
                    self.first[item][1].remove(_non)
        for item in self.can_be_empty:
            self.first[item][0].add('@')
        for item in self.nonterminal:
            del self.first[item][1]




    def make_follow(self):
        # 把#放入开始符号的follow集中
        self.follow[self.start][0].add('#')
        # 非终结符直接放到第一个set,非终结符的first集和follow集暂时放到第2和第3个set
        for production in self.lines:
            left,right = production.split('->')
            for i in range(len(right)-1):
                # print("debug:current nonterminal{}".format(right[i]))
                if right[i] in self.nonterminal:
                    # 非终结符紧跟一个终结符的情况
                    if right[i+1] in self.terminal:
                        self.follow[right[i]][0].add(right[i+1])
                    # 非终结符紧跟一个非终结符的情况
                    elif right[i+1] in self.nonterminal:
                        self.follow[right[i]][1].add(right[i+1])
                        # 如果后跟的非终结符含有空串@,就把其follow集也加入
                        if '@' in self.first[right[i+1]]:
                            self.follow[right[i]][2].add(right[i+1])
            # 对形如U－>…P的产生式的情况，把Follow(U)添加倒Follow（P)
            _tmp = right[len(right)-1]
            if _tmp in self.nonterminal:
                if _tmp is not left:
                    self.follow[_tmp][2].add(left)
        # 处理第2，3个集合直到为空
        notempty = 1
        while(notempty>0):
            for item in self.follow:
                if len(self.follow[item][2])>0:
                    _toremove = []
                    for ans in self.follow[item][2]:
                        self.follow[item][0] |= self.follow[ans][0]
                        self.follow[item][1] |= self.follow[ans][1]
                        _toremove.append(ans)
                    # 移除第3个集合中非终结符
                    for i in _toremove:
                        self.follow[item][2].remove(i)

            for item in self.follow:
                if len(self.follow[item][1])>0:
                    _toremove = []
                    for ans in self.follow[item][1]:
                        self.follow[item][0] |= self.first[ans][0]
                        _toremove.append(ans)
                    # 移除第2个集合中非终结符
                    for i in _toremove:
                        self.follow[item][1].remove(i)
            for item in self.follow:
                if self.follow[item][1]!=set() or (self.follow[item][2]!=set()):
                    notempty += 1
                    break
            notempty -= 1


    def make_pretable(self):
        '''
        (1)对First(A)中的每一个终结符a，把A->XXX加入M[A,a]中。
        (2)若‘空’在First(A)中，把Follow(A)的每一个终结符b(包括$)，
            把A->XXX加入M[A,b]中。剩下为错误条目，空白处理。
        '''
        # 执行步骤(1)
        for line in self.lines:
            # left和x作为坐标确定分析表中的位置
            left, right = line.split('->')
            isempty_exist = False
            for x in self.first[left][0]:
                if x == '@':
                    isempty_exist = True
                self._set_tableitem(x, left, line)
            # 执行步骤(2)
            if isempty_exist:
                for x in self.follow[left][0]:
                    self._set_tableitem(x, left, line)



    def ll1(self, str):
        pass



    def _split(self, line):
        # 分割带有 '|' 的产生式
        left, right = line.split('->')
        factions = right.split('|')
        for faction in factions:
            self.lines.append(left + '->' + faction)
        # 删除被分割的产生式
        self.lines.remove(line)


    def _set_tableitem(self, x, y, content):
        try:
            if self.pretable[x][y] == 'error' or self.pretable[x][y] == content:
                self.pretable[x][y] = content
            else:
            #    print("{}将被替换为{}".format(self.pretable[x][y], content))
                self._error(self.pretable[x][y], content, x, y)
        except:
            print("x:{}y:{}content:{}".format(x, y, content))
    def _error(self, str1, str2, x, y):
        print("不是LL1文法,冲突为{},{},位置为{}，{}".format(str1, str2, x, y))



if __name__ == '__main__':
    parser = Parser()
    parser.open('data.txt')
    print(parser.lines)
    print(parser.nonterminal)
    print(parser.terminal)
    print("start symbol:{}".format(parser.start))

    parser.make_first()
    parser.make_follow()
    parser.make_pretable()

    print ("\033[;32m first\033[0m")
    pprint(parser.first,width=30)
    print ("\033[;32m follow\033[0m")
    pprint(parser.follow,width=40)
    print ("\033[;32m can be empty\033[0m")
    pprint(parser.can_be_empty,width=40)
    # pprint(parser.pretable,width=200)

    tb = pt.PrettyTable()
    # tb.field_names = parser.pretable.keys()
    _flag = True
    for key1 in parser.pretable.keys():
        if _flag:
            tb.add_column(" ", list(parser.pretable[key1]))
            _flag = False
        tb.add_column(key1,list(parser.pretable[key1].values()))


    print(tb)