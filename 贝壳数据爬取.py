"""
  贝壳数据爬取：
      静态网页：可以直接使用beautifulsoup html5lib库进行解析
      动态网页：涉及到json数据

    思路分析：
        1.分析网站是静态的还是动态的？------------->动态的，考虑可以是json数据
        2.异步请求，json数据怎么获取?，链接地址在哪里？
        3.获取json数据进行解析
        4.将想要的数据进行存储，存储在excel或者csv或者mysql数据库中

    实现思路：
       1.在控制台打印商圈  区域 地铁数据并进行选择
       2.选择对应的编号之后打印输出二级菜单对应的内容
"""
import math
import os
import jsonpath
import requests
import json

import pymysql
from mysqlUtils import MysqlDB

# 创建对象
my_db=MysqlDB()

table_name="beke"
# 创建表
create_table="create table {}(id int not null primary key auto_increment,title varchar(255),rentPrice varchar(255),unitDesc varchar(255),districtName varchar(255),bizcircleName varchar(255));".format(table_name)
my_db.commit_data(create_table)
pass


# 获取选项地址
other_url="https://shangye.ke.com/api/ke/filters/location/xzl_star?platform=2&device=1&business_type=2&page_type=2&city_code=440300&cityCode=440300&menu_type=house%3Amenu%3Ahouse%3Arent"

headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}

# 详情url地址
home_data_url="https://shangye.ke.com/api/ke/xzl/getHouseDetail?platform=1&device=1&business_type=2&house_code={}&crep_channel="

url_dic={
    "热门商圈":"https://shangye.ke.com/api/c/house/list?platform=1&device=1&page=0&city_id=440300&size=20&big_bizcircle_id=&district_id={}&bizcircle_id%5B0%5D={}&subway_id=&resblock_id=&query_content=&bigbizcircle_switch=1&business_type=2",
    "区域":"https://shangye.ke.com/api/c/house/list?platform=1&device=1&page=0&city_id=440300&size=20&big_bizcircle_id=&district_id={}&subway_id=&resblock_id=&query_content=&bigbizcircle_switch=1&business_type=2",
    "地铁":"https://shangye.ke.com/api/c/house/list?platform=1&device=1&page=0&city_id=440300&size=20&big_bizcircle_id=&district_id=&subway_id={}&resblock_id=&query_content=&bigbizcircle_switch=1&business_type=2"
}


# 发送请求获取数据
def getUrlData(url,headers):
    reqs_url=requests.get(url=url,headers=headers)
    # 判断是否是200
    if reqs_url.status_code==requests.codes.ok:
        reqs_data=reqs_url.content
        # 封装
        result_data={"success":True,"data":reqs_data}
        return result_data
        pass
    else:
        # 不是200
        result_data={"success":False,"data":""}
        return result_data
        pass
    pass

# 读取json数据并打印输出
def User_Option():
    file_json=open("文件/lable_json.json","r",encoding="utf-8")
    json_dict=json.load(file_json)
    file_json.close()
    # 通过jsonpath解析
    code_name="$.data.options[*].label"
    lable_list=jsonpath.jsonpath(json_dict,code_name)
    # 循环遍历
    for i in range(1,len(lable_list)+1):
        print("[{}]".format(i),lable_list[i-1])
        pass
    userInput=int(input("请您选择使用第一层筛选条件："))
    print("-----------------------展示[{}]的选择------------------".format(lable_list[userInput-1]))
    # 第二层
    if userInput==1:
        # 热门商圈
        big_name_list=jsonpath.jsonpath(json_dict,"$.data.options[{}].options[*].big_bizcircle_name".format(userInput-1))
        # 循环遍历
        for i in range(0,len(big_name_list)):
            print("[{}]".format(i),big_name_list[i])
            pass
        pass
    else:
        big_name_list=jsonpath.jsonpath(json_dict,"$.data.options[{}].options[*].name".format(userInput-1))
        # 循环遍历
        for i in range(0,len(big_name_list)):
            print("[{}]".format(i),big_name_list[i])
            pass
        pass
    print("----------------请选择要查询的[{}]-----------------".format(lable_list[userInput-1]))
    code_input=int(input(""))
    print("您选择了:[{}]".format(big_name_list[code_input]))
    # 爬取数据
    # 获取url地址
    # 找到匹配的地址
    url_01=url_dic[lable_list[userInput-1]]
    url_02=""
    if userInput==1:
        # 热门商圈
        # 根据district_id=23008679&bizcircle_id%5B0%5D=611100855获取url地址
        name_bool="$.data.options[{}].options[1:].big_bizcircle_name".format(userInput-1)
        district_id_bool="$.data.options[{}].options[1:].district_id".format(userInput-1)
        big_bizcircle_id_bool="$.data.options[{}].options[1:].big_bizcircle_id".format(userInput-1)
        district_id_list=jsonpath.jsonpath(json_dict,district_id_bool)
        big_bizcircle_id_list=jsonpath.jsonpath(json_dict,big_bizcircle_id_bool)
        name_bool_list=jsonpath.jsonpath(json_dict,name_bool)
        # 判断你要查询的id编号是多少
        index_point=name_bool_list.index(big_name_list[code_input])
        # 拼接url地址
        url_02=str(url_01).format(district_id_list[index_point],big_bizcircle_id_list[index_point])
    else:
        name_bool="$.data.options[{}].options[1:].name".format(userInput-1)
        id_bool="$.data.options[{}].options[1:].id".format(userInput-1)
        name_bool_list=jsonpath.jsonpath(json_dict,name_bool)
        id_bool_list=jsonpath.jsonpath(json_dict,id_bool)
        # # 判断你要查询的id编号是多少
        index_point=name_bool_list.index(big_name_list[code_input])
        # # 拼接url地址
        url_02=str(url_01).format(id_bool_list[index_point])
    return url_02
    pass

