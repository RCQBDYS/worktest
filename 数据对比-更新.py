import pandas as pd
import xlrd


def read_excel(file_path):
    work_book = xlrd.open_workbook(filename=file_path)
    # 获取第一个索引里面的内容
    sheet1_content = work_book.sheet_by_index(0)
    # 根据文件col读取数据
    num = sheet1_content.nrows
    print('num' + str(num))
    result = []
    for i in range(1, num):
        col = sheet1_content.row_values(i)
        # print(col)
        result.append(col)
    return result


def write_excel(content):
    columns = ['原始条码', '条码', '是否匹配', '原始密码', '密码', '是否匹配']
    write_sheet = pd.DataFrame(content, columns=columns)
    write_sheet.to_excel('G:\\培训文件\\数据对比\\result5.xlsx', index=0)
    print("已生成对比结果文件")


def find_bar(source_path, current_path):
    source_list = read_excel(source_path)
    current_list = read_excel(current_path)
    result = list()
    for i in range(len(current_list)):
        current_bar = current_list[i][0]
        current_password = current_list[i][1]
        for j in range(len(source_list)):
            source_bar = source_list[j][0]
            # print(current_bar + " " + source_bar)
            if current_bar == source_bar:
                # 找到了original中的条码
                source_temp = source_bar
                # 对比其他数据
                source_password = source_list[j][1]
                if current_password == source_password:
                    password_status = '匹配'
                else:
                    password_status = '不匹配'
                # flag 1为存在，0为不存在
                flag = 1
                break
            else:
                source_temp = source_bar
                flag = 0
        # print(str(flag) + str(source_temp))
        if flag == 1:
            # print(current_bar + " " + source_bar)
            temp = list()
            # current条码以及original中的条码
            temp.append(current_bar)
            temp.append(source_temp)
            temp.append('存在且匹配')
            temp.append(current_password)
            temp.append(source_password)
            temp.append(password_status)
            result.append(temp)
        elif flag == 0:
            # print(current_bar + " " + source_bar)
            temp = list()
            temp.append(current_bar)
            temp.append('')
            temp.append('不存在')
            result.append(temp)
    write_excel(result)


if __name__ == '__main__':
    source = r'G:\培训文件\数据对比\original.xlsx'
    current = r'G:\培训文件\数据对比\current.xlsx'
    find_bar(source, current)