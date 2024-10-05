"""
 jsonpath:用来解析多层嵌套json数据

 安装： pip install jsonpath -i https://mirrors.aliyun.com/pypi/simple/

"""
import jsonpath
import json


# 读取json文件内容并进行解析
json_file=open("文件/a.json","r")
json_dict=json.load(json_file)
json_file.close()
# 使用jsonpath解析获取age或者name的值
# 获取年龄
code_name="$.store.book[*].name"
msg=jsonpath.jsonpath(json_dict,code_name)
print(msg)
