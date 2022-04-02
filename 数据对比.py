import csv
import xlrd
import pandas as pd
import re


def document_contrast(original_path, current_path):
    # 读取原文件original
    document_original = read_excel(original_path)
    # 读取现在文件current
    document_current = read_excel(current_path)
    result = []
    # len(list)获取列表长度
    for i in range(len(document_current)):
        # 获取源文件条形码和密码
        bar_code = document_original[i][0]
        original_password = document_original[i][1]
        # 获取现有文件密码
        current_code = document_current[i][0]
        current_password = document_current[i][1]
        # 获取密码时间
        # crate_time = document_original[i][2]
        # lower()将大写字母转换成小写函数
        if bar_code.lower() == current_code.lower():
            password_status = '条码匹配'
        else:
            password_status = '条码不匹配'

        if original_password == current_password:
            status = "匹配"
        else:
            status = "不匹配"
        temp = list()
        # 原始条码['1000000000000']
        temp.append(bar_code)
        # 现文件条码['1000000000000','1000000000000']
        temp.append(current_code)
        # 条码是否匹配['1000000000000','1000000000000','条码匹配']
        temp.append(password_status)
        # 添加时间
        # temp.append(crate_time)

        # 原始密码['1000000000000','1000000000000','条码匹配','678945']
        temp.append(original_password)
        # 解密密码['1000000000000','1000000000000','条码匹配','678945','678945']
        temp.append(current_password)
        # 密码是否匹配['1000000000000','1000000000000','条码匹配','678945','678945','匹配']
        temp.append(status)
        # print(temp)[['1000000000000','1000000000000','条码匹配','678945','678945','匹配']]
        result.append(temp)

    # write_csv(result)
    write_excel(result)


def string_findall(pattern, line):
    temp = re.compile(pattern)
    result = temp.findall(line)
    return result


def read_excel(file_path):
    print(file_path)
    work_book = xlrd.open_workbook(filename=file_path)
    # 获取第一个索引里面的内容
    sheet1_content = work_book.sheet_by_index(0)
    # 根据文件行数读取数据
    num = sheet1_content.nrows
    print('num =' + str(num))
    result = []
    # range(1,num)'1'跳过表头进行内容的读取
    for i in range(1, num):
        row = sheet1_content.row_values(i)
        result.append(row)
    # result中最终形成的数据样式：[['威克岛', 'UA', '301469'],['保加利亚', 'SA', '524901']]
    return result


def read_csv(file_path):
    csv_reader = csv.reader(open(file_path))
    return csv_reader


def write_csv(content):
    # print(content)
    # 创建文件
    csv_file = open('contrastResult.csv', 'w', newline='\n')
    write_active = csv.writer(csv_file)
    # 写入col_name
    write_active.writerow(["旧条形码", "掌上通条形码", "条码是否匹配", "时间", "源密码", "掌上通密码", "对比结果"])
    write_active.writerows(content)
    csv_file.close()
    print("已生成对比结果文件")


def write_excel(content):
    columns = ['条形码', '掌上通条形码', '条码是否匹配', '源密码', '掌上通密码', '对比结果']
    write_sheet = pd.DataFrame(content, columns=columns)
    write_sheet.to_excel('G:\\培训文件\\数据对比\\result.xlsx', index=0)
    print("已生成对比结果文件")


if __name__ == '__main__':
    original = r'G:\培训文件\数据对比\original.xlsx'
    current = r'G:\培训文件\数据对比\current.xlsx'
    document_contrast(original, current)
