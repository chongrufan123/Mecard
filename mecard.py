import json
import random
from typing import List
import datetime  # 添加

class Card:
    def __init__(self):
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
        self.questions = []

    def load_categories(self):
        for category, name in self.categories_dict.items():
                print(f'{category}. {name}')
            
    def add(self):
        self.questions = self.load_questions()
        self.load_categories()
        category = input('请选择题目的类别（输入数字）：')
        if not category.isdigit() or int(category) not in range(1, 10):
            print('输入错误')
            return
        while True:
            title = input('请输入题目标题：')
            content = []
            print('请输入题目内容（以一个空白回车作为结束）：')
            while True:
                line = input()
                if line.strip() == '':
                    break
                content.append(line)
            content = '\n'.join(content).replace('，', ', ').replace('\*', '*').replace('\t', '')
            question = {'category': int(category), 'title': title, 'content': content, 'times': 0}
            self.questions.append(question)
            print('题目添加成功！')
            print("---------------")
            juage = input("有以下几种选择：\n保持当前类别：直接按回车；\n更换类别：输入要更换类别的数字\n查看有哪些类别：c；\n结束插入题目：n\n请输入：")
            if juage == 'c':
                self.load_categories()
                category = input('请选择题目的类别（输入数字）：')
                while not category.isdigit() or int(category) not in range(1, 10):
                    print('输入错误')
                    category = input('请选择题目的类别（输入数字）：')
            if juage == 'n':
                break
            if juage.isdigit() and int(juage) in range(1, 10):
                category = juage
            print("---------------")
        with open('card.json', 'w') as f:
            json.dump(self.questions, f, ensure_ascii=False, indent=4)
        

    def start(self):
        self.questions = self.load_questions()
        category = self.select_category()
        mode = self.select_mode()
        self.memory(category, mode)

    def load_questions(self) -> List[dict]:
        with open('card.json', 'r') as f:
            return json.load(f)

    def select_category(self) -> int:
        while True:
            print('请选择题库的类别：')
            self.load_categories()
            choice = input()
            if choice.isdigit() and int(choice) in range(10):
                return int(choice)

    def select_mode(self) -> int:
        while True:
            print('请选择记忆模式：')
            print('1. 顺序记忆')
            print('2. 随机记忆')
            choice = input()
            if choice.isdigit() and int(choice) in range(1, 3):
                return int(choice)

    def memory(self, category: int, mode: int):
        if category == 0:
            selected_questions = self.questions
        else:
            selected_questions = [q for q in self.questions if q['category'] == category]
        if mode == 1:
            selected_questions = sorted(selected_questions, key=lambda q: q['title'])
        else:
            random.shuffle(selected_questions)
        correct_count = 0
        total_count = 0
        for question in selected_questions:
            total_count += 1
            print(question['title'])
            answer = input()
            if answer.lower() == 'n':
                question['times'] += 1  # 添加
            else:
                correct_count += 1
                # break
            # if answer == question['content']:
            #     correct_count += 1
            #     print('回答正确！')
            # else:
            #     question['times'] += 1
            #     print('回答错误！')
            print(question['content'])
            print()
            continue_memory = input('是否继续？（y/n）')
            if continue_memory.lower() == 'n':
                break
            print("----------------")
        incorrect_count = total_count - correct_count
        accuracy = (1 - incorrect_count / total_count) * 100 if total_count > 0 else 0
        print(f'您答对了{correct_count}道题，答错了{incorrect_count}道题，正确率为{accuracy:.2f}%。')
        with open('stat.md', 'a') as f:
            # f.write(f'{accuracy:.2f}%,{total_count},{correct_count},{incorrect_count},{datetime.datetime.now()}\n')
            f.write(f'|{datetime.datetime.now().strftime("%Y-%m-%d")}|{accuracy:.2f}%|{total_count}|{correct_count}|{incorrect_count}|\n')
