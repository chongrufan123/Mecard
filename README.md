# Mecard
Mecard是一个用python写成的简单的命令行工具，使用了fire框架，可以实现类似记忆卡片(memory card)的功能。抽查你对与题库中题目的理解或记忆程度。

## Getting Started
首先下载依赖的库
```
pip install -r requirements.txt
```

之后便可以跑程序了
```
# 开始记忆
python main.py start
# 手动添加题库
python main.py add
```
因为时间原因，像修改题库，删除题库等功能还没做出来，需要手动到card_bank/card.json进行删改查

## more informention
card_bank中有我这些日子总结好的所有题目，因为时间仓促，难免有疏忽错误的地方，望请原谅
