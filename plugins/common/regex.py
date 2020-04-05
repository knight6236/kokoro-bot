import datetime
import re


def deal_task(s: str):
    s = s.replace('/', '-')
    s = s.replace('月', '-')
    s = s.replace('日', ' ')
    s = s.replace('号', ' ')
    s = s.replace('时', ':')
    s = s.replace('点', ':')
    s = s.replace('分', '')
    # m = re.search(r"(\d{4}[-/]\d{1,2}[-/]\d{1,2}\s\d{1,2}:\d{0,2})", s)
    m = re.search('(?P<time>\d{1,2}[-]\d{1,2}\s\d{1,2}:\d{0,2})(?P<task>.*)', s)
    content = m.groupdict()
    content['time'] = str(datetime.datetime.year) + '-' + content['time'] + ":00"
    print(content)  # 在起始位置匹配
    return content
    # t = datetime.datetime.strptime('2020-' + content['time'], "%Y-%m-%d %H:%M")
    # print(t)


s = "预约任务:03-22 10:00和优衣逛街,吃饭"
s = "预约任务:03月22 10:00和优衣逛街,吃饭"
s = "预约任务:3月22号10:00和优衣逛街,吃饭"
s = "预约任务:3月22号10点和优衣逛街,吃饭,2"

print(deal_task(s))
