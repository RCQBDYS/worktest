import requests
import json
import pandas as pd


def function():
    url = 'https://gasrecovery.gree.com:9089/getMachineByTime'
    data = {'username': 'test', 'password': 'testio2018!#', 'bucket': 'gree-test-bucket', 'updateTime': '2000-01-01'}
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/88.0.4324.190 Safari/537.36'}
    r = requests.post(url, headers=headers, data=data)
    content = json.loads(r.text)
    data = content['data']
    result = list()
    for i in data:
        temp = list()
        brand = i['Brand']
        machine = i['Machine']
        temp.append(machine)
        temp.append(brand)
        result.append(temp)
    write_excel(result)


def write_excel(content):
    columns = ['machine', 'brand']
    write_sheet = pd.DataFrame(content, columns=columns)
    write_sheet.to_excel('掌上通结果.xlsx', index=0)
    print("已生成文件")


if __name__ == '__main__':
    function()