def Get_Page_Number(url):
    print("-------------正在帮您查询中--------------------")
    # 进行网路访问
    result_data=getUrlData(url=url,headers=headers)
    if result_data["success"]:
        data=result_data["data"].decode("utf-8")
        json_dict=json.loads(data)
        # 获取数据
        total_value=jsonpath.jsonpath(json_dict,"$.data.total")[0]
        print("总共的房源数据为：",total_value)
        page_num=math.ceil(total_value/20)
        print("理想情况下：{}页".format(page_num))
        if page_num>49:
            # 如果页数大于49，只能查询50页到0页的开始
            return 49
            pass
        return page_num
    pass

# 解析详情页数据
def JsonPath_Home(data):
    # 获取总价格
    home_info=jsonpath.jsonpath(data,"$.data.data.house_info")[0]
    # title
    title=home_info.get("title")
    print(title)
    rent_price=str(round(home_info.get("rent_price")/10000,2))+"万元/月"
    print("月租金：",rent_price)
    # 每平方米的价格
    rent_price_unit_value=str(home_info.get("rent_price_unit_value"))
    rent_price_unit_desc=home_info.get("rent_price_unit_desc")
    unit_dec=rent_price_unit_value+rent_price_unit_desc
    print("每平方米价格：",unit_dec)
    # 所在区域
    district_name=home_info.get("district_name")
    print("所在区域：",district_name)
    # 所在地区
    bizcircle_name=home_info.get("bizcircle_name")
    print("所在地区：",bizcircle_name)
    sql="insert into beke(title,rentPrice,unitDesc,districtName,bizcircleName)values('"+title+"','"+rent_price+"','"+unit_dec+"','"+district_name+"','"+bizcircle_name+"')"
    my_db.commit_data(sql)
    pass

# 解析每一页的内容
def JSONpath_page(data):
    docs_list=jsonpath.jsonpath(data,"$.data.docs[*]")
    for i in range(0,len(docs_list)):
        item_dic=docs_list[i]
        # 标题
        title=item_dic["title"]
        #面积
        area=str(item_dic["area_max"])+"㎡"
        # 详情数据
        house_code=item_dic["house_code"]
        n_home_url=home_data_url.format(house_code)
        print(n_home_url)
        # 通过爬取请求
        result_data=getUrlData(url=n_home_url,headers=headers)
        if result_data["success"]:
            data=result_data["data"].decode("utf-8")
            json_data=json.loads(data)
            # 开始解析详情页数据
            ar_list=JsonPath_Home(data=json_data)
            pass

# 程序入口
if __name__ == '__main__':
    # 将数据存储到json文件中
    json_save="文件/lable_json.json"
    if not os.path.exists(json_save):  # 如果文件或者文件夹不存在
        os.mkdir("文件")
        result_data=getUrlData(url=other_url,headers=headers)
        if result_data["success"]:
            # 存储
            data=result_data["data"].decode("utf-8")
            # 存储到json文件
            file_json=open(json_save,"w",encoding="utf-8")
            file_json.write(data)
            file_json.close()
            pass
        pass
    url_02=User_Option()
    # 获取选择的区域，根据url地址进行解析
    page_num=Get_Page_Number(url_02)
    for i in range(0,2):
        print("-----------正在爬取【第{}页】数据----------------".format(i+1))
        page_url=url_02.replace("page=0","page={}".format(i))
        # 访问网络爬取数据
        result_data=getUrlData(url=page_url,headers=headers)
        if result_data["success"]:
            data=result_data["data"].decode("utf-8")
            json_data=json.loads(data)
            # 开始解析当前页的数据
            JSONpath_page(data=json_data)
            pass
        else:
            continue
            pass
        pass
    pass


