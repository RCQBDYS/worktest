from importlib.resources import path
from operator import index
from numpy import dtype
import pandas as pd
import os
import re


# def text_to_excel():
#     global columns
#     file = 'C:\\Users\\672025\\Desktop\\数据\\system_dictdetails_202109131445.txt'
#     f = open(file, encoding='utf-8')
#     file_basename = os.path.basename(file)
#     file_name = file_basename.split('.')[0]
#     file_dir_path = os.path.dirname(file)
#     line = f.readlines()
#     result = list()
#     count = 0
#     for item in line:
#         temp = item.replace(" ", "").replace("\n", "").lstrip('|').rstrip('|')
#         if count == 0:
#             columns = temp.split('|')
#         else:
#             result.append(temp.split('|'))
#         count += 1
#     write_sheet = pd.DataFrame(result, columns=columns)
#     write_sheet.to_excel('{}\\{}.xlsx'.format(file_dir_path ,file_name), index=0)
#     print('文件已转换成csv文件')


# txt文件的读取
def read_txt(path):
    with open(path, encoding='utf-8') as f:
        line = f.readlines()
    return line


# excel文件的读取
def read_excel(path):
    excel_read = pd.read_excel(path, dtype=str, header=None)
    excel_content = excel_read.values


# excel文件的写入
def write_excel(content):
    columns = ['id', 'name', 'telephone', 'address']
    write_excel = pd.DataFrame(data=content, columns=columns, dtype=str)
    write_excel.to_excel('smaple.xlsx', index=0)


# 正则表达式匹配字符串
def string_match(path):
    global A1_list
    content = read_txt(path)
    A1_list = list()
    A3_list = list()
    B_list = list()
    for item in content:
        temp = item.replace("\n", "")
        if re.search(r'originals:>0A,1', temp):
            A1_list.append(temp)
        elif re.search(r'originals:>0A,3', temp):
            A3_list.append(temp)
        elif re.search(r'originals:>0B', temp):
            B_list.append(temp)


if __name__ == '__main__':
    # text_to_excel()
    file_path = r'G:\工作文件\线装式在途定位器\数据\原始数据.txt'
    string_match(file_path)
