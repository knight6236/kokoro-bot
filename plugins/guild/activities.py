from pprint import pprint

from plugins.common.commons import *
from mirai import Mirai, Member

activities = {}


async def init_active(app: Mirai):
    global activities
    try:
        activities = read_json('data/active/active.json')
    except OSError:
        print_msg(tag='Error', err='未读取到文件，初始化所有群组活跃度数据')
        activities = await init_all_group_active(app)
    # finally:
    #     pprint(activities)


async def init_all_group_active(app: Mirai, manage_groups):
    # groups = await app.groupList()
    g_json = {}
    for group in manage_groups:
        g_json[str(group)] = await init_single_group_active(app, group)
    write_json('data/active/active.json', g_json)
    return g_json


async def init_single_group_active(app: Mirai, group_id):
    members = await app.memberList(group_id)
    m_json = {}
    for member in members:
        m_json[str(member.id)] = {'name': member.memberName, 'points': 0}
    # pprint(m_json)
    return m_json


async def calculate_points(app: Mirai, member: Member):
    # print('calculate_points', member)
    global activities
    group_data: dict
    g_id = str(member.group.id)
    if g_id in activities:
        group_data = activities[g_id]
    else:
        group_data = await init_single_group_active(app, member.group.id)
        activities[g_id] = group_data

    member_date: dict
    m_id = str(member.id)
    if m_id in group_data:
        member_date = group_data[m_id]
    else:
        member_date = {'name': member.memberName, 'points': 0}
        group_data[m_id] = member_date
    member_date['points'] += 1
    # pprint(activities)
    write_json('data/active/active.json', activities)


async def query_points(app: Mirai, member: Member):
    global activities
    group_data: dict
    g_id = str(member.group.id)
    if g_id in activities:
        group_data = activities[g_id]
    else:
        group_data = await init_single_group_active(app, member.group.id)

    member_date: dict
    m_id = str(member.id)
    if m_id in group_data:
        member_date = group_data[m_id]
    else:
        member_date = {'name': member.memberName, 'points': 0}
    # g = activities[str(member.group.id)]
    # m = g[str(member.id)]
    p: dict
    for g_k in group_data.keys():
        p[g_k] = group_data[g_k]['points']
    # pprint(p)
    rank_list = sorted(p.items(), key=lambda x: x[1], reverse=True)
    rank = 0
    for index, value in enumerate(rank_list):
        # print(index, value)
        if value[0] == str(member.id):
            rank = index + 1
            break
    return await reply_group(app, member.group.id, '你当前的活跃度为:' + str(member_date['points']) + ', 排名为:' + str(rank),
                             [member.id])
