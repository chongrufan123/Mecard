import json
import random
from typing import List
import datetime  # 添加

class Card:
    def __init__(self):
        # 定义题目分类字典
        self.categories_dict = {
            1: '密码学',
            2: '网络安全',
            3: '数据库',
            4: '体系结构与组成原理',
            5: '软件工程',
            6: '操作系统',
            7: '计算机网络',
            8: '数据结构',
            9: '编程语言',
        }
        # 初始化题目列表为空
        self.questions = []

    def load_categories(self):
        # 输出题目分类列表
        for category, name in self.categories_dict.items():
                print(f'{category}. {name}')
            
    def add(self):
        # 加载题目列表
        self.questions = self.load_questions()
        # 输出题目分类列表
        self.load_categories()
        # 用户选择题目分类
        category = input('请选择题目的类别（输入数字）：')
        if not category.isdigit() or int(category) not in range(1, 10):
            print('输入错误')
            return
        while True:
            # 用户输入题目标题
            title = input('请输入题目标题：')
            # 用户输入题目内容，以空行结束
            content = []
            print('请输入题目内容（以一个空白回车作为结束）：')
            while True:
                line = input()
                if line.strip() == '':
                    break
                content.append(line)
            # 格式化题目内容
            content = '\n'.join(content).replace('，', ', ').replace('\*', '*').replace('\t', '')
            # 将题目信息添加到题目列表中
            question = {'category': int(category), 'title': title, 'content': content, 'times': 0}
            self.questions.append(question)
            print('题目添加成功！')
            print("---------------")
            # 提供用户选择，继续添加题目或退出添加
            juage = input("有以下几种选择：\n保持当前类别：直接按回车；\n更换类别：输入要更换类别的数字\n查看有哪些类别：c；\n结束插入题目：n\n请输入：")
            if juage == 'c':
                self.load_categories()
                # 用户选择题目分类
                category = input('请选择题目的类别（输入数字）：')
                while not category.isdigit() or int(category) not in range(1, 10):
                    print('输入错误')
                    category = input('请选择题目的类别（输入数字）：')
            if juage == 'n':
                break
            if juage.isdigit() and int(juage) in range(1, 10):
                category = juage
            print("---------------")
        # 将题目列表保存到json文件中
        with open('card.json', 'w') as f:
            json.dump(self.questions, f, ensure_ascii=False, indent=4)
        

    def start(self):
        self.questions = self.load_questions()  # 加载题目列表
        category = self.select_category()   # 用户选择题目分类
        mode = self.select_mode()           # 用户选择记忆模式
        self.memory(category, mode)     # 开始记忆

    def load_questions(self) -> List[dict]:
        with open('card.json', 'r') as f:  # 打开文件 card.json 用于读取
            return json.load(f)  # 使用 json.load() 方法从文件中读取数据并返回一个列表

    # 定义一个方法用于选择题目类别
    def select_category(self) -> int:
        while True:
            print('请选择题库的类别：')
            self.load_categories()  # 调用 load_categories() 方法显示所有可选的题目类别
            choice = input()  # 接收用户输入
            if choice.isdigit() and int(choice) in range(10):  # 如果用户输入的是数字并且在 0~9 的范围内
                return int(choice)  # 返回用户输入的数字作为选择的题目类别

    # 定义一个方法用于选择记忆模式
    def select_mode(self) -> int:
        while True:
            print('请选择记忆模式：')
            print('1. 顺序记忆')
            print('2. 随机记忆')
            choice = input()  # 接收用户输入
            if choice.isdigit() and int(choice) in range(1, 3):  # 如果用户输入的是数字并且在 1~2 的范围内
                return int(choice)  # 返回用户输入的数字作为选择的记忆模式

    # 定义一个方法用于进行记忆
    def memory(self, category: int, mode: int):
        if category == 0:  # 如果选择的题目类别为 0（即所有题目）
            selected_questions = self.questions  # 将所有题目作为需要记忆的题目
        else:
            # 否则，从所有题目中选择与选择的类别相同的题目
            selected_questions = [q for q in self.questions if q['category'] == category]
        if mode == 1:  # 如果选择的是顺序记忆模式
            # 按照题目标题进行排序
            selected_questions = sorted(selected_questions, key=lambda q: q['title'])
        else:  # 否则选择的是随机记忆模式
            random.shuffle(selected_questions)  # 随机打乱题目的顺序
        correct_count = 0  # 初始化答对的题目数量为 0
        total_count = 0  # 初始化答题总数为 0
        for question in selected_questions:  # 遍历需要记忆的题目
            total_count += 1  # 记录答题总数
            print(question['title'])  # 显示题目标题
            answer = input()  # 接收用户输入的答案
            if answer.lower() == 'n':  # 如果用户输入的是 n，则表示不知道答案
                question['times'] += 1  # 将该题的记忆次数加 1
            else:  # 否则用户输入了答案
                correct_count += 1  # 答对的题目数量加 1
            print(question['content'])  # 显示
            print()
            continue_memory = input('是否继续？（y/n）')
            if continue_memory.lower() == 'n':
                break
            print("----------------")
        incorrect_count = total_count - correct_count  # 计算答错的题目数量
        accuracy = (1 - incorrect_count / total_count) * 100 if total_count > 0 else 0  # 计算正确率，如果总题数为0则正确率为0
        print(f'您答对了{correct_count}道题，答错了{incorrect_count}道题，正确率为{accuracy:.2f}%。')  # 输出答题结果
        with open('stat.md', 'a') as f:  # 打开或创建一个 Markdown 文件，用于记录答题结果
            f.write(f'|{datetime.datetime.now().strftime("%Y-%m-%d")}|{accuracy:.2f}%|{total_count}|{correct_count}|{incorrect_count}|\n')  # 将结果以表格形式写入 Markdown 文件
