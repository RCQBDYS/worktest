import requests
import urllib3
import json
import pandas as pd


def function():
    url = "https://fmall.gree.com/mobile/shop/recommendLists"
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI '
                            'MiniProgramEnv/Windows WindowsWechat',
              'content-type': 'application/json'}
    data = '{"distributorShopId": "2000002215", "recommendFlag": 11987, "page": 2}'
    urllib3.disable_warnings()
    r = requests.post(url=url, data=data, headers=header, verify=False)
    content = json.loads(r.text)
    result = content['result']
    rows = result['rows']

    excel_content = list()
    for i in rows:
        row = list()
        row.append(i['itemName'])
        row.append(i['itemPrice'])
        row.append(i['skuPrice'])
        excel_content.append(row)

    print(excel_content)
    write_excel(excel_content)


def write_excel(content):
    columns = ['itemName', 'itemPrice', 'skuPrice']
    write_sheet = pd.DataFrame(content, columns=columns)
    write_sheet.to_excel('current.xlsx', index=0)
    print("已生成文件")


if __name__ == '__main__':
    function()
