#!/usr/bin/env python
#encoding:utf8
import json

# 原始json数据
jsonData = [{'name': '张某某', 'age': 30, 'sex': '男'}, {'name': '李某', 'age': 20, 'sex': '女'}]

# 序列化，然后输出
jsonStr = json.dumps(jsonData, ensure_ascii=False)
print("序列化结果：")
print(jsonStr)

# 再将jsonStr反序列化为json格式
jsonData = json.loads(jsonStr)
print("反序列化整体结果：")
print(jsonData)
print("利用循环遍历反序列化结果：")
for each in jsonData:
    print(each['name'], each['age'], each['sex']);