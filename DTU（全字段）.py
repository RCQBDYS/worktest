# coding:utf-8
import re
import pandas as pd
import datetime
import requests
from bs4 import BeautifulSoup
import time

dtu02 = []  # 存放状态为02的数据
dtu03 = []  # 存放状态为03的数据


# 数据保存到excel
def split_file(file_name):
    f = open(file_name, encoding='utf-8')
    lines = f.readlines()  # 读取所有行
    num = 0  # 总数据量
    num02 = 0  # 状态02总计数
    num03 = 0  # 状态03数据计数

    # 循环读取每一行进行处理
    for line in lines:
        timeCode = re.search(r'(\d{4}\-\d{2}\-\d{1,2} \d{2}:\d{2}:\d{2}.\d{3}).*客户端发来数据.*>(['
                             r'a-zA-Z0-9]*4C3947434246364335444343314D333033[a-zA-Z0-9]*)', line)
        if timeCode:
            # 上报时间
            reportTime = timeCode.group(1)
            # 编码
            code = timeCode.group(2)
            # 数据采集时间 16进制
            collTime = code[48:60]
            # 格式化为10进制时间
            formatTime = dateTimeFormat(collTime)
            # 命令标识
            comId = code[4:6]
            # 应答标识
            resId = code[6:8]
            # 数据单元加密方式
            encryption = code[42:44]
            # 数据单元长度
            length = str(int(code[44:48], 16) * 2) + "字节"
            # 车辆位置数据
            location = code[60:62]
            # 定位状态
            positionStatus = code[62:64]
            # Lng
            lng = int(code[64:72], 16) / 1000000
            # Lat
            lat = int(code[72:80], 16) / 1000000
            # 整车数据
            data = code[80:82]
            # 车辆状态
            vehicleStatus = code[82:84]
            # 充电状态
            chargeStatus = code[84:86]
            # 运行模式
            operMode = code[86:88]
            # 车速
            speed = int(code[88:92], 16) / 10
            # 累计里程
            mileage = int(code[92:100], 16) / 10
            # 总电压解析数据
            analVoltage = int(code[100:104], 16) / 10
            # 总电流解析数据
            analElectri = (int(code[104:108], 16) / 10) - 1000
            # 电量
            soc = int(code[108:110], 16)
            # DC-DC状态
            dcStatus = code[110:112]
            # 档位
            gear = bin(int(code[112:114], 16))[2:]
            # 绝缘电阻
            resistance = int(code[114:118], 16)
            # 驱动电机数据
            motorData = code[122:124]
            # 驱动电机数
            motorData2 = code[124:126]
            # 驱动电机顺序号
            motorId = code[126:128]
            # 驱动电机状态
            motorStatus = code[128:130]
            # 驱动电机控制器温度
            cTemperature = int(code[130:132], 16) - 40
            # 电机转速
            analSpeed = int(code[132:136], 16) - 20000
            # 电机转矩
            analMotor = (int(code[136:140], 16) - 20000) / 10
            # 电机温度
            mTemperature = int(code[140:142], 16) - 40
            # 电机控制器输入电压解析后数据
            analVo = int(code[142:146], 16) / 10
            # 电机控制器直流母线电流解析后数据
            analIi = (int(code[146:150], 16) / 10) - 1000
            # 极值
            extremum = code[200:202]
            # 最高电压电池子系统号
            number = code[202:204]
            # 最高电压电池单体代号
            cellCode = code[204:206]
            # 电池单体电压最高值
            maxVoltage = int(code[206:210], 16) / 1000
            # 最低电压电池子系统号
            number2 = code[210:212]
            # 最低电压电池单体代号
            minVoltage = code[212:214]
            # 电池单体电压最低值
            minCell = int(code[214:218], 16) / 1000
            # 最高温度子系统号
            maxTemperature = code[218:220]
            # 最高温度探针序号
            maxTemperature2 = code[220:222]
            # 最高温度值
            maxTemperature3 = int(code[222:224], 16) - 40
            # 最低温度子系统号
            minTemperature = code[224:226]
            # 最低温度探针序号
            minTemperature2 = code[226:228]
            # 最低温度值
            minTemperature3 = int(code[228:230], 16) - 40
            # 报警数据
            alarmData = code[336:338]
            # 最高报警等级
            maxAlarm = code[338:340]
            # 通用报警标志
            alarmFlag = bin(int(code[340:348], 16))[2:]
            num = num + 1

            global tc
            tc = 0
            # 判断状态码
            if code[4:6] == '02':
                if len(dtu02) > 0:
                    # 计算时间间隔
                    tc = timecell(dtu02[len(dtu02) - 1][1], reportTime)
                temp02 = [formatTime, reportTime, tc, comId, resId, encryption, length, location, positionStatus, lng,
                          lat, data, vehicleStatus, chargeStatus,
                          operMode, speed, mileage, analVoltage, analElectri, soc, dcStatus, gear, resistance,
                          motorData, motorData2, motorId,
                          motorStatus, cTemperature, analSpeed, analMotor, mTemperature, analVo, analIi, extremum,
                          number, cellCode, maxVoltage, number2, minVoltage,
                          minCell, maxTemperature, maxTemperature2, maxTemperature3, minTemperature, minTemperature2,
                          minTemperature3, alarmData, maxAlarm, alarmFlag]
                dtu02.append(temp02)
                num02 += 1
            elif code[4:6] == '03':
                if len(dtu03) > 0:
                    tc = timecell(dtu03[len(dtu03) - 1][1], reportTime)
                temp03 = [formatTime, reportTime, tc, comId, resId, encryption, length, location, positionStatus, lng,
                          lat, data, vehicleStatus, chargeStatus,
                          operMode, speed, mileage, analVoltage, analElectri, soc, dcStatus, gear, resistance,
                          motorData, motorData2, motorId,
                          motorStatus, cTemperature, analSpeed, analMotor, mTemperature, analVo, analIi, extremum,
                          number, cellCode, maxVoltage, number2, minVoltage,
                          minCell, maxTemperature, maxTemperature2, maxTemperature3, minTemperature, minTemperature2,
                          minTemperature3, alarmData, maxAlarm, alarmFlag]
                dtu03.append(temp03)
                num03 += 1

    print('总条数：%d' % num)
    print('02有效数据条数：%d' % num02)
    print('03无效数据条数：%d' % num03)
    # 02的数据保存到excel
    df = pd.DataFrame(dtu02,
                      columns=['数据采集时间', '上报时间', '时间差(S)', '命令标识', '应答标识', '数据单元加密方式', '数据单元长度', '车辆位置数据', '定位状态',
                               'Lng', 'Lat', '整车数据', '车辆状态', '充电状态', '运行模式', '车速', '累计里程', '总电压', '总电流', 'SOC(电量)',
                               'DC-DC状态', '档位',
                               '绝缘电阻', '驱动电机数据', '驱动电机数', '驱动电机顺序号', '驱动电机状态', '驱动电机控制器温度', '电机转速', '电机转矩', '电机温度',
                               '电机控制器输入电压', '电机控制器直流母线电流', '极值', '最高电压电池子系统号', '最高电压电池单体代号', '电池单体电压最高值', '最低电压电池子系统号',
                               '最低电压电池单体代号', '电池单体电压最低值', '最高温度子系统号', '最高温度探针序号', '最高温度值', '最低温度子系统号', '最低温度探针序号',
                               '最低温度值', '报警数据',
                               '最高报警等级', '通用报警标志'])
    df.to_excel("G:\\log_info_02.xlsx", index=False)
    print('生成log_info_02.xlsx')
    # 03的数据保存到excel
    df = pd.DataFrame(dtu03,
                      columns=['数据采集时间', '上报时间', '时间差(S)', '命令标识', '应答标识', '数据单元加密方式', '数据单元长度', '车辆位置数据', '定位状态',
                               'Lng', 'Lat', '整车数据', '车辆状态', '充电状态', '运行模式', '车速', '累计里程', '总电压', '总电流', 'SOC(电量)',
                               'DC-DC状态', '档位',
                               '绝缘电阻', '驱动电机数据', '驱动电机数', '驱动电机顺序号', '驱动电机状态', '驱动电机控制器温度', '电机转速', '电机转矩', '电机温度',
                               '电机控制器输入电压', '电机控制器直流母线电流', '极值', '最高电压电池子系统号', '最高电压电池单体代号', '电池单体电压最高值', '最低电压电池子系统号',
                               '最低电压电池单体代号', '电池单体电压最低值', '最高温度子系统号', '最高温度探针序号', '最高温度值', '最低温度子系统号', '最低温度探针序号',
                               '最低温度值', '报警数据',
                               '最高报警等级', '通用报警标志'])
    df.to_excel("G:\\log_info_03.xlsx", index=False)
    f.close()
    print('生成log_info_03.xlsx')



