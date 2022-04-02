# @Time : 2022/3/8 14:03
# @Author : 672025
# @Version：V 0.1
# @File : dataProcessing.py
# @desc : 对于txt类型，GPS数据提取分类
import pandas as pd
import os
import re


# 数据读取
def read_txt(path):
    file = open(path, encoding='utf-8')
    line_content = file.readlines()
    process_content_list = list()
    process_content_list.append(['@timestamp','message'])
    for item in line_content:
        temp = item.strip()
        line_list = list()
        if len(temp) != 0:
            line_list.append(temp[0:28])
            line_list.append(temp[29:])
            process_content_list.append(line_list)
    for i in process_content_list:
        print(i)
    return process_content_list


# 数据提取
def data_fetch(content_list, barcode):
    OA_list = list()
    OB_list = list()
    for line in content_list:
        # 正式数据
        if barcode in line:
            if 'originals:>0A' in line:
                OA_list.append(line)
            # 心跳数据
            elif 'originals:>0B' in line:
                OB_list.append(line)
    # for i in OA_list:
    #     data_time = re.match(r'^(.*)-(.*)-(.*)/s(.*):(.*):(.*)', i)


if __name__ == '__main__':
    txt_path = 'G:\工作文件\线装式在途定位器\数据\原始数据.txt'
    content = read_txt(txt_path)
    # number = '866545052039366'
    # data_fetch(content, number)
