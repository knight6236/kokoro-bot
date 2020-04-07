import datetime
import json
import os
import random
import re
from urllib import request
from idna import unichr
from mirai import Plain, At, AtAll


def init_path():
    create_path('data/battle/')
    create_path('data/guild/')
    create_path('data/task/')
    print_msg(msg='初始化路径成功')


# 路径不存在则创建
def create_path(file_path):
    dir_path = os.path.dirname(file_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


# 读取json文件
def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as fw:
        return json.load(fw)


# 写入json文件
def write_json(file_path, json_data):
    # create_path(file_path)
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


dmg_pattern = re.compile(r'[0-9]{1,4}[*]*$')


# 检查伤害数据合法性
def check_dmg(s: str):
    if dmg_pattern.match(s):
        return True
    else:
        return False


# print(check_dmg('300*'))


# 伤害排序
def sort_dmg(g):
    p = []
    for g_k in g.keys():
        t_name = strQ2B(g[g_k]['name']).split('(', maxsplit=1)[0]
        tail = 0
        if 'tail' in g[g_k].keys():
            tail = g[g_k]['tail']
        t = (g_k, t_name, g[g_k]['hp'], tail)
        p.append(t)
    rank_list = sorted(p, key=lambda x: (x[3], x[2]), reverse=True)
    return rank_list


job_pattern = re.compile(r'^[0-9]{17}$')


# 检查任务id合法性
def check_job(s: str):
    if job_pattern.match(s):
        return True
    else:
        return False


def uniqueNumStr():
    """生成唯一字符串"""
    nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
    randomNum = random.randint(1, 100);  # 生成的随机整数n，其中1<=n<=100
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
        elif 65281 <= inside_code <= 65374:  # 全角字符（除空格）根据关系转化
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


def deal_job(s: str):
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
        m = re.search(r'(?P<time>\d{1,2}[-]\d{1,2}\s\d{1,2}[:]\d{0,2})(?P<task>.*)', s)
        content = m.groupdict()
        content['time'] = '2020-' + content['time'] + ":00"
        print(content)  # 在起始位置匹配
        return content
    except AttributeError:
        print('deal_task err')
        return None


# deal_job('3月25号22点0分和可可萝一起洗澡')


def deal_task(s: str):
    try:
        m = re.search(r'(?P<task_mark>[1-4][-][1-5])\s*(?P<team>[\u4E00-\u9FA50-9a-zA-Z]+)\s(?P<score>[0-9]{1,4})$', s)
        content = m.groupdict()
        print(content)
        return content
    except AttributeError:
        print('check_task err')
        return None


# deal_task('1-5 狼克剑圣猫拳春妈nnk 900')


task_pattern = re.compile(r'[1-4][-][1-5]')


# 检查作业数据合法性
def check_task_mark(s: str):
    if task_pattern.match(s):
        return True
    else:
        return False
