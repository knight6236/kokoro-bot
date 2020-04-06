from mirai import Mirai, Member
from plugins.guild.guild import *

task_data: dict = {}


def write_task(groupId):
    write_json('data/task/' + str(groupId) + '.json', task_data)


def read_task(groupId):
    global task_data
    try:
        return read_json('data/task/' + str(groupId) + '.json')
    except FileNotFoundError:
        return task_data


# 导入作业 1-1 狼克剑圣猫拳春妈 900
async def import_task(app: Mirai, member: Member, args: str):
    global task_data
    # task_str_list = args.split(' ', maxsplit=2)
    # record = {'member_id': member.id, 'member_name': member.memberName, 'team': task_str_list[1],
    #           'score': int(task_str_list[2])}
    task = deal_task(args)
    if task is None:
        return await reply_group(app, member.group.id, ILLEGAL_ERR, [member.id])
    record = {'member_id': member.id, 'member_name': member.memberName, 'team': task['team'],
              'score': int(task['score'])}
    record_list: list = []
    task_data = read_task(member.group.id)
    if task['task_mark'] in task_data.keys():
        record_list = task_data[task['task_mark']]
    record_list.append(record)
    # print(record_list)
    task_data[task['task_mark']] = record_list
    write_task(member.group.id)
    msg = '导入作业成功'
    await reply_group(app, member.group.id, msg)


async def query_task(app: Mirai, member: Member, task_mark: str = ''):
    global task_data
    task_data = read_task(member.group.id)
    count = 0
    msg: str
    if task_mark == '':
        msg = '查询到的作业列表（越靠后的越新）：\n'
    else:
        if not check_task_mark(task_mark):
            return await reply_group(app, member.group.id, ILLEGAL_ERR, [member.id])
        msg = task_mark + '的作业列表（越靠后的越新）：\n'
    for key in task_data.keys():
        if key != task_mark and task_mark != '':
            continue
        task_list = task_data[key]
        for task in task_list:
            count += 1
            k_name = strQ2B(task['member_name']).split('(', maxsplit=1)[0]
            if task_mark == '':
                msg += key + ' '
            msg += task['team'] + ' ' + str(task['score']) + ' --by ' + k_name + '\n'
    if count > 0:
        await reply_group(app, member.group.id, msg)
    else:
        await reply_group(app, member.group.id, '未查询到' + task_mark + '作业，请先导入吧！')


async def query_current_task(app: Mirai, member: Member):
    guild = read_guild(member.group.id)
    current_key = str(guild['current_stage']) + '-' + str(guild['current_boss'])
    await query_task(app, member, current_key)


async def reset_task(app: Mirai, member: Member, task_mark: str = ''):
    global task_data
    task_data = read_task(member.group.id)
    count = 0
    msg: str
    if task_mark == '':
        task_data = {}
        write_task(member.group.id)
        return await reply_group(app, member.group.id, '重置全部作业成功')
    else:
        if not check_task_mark(task_mark):
            return await reply_group(app, member.group.id, ILLEGAL_ERR, [member.id])
    if task_mark in task_data.keys():
        del task_data[task_mark]
        count += 1
    write_task(member.group.id)
    if count > 0:
        await reply_group(app, member.group.id, task_mark + '作业重置成功')
    else:
        await reply_group(app, member.group.id, '未查询到' + task_mark + '作业，请先导入吧！')
