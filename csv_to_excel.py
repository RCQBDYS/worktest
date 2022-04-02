import csv
import pandas as pd


def read_csv(file_path):
    csv_reader = csv.reader(open(file_path, encoding='utf-8'))
    # print(csv_reader)
    return csv_reader


def write_excel(content):
    columns = ['国家', '邮政编码', '邮编']
    write_sheet = pd.DataFrame(content, columns= columns)
    write_sheet.to_excel('G:\\培训文件\\数据对比\\数据对比-1-1.xlsx', index=0)
    print("complete！")


def csv_to_excel(path):
    temp = list()
    for i in read_csv(path):
        temp.append(i)
        print(i)
    write_excel(temp)


if __name__ == '__main__':
    original = r'G:\培训文件\数据对比\数据对比.csv'
    csv_to_excel(original)
