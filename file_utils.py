import pandas as pd
import os
import re


#txt文件的读取
def read_txt(path):
    with open(path, encoding='utf-8') as f:
        line = f.readlines()
    print('已读取{}文件'.format(path))
    return line


# txt文件的写入
def write_txt(content, save_path, save_name):
    with open('{}/{}.txt'.format(save_path, save_name), 'w+') as f:
        for item in content:
            temp = ''
            for i in range(len(item)):
                temp += item[i] + ' '
            temp += '\n'
            f.write(temp)
    print('已在{}生成{}.txt文件'.format(save_path, save_name))


# excel文件的读取
def read_excel(path):
    excel_read = pd.read_excel(path, dtype=str, header=None)
    excel_content = excel_read.values
    print('已读取{}文件'.format(path))
    return excel_content


# excel文件的写入
def write_excel(content, column, save_path, save_name):
    write_excel = pd.DataFrame(data=content, columns=column, dtype=str)
    write_excel.to_excel('{}/{}.xlsx'.format(save_path, save_name), index=0)
    print('已在{}生成{}.txt文件'.format(save_path, save_name))


# 正则表达式匹配字符串
def string_match(content):
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

    # 0A,1数据处理
    result_content = list()
    for item in A1_list:
        temp = list()
        A1_time = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*(originals:>0A,1.*)', item)
        # A1_content = re.search(r'(originals:>0A,1.*)', item).group()
        sample = re.search(r'^', item)
        print(sample.group())
        A1_device_time = re.search(r'\d{4}/\d{2}/\d{2} (\d{2}:\d{2}:\d{2}).*(.,.)', item)
        # result_content.append(temp)

    return result_content


if __name__ == '__main__':
    # text_to_excel()
    file_path = r'G:\工作文件\线装式在途定位器\数据\原始数据.txt'
    # 保存处理之后的A1数据
    file_dir_path = os.path.dirname(file_path)
    txt_content = read_txt(file_path)
    A1_content = string_match(txt_content)
    # write_txt(A1_content, file_dir_path, 'A1数据')