# 计算时间差，第二个数据减去第一个，第三个数据减去第二个
def timecell(time1, time2):
    startTime = datetime.datetime.strptime(time1, "%Y-%m-%d %H:%M:%S.%f")
    endTime = datetime.datetime.strptime(time2, "%Y-%m-%d %H:%M:%S.%f")
    seconds = (endTime - startTime).total_seconds()
    return seconds


# 十六进制时间转换为十进制，进行拼接
def dateTimeFormat(collTime):
    year = str(int(collTime[0:2], 16))
    month = str(int(collTime[2:4], 16))
    day = str(int(collTime[4:6], 16))
    hour = str(int(collTime[6:8], 16)).zfill(2)
    min = str(int(collTime[8:10], 16)).zfill(2)
    sec = str(int(collTime[10:], 16)).zfill(2)
    return year + "年" + month + "月" + day + "日" + hour + ":" + min + ":" + sec


def log_text():
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}
    link = 'http://112.91.147.106:8085/'
    read = requests.get(link, headers=header, timeout=20)
    soup = BeautifulSoup(read.text, 'lxml')
    div_content = soup.find_all(id='contentx')
    for item in div_content:
        content = item.get_text()
        file = open('G:\\logResult.txt', 'w', encoding='utf-8')  # 覆盖添加
        file.write(content)
        file.close()
    print('内容抓取完毕')
    # i = 0
    # while True:
    #     link = 'http://112.91.147.106:8085/'
    #     read = requests.get(link, headers=header, timeout=10)
    #     soup = BeautifulSoup(read.text, 'lxml')
    #     div_content = soup.find_all(id='contentx')
    #     for item in div_content:
    #         content = item.get_text()
    #         file = open('G:\\logResult.txt', 'w', encoding='utf-8')  # 覆盖添加
    #         file.write(content)
    #         file.close()
    #         i += 1
    #         print('第' + str(i) + '次加载数据')
    #     time.sleep(10)


if __name__ == '__main__':
    log_text()
    split_file('G:\\logResult.txt')
