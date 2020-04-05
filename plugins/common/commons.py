import re, json, datetime, random
from urllib import request

from idna import unichr
from mirai import Plain, At, AtAll

pattern = re.compile('[0-9]')


# 检查伤害数据合法性
def check_dmg(arg):
    print_msg(check_dmg=arg)
    if pattern.match(arg):
        return True
    else:
        return False


# 读取json文件
def read_json(file_path):
    with open(file_path, encoding='utf-8') as f:
        return json.load(f)


# 写入json文件
def write_json(file_path, json_data):
    with open(file_path, 'w', encoding='utf-8') as fw:
        json.dump(json_data, fw, ensure_ascii=False, indent=4)


async def reply_group(app, group, msg, atList=[], atAll=False):
    message = []
    if atAll:
        message.append(AtAll())
    else:
        for at in atList:
            message.append(At(target=at))
    message.append(Plain(msg))
    print_msg(message=message)
    await app.sendGroupMessage(group, message)


def print_msg(tag='Info', **kwargs):
    nowTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print('[' + nowTime + '][Bot] ' + tag + ':', kwargs)


def uniqueNumStr():
    """生成唯一字符串"""
    nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
    randomNum = random.randint(1, 100);  # 生成的随机整数n，其中0<=n<=100
    randomNumStr = ''
    if randomNum < 10:
        randomNumStr = '00' + str(randomNum);
    elif randomNum < 100:
        randomNumStr = '0' + str(randomNum);
    uniqueNum = str(nowTime) + randomNumStr;
    return uniqueNum


def downloadImg(url, fileName):
    download(url, 'data/resources/images/' + fileName + '.gif')


def download(url, path):
    request.urlretrieve(url, path)


# -*- coding: cp936 -*-
def strQ2B(ustring):
    """全角转半角"""
    rstrings = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 12288:  # 全角空格直接转换
            inside_code = 32
        elif inside_code >= 65281 and inside_code <= 65374:  # 全角字符（除空格）根据关系转化
            inside_code -= 65248

        rstrings += unichr(inside_code)
    return rstrings


def strB2Q(ustring):
    """半角转全角"""
    rstrings = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 32:  # 半角空格直接转化
            inside_code = 12288
        elif 32 <= inside_code <= 126:  # 半角字符（除空格）根据关系转化
            inside_code += 65248

        rstrings += unichr(inside_code)
    return rstrings


def deal_task(s: str):
    """处理任务内容"""
    s = s.replace('/', '-')
    s = s.replace('月', '-')
    s = s.replace('日', ' ')
    s = s.replace('号', ' ')
    s = s.replace('时', ':')
    s = s.replace('点', ':')
    s = s.replace('分', '')
    # m = re.search(r"(\d{4}[-/]\d{1,2}[-/]\d{1,2}\s\d{1,2}:\d{0,2})", s)
    try:
        m = re.search('(?P<time>\d{1,2}[-]{0,1}\d{1,2}\s\d{1,2}:{,1}\d{0,2})(?P<task>.*)', s)
        content = m.groupdict()
        content['time'] = '2020-' + content['time'] + ":00"
        print(content)  # 在起始位置匹配
        return content
    except AttributeError:
        return None
