import xlrd


def function():
    workbook = xlrd.open_workbook(r'G:\工作簿1.xlsx')
    print(workbook.sheet_names())


if __name__ == '__main__':
    function()