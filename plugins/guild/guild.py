import time
from pprint import pprint

from plugins.common.constants import *
from plugins.common.commons import *

boss_data = [[]]

guild_data: dict = {'current_stage': 1, 'current_boss': 1, 'current_loop': 1,
                    'tree_members': {}, 'cache_boss': {}, 'current_boss_data': []}


def write_guild(groupId):
    write_json('data/guild/' + str(groupId) + '.json', guild_data)


def read_guild(groupId):
    return read_json('data/guild/' + str(groupId) + '.json')


def init():
    global boss_data
    boss_data = read_json('data/boss_data.json')
    # pprint(boss_data)


init()


def initData(member):
    global guild_data
    print_msg(msg='初始化会战数据')
    try:
        guild_data = read_guild(member.group.id)
        if 'current_stage' not in guild_data.keys():
            guild_data['current_stage'] = 1
        if 'current_boss' not in guild_data.keys():
            guild_data['current_boss'] = 1
        if 'current_loop' not in guild_data.keys():
            guild_data['current_loop'] = 1
        if 'tree_members' not in guild_data.keys():
            guild_data['tree_members'] = {}
        if 'cache_boss' not in guild_data.keys():
            guild_data['cache_boss'] = boss_data[guild_data['current_stage'] - 1][guild_data['current_boss'] - 1].copy()
        if 'current_boss_data' not in guild_data.keys():
            guild_data['current_boss_data'] = boss_data[0]
    except OSError as reason:
        print_msg(tag='Error', err='读文件异常，数据重置')
        guild_data['current_stage'] = 1
        guild_data['current_boss'] = 1
        guild_data['current_loop'] = 1
        guild_data['tree_members'] = {}
        guild_data['cache_boss'] = boss_data[guild_data['current_stage'] - 1][guild_data['current_boss'] - 1].copy()
        guild_data['current_boss_data'] = boss_data[0]
    # finally:
    #     pprint(guild_data)


async def menu(app, member):
    msg = '预约boss: 预约老一/预约1 伤害（纯数字，单位是w，有空格）\n'
    msg += "预约下一轮boss: 预约下轮\n"
    msg += "取消预约: 取消老一/取消1\n"
    msg += "取消下一轮预约: 取消下轮\n"
    # msg += "查询预约: 谁预约了老一/谁约1\n"
    msg += "查询进度/预约/boss当前状态: 老几了/预约情况/预约状态\n"
    # msg += "查询预约/boss当前状态: 预约名单1/状态1/谁预约了老一\n"
    msg += "报刀: 报刀/打了/杀了/恰了（纯数字，单位是w，有空格）\n"
    msg += "设置boss实际剩余血量: 更新老一/更1 血量（纯数字，单位是w，有空格）\n"
    # msg += "查询boss当前状态: 老一状态/状态1\n"
    msg += "boss死亡后: 老一了/老1了\n"
    msg += "上树: 上树/挂树\n"
    msg += "查询挂树情况: 树上情况/状态\n"
    msg += "切换阶段: 一阶了\n"
    msg += "修改圈数: 修改圈 数字\n"
    # msg += "重置boss数据: 重置 数字（1-5）\n"
    msg += "查询活跃度: 我的活跃度/排名\n"
    # await reply_group(app, member.group.id, msg)
    # time.sleep(1)
    msg += "预订任务: 添加任务：x月x号x点x分和可可萝一起洗澡\n"
    msg += "取消任务: 删除任务：任务id（查询获得）\n"
    msg += "查询任务: 我的任务"
    await reply_group(app, member.group.id, msg)


async def exchange_stage(app, member, index):
    global guild_data
    if guild_data['current_stage'] == index:
        return await reply_group(app, member.group.id, '已进入 ' + str(index) + ' 阶段，不需要切换')
    elif guild_data['current_stage'] == index - 1:
        guild_data['current_stage'] = index
        # guild_data['current_boss'] = 1
        guild_data['current_boss_data'] = boss_data[index - 1]
        write_guild(member.group.id)
        await reply_group(app, member.group.id, '进入 ' + str(index) + ' 阶段')
        time.sleep(5)
        await boss_dead(app, member, 1)
    # elif guild_data['current_stage'] < index - 1:
    else:
        return await reply_group(app, member.group.id,
                                 '当前阶段为第 ' + str(guild_data['current_stage']) + ' 阶段, 不能进入 ' + str(index) + ' 阶段')


async def order_boss(app, member, arg, index):
    global guild_data
    boss = guild_data['current_boss_data'][index - 1]
    killers = boss['killers'].copy()
    killer = {'name': member.memberName, 'hp': 0}
    if check_dmg(arg):
        # pprint(killers)
        killer['hp'] = int(arg)
        if index + 1 == guild_data['current_boss']:
            cache_boss = guild_data['cache_boss']
            cache_killers = cache_boss['killers'].copy()
            if str(member.id) in killers:
                # await cancel_boss(app, member, name, index, False)
                # return await order_boss(app, member, arg, name, index)
                return await reply_group(app, member.group.id, '你已经预约过【本轮】老 ' + str(index) + ' 了', [member.id])
            if boss['pre_hp'] == 0 and cache_boss['pre_hp'] == 0:
                return await reply_group(app, member.group.id, '老 ' + str(index) + ' 已被预约完，无法再预约', [member.id])
            else:
                if int(arg) > boss['real_hp']:
                    return await reply_group(app, member.group.id,
                                             '预约血量超过【本轮】老 ' + str(index) + ' 实际剩余血量(' + str(
                                                 boss['real_hp']) + '), 请重新预约',
                                             [member.id])
                elif int(arg) <= boss['pre_hp']:
                    boss['pre_hp'] -= int(arg)
                    killers[member.id] = killer
                    boss['killers'] = killers
                    write_guild(member.group.id)
                    return await reply_group(app, member.group.id, '【本轮】老 ' + str(index) + ' 预约成功', [member.id])
                else:
                    if str(member.id) in cache_killers:
                        # await cancel_boss(app, member, name, index, False)
                        # return await order_boss(app, member, arg, name, index)
                        return await reply_group(app, member.group.id, '你已经预约过【下一轮】老 ' + str(index) + ' 了', [member.id])
                    if int(arg) <= cache_boss['pre_hp']:
                        cache_boss['pre_hp'] -= int(arg)
                        cache_killers[member.id] = killer
                        cache_boss['killers'] = cache_killers
                        write_guild(member.group.id)
                        return await reply_group(app, member.group.id, '【下一轮】老 ' + str(index) + ' 预约成功', [member.id])
                    else:
                        return await reply_group(app, member.group.id,
                                                 '预约血量超过【下一轮】老 ' + str(index) + ' 剩余预约血量(' + str(
                                                     boss['pre_hp']) + ', ' + str(cache_boss['pre_hp']) + '), 请重新预约',
                                                 [member.id])
        else:
            if str(member.id) in killers:
                # await cancel_boss(app, member, name, index, False)
                # return await order_boss(app, member, arg, name, index)
                return await reply_group(app, member.group.id, '你已经预约过老 ' + str(index) + ' 了', [member.id])
            if boss['pre_hp'] == 0:
                return await reply_group(app, member.group.id, '老 ' + str(index) + ' 已被预约完，无法再预约', [member.id])
            else:
                if int(arg) <= boss['pre_hp']:
                    boss['pre_hp'] -= int(arg)
                    killers[member.id] = killer
                    boss['killers'] = killers
                    write_guild(member.group.id)
                    return await reply_group(app, member.group.id, '老 ' + str(index) + ' 预约成功', [member.id])
                else:
                    return await reply_group(app, member.group.id,
                                             '预约血量超过老 ' + str(index) + ' 剩余预约血量(' + str(boss['pre_hp']) + '), 请重新预约',
                                             [member.id])
    else:
        return await reply_group(app, member.group.id, ILLEGAL_ERR, [member.id])


async def order_next_boss(app, member, arg):
    global guild_data
    current_boss = guild_data['current_boss']
    cache_boss = guild_data['cache_boss']
    cache_killers = cache_boss['killers'].copy()
    killer = {'name': member.memberName, 'hp': 0}
    if check_dmg(arg):
        # pprint(killers)
        killer['hp'] = int(arg)
        if str(member.id) in cache_killers:
            # await cancel_boss(app, member, name, index, False)
            # return await order_boss(app, member, arg, name, index)
            return await reply_group(app, member.group.id, '你已经预约过【下一轮】老 ' + str(current_boss) + ' 了', [member.id])
        if int(arg) <= cache_boss['pre_hp']:
            cache_boss['pre_hp'] -= int(arg)
            cache_killers[member.id] = killer
            cache_boss['killers'] = cache_killers
            write_guild(member.group.id)
            return await reply_group(app, member.group.id, '【下一轮】老 ' + str(current_boss) + ' 预约成功', [member.id])
        else:
            return await reply_group(app, member.group.id,
                                     '预约血量超过【下一轮】老 ' + str(current_boss) + ' 剩余预约血量(' + str(
                                         cache_boss['pre_hp']) + ', ' + str(
                                         cache_boss['pre_hp']) + '), 请重新预约', [member.id])

    else:
        return await reply_group(app, member.group.id, ILLEGAL_ERR, [member.id])


async def cancel_boss(app, member, index, reply=True, report=True):
    global guild_data
    boss = guild_data['current_boss_data'][index - 1]
    killers = boss['killers']
    if index + 1 == guild_data['current_boss']:
        cache_boss = guild_data['cache_boss']
        cache_killers = cache_boss['killers']
        if str(member.id) not in killers and str(member.id) not in cache_killers and reply:
            return await reply_group(app, member.group.id, '你还没预约老 ' + str(index), [member.id])
        if str(member.id) in killers:
            preKiller = killers[str(member.id)]
            if report:
                boss['pre_hp'] += preKiller['hp']
            del killers[str(member.id)]
            write_guild(member.group.id)
            if reply:
                return await reply_group(app, member.group.id, '【本轮】老 ' + str(index) + ' 取消成功', [member.id])
        elif str(member.id) in cache_killers:
            preKiller = cache_killers[str(member.id)]
            cache_boss['pre_hp'] += preKiller['hp']
            del cache_killers[str(member.id)]
            write_guild(member.group.id)
            if reply:
                return await reply_group(app, member.group.id, '【下一轮】老 ' + str(index) + ' 取消成功', [member.id])
    else:
        if str(member.id) not in killers and reply:
            return await reply_group(app, member.group.id, '你还没预约老 ' + str(index), [member.id])
        preKiller = killers[str(member.id)]
        boss['pre_hp'] += preKiller['hp']
        del killers[str(member.id)]
        write_guild(member.group.id)
        if reply:
            return await reply_group(app, member.group.id, '老 ' + str(index) + ' 取消成功', [member.id])


async def cancel_next_boss(app, member):
    global guild_data
    current_boss = guild_data['current_boss']
    cache_boss = guild_data['cache_boss']
    cache_killers = cache_boss['killers']
    if str(member.id) not in cache_killers:
        return await reply_group(app, member.group.id, '你还没预约【下一轮】老 ' + str(current_boss), [member.id])
    if str(member.id) in cache_killers:
        preKiller = cache_killers[str(member.id)]
        cache_boss['pre_hp'] += preKiller['hp']
        del cache_killers[str(member.id)]
        write_guild(member.group.id)
        return await reply_group(app, member.group.id, '【下一轮】老 ' + str(current_boss) + ' 取消成功', [member.id])


async def boss_dead(app, member, index):
    global guild_data
    current_boss = guild_data['current_boss']
    if current_boss == index:
        return await reply_group(app, member.group.id, '目前的boss就是老 ' + str(current_boss))
    elif (current_boss != 5 and current_boss == index - 1) or (current_boss == 5 and index == 1):
        # 先重置打完boss的数据
        current = guild_data['current_boss_data'][current_boss - 1]
        # current['real_hp'] = current['all_hp']
        cache_boss: dict = guild_data['cache_boss'].copy()
        cache_boss['real_hp'] = cache_boss['all_hp']
        # print('cache_boss')
        current.update(cache_boss)
        # print('killers')
        # 在初始化下一个boss的数据
        boss = guild_data['current_boss_data'][index - 1]
        # pprint(boss)
        guild_data['cache_boss'] = boss_data[guild_data['current_stage'] - 1][current_boss].copy()

        await down_tree(app, member)

        time.sleep(5)

        guild_data['current_boss'] = index
        if index == 1:
            guild_data['current_loop'] += 1
        write_guild(member.group.id)
        killers = boss['killers']
        members = []
        msg = '老 ' + str(index) + ' 了'
        if len(killers) > 0:
            rank_list = sort_dmg(killers)
            for rank in rank_list:
                # await reply_group(app, member.group.id, name + '了', [rank[0]])
                # print_msg(rank=rank)
                members.append(int(rank[0]))
                msg += ', ' + rank[1] + '伤害为' + str(rank[2])
            #     time.sleep(30)
            # return
            msg += ', 请注意按预约伤害排名出刀'
        return await reply_group(app, member.group.id, msg, members)
    else:
        return await reply_group(app, member.group.id, '当前boss为老 ' + str(current_boss) + ', 不能跳到老 ' + str(index))


async def boss_dead_bak(app, member, name, index):
    global guild_data
    current_boss = guild_data['current_boss']
    if current_boss == index + 1:
        return await reply_group(app, member.group.id, '目前的boss就是老 ' + str(current_boss))
    elif (current_boss != 5 and current_boss == index) or (current_boss == 5 and index == 0):
        # 先重置打完boss的数据
        current = guild_data['current_boss_data'][current_boss - 1]
        # current['real_hp'] = current['all_hp']
        cache_boss: dict = guild_data['cache_boss'].copy()
        cache_boss['real_hp'] = cache_boss['all_hp']
        # print('cache_boss')
        current.update(cache_boss)
        # print('killers')
        # 在初始化下一个boss的数据
        boss = guild_data['current_boss_data'][index]
        # pprint(boss)
        guild_data['cache_boss'] = boss_data[guild_data['current_stage'] - 1][current_boss].copy()

        await down_tree(app, member)

        time.sleep(5)

        guild_data['current_boss'] = index + 1
        if index == 0:
            guild_data['current_loop'] += 1
        write_guild(member.group.id)
        killers = boss['killers']
        members = []
        msg = name + '了'
        if len(killers) > 0:
            rank_list = sort_dmg(killers)
            for rank in rank_list:
                # await reply_group(app, member.group.id, name + '了', [rank[0]])
                # print_msg(rank=rank)
                members.append(int(rank[0]))
                msg += ', ' + rank[1] + '伤害为' + str(rank[2])
            #     time.sleep(30)
            # return
            msg += ', 请注意按预约伤害排名出刀'
        return await reply_group(app, member.group.id, msg, members)
    else:
        return await reply_group(app, member.group.id, '当前boss为老' + str(current_boss) + ', 不能跳到' + name)


def sort_dmg(g):
    # p = {}
    # for g_k in g.keys():
    #     p[g_k] = g[g_k]['hp']
    # pprint(p)
    p = []
    for g_k in g.keys():
        t_name = strQ2B(g[g_k]['name']).split('(', maxsplit=1)[0]
        t = (g_k, t_name, g[g_k]['hp'])
        # print(t)
        p.append(t)
    rank_list = sorted(p, key=lambda x: x[2], reverse=True)
    # pprint(rank_list)
    return rank_list


async def reset_boss(app, member, index):
    global guild_data
    if index < 1 or index > 5:
        return await reply_group(app, member.group.id, '只能重置1-5')
    current = guild_data['current_boss_data'][int(index) - 1]
    current['pre_hp'] = current['real_hp'] = current['all_hp']
    current['killers'] = {}
    write_guild(member.group.id)
    await reply_group(app, member.group.id, '重置老 ' + str(index) + ' 成功')


async def stage_info(app, member):
    global guild_data
    current_stage = guild_data['current_stage']
    current_boss = guild_data['current_boss']
    current_loop = guild_data['current_loop']
    msg = '当前为第 ' + str(current_stage) + ' 阶 - 第 ' + str(current_loop) + ' 圈\n\n'
    boss_list: list = guild_data['current_boss_data']
    boss_list.insert(current_boss - 1, guild_data['cache_boss'])
    # pprint(boss_list)
    for i, boss in enumerate(boss_list):
        tmp = ''
        index = i + 1
        if current_boss == i:
            index = i
            tmp += '【正在进行中】 -> '
        elif current_boss < i:
            index = i
        killers = boss['killers']
        if current_boss == i + 1:
            tmp += '预约下一轮老 ' + str(index) + ' 的有 ' + str(len(killers)) + " 个人,"
        else:
            tmp += '预约老 ' + str(index) + ' 的有 ' + str(len(killers)) + " 个人,"
        if len(killers) > 0:
            tmp += " 分别是："
            for key in killers.keys():
                killer = killers[key]
                k_name = strQ2B(killer['name']).split('(', maxsplit=1)[0]
                tmp += k_name + ' ' + str(killer['hp']) + '、'
        pre_hp = 0
        if boss['pre_hp'] > 0:
            pre_hp = boss['pre_hp']
        msg += tmp[:len(tmp) - 1] + ", 预约剩余血量：" + str(pre_hp) + ", 实际剩余血量：" + str(boss['real_hp']) + '\n\n'
    return await reply_group(app, member.group.id, msg, [member.id])


async def report_dmg(app, member, arg):
    global guild_data
    current_boss = guild_data['current_boss']
    boss = guild_data['current_boss_data'][current_boss - 1]
    if check_dmg(arg):
        if int(arg) > boss['real_hp']:
            return await reply_group(app, member.group.id, '无效数据，伤害不会比剩余血量高, 实际剩余血量：' + str(boss['real_hp']),
                                     [member.id])
        else:
            boss['real_hp'] -= int(arg)
            write_guild(member.group.id)

            await reply_group(app, member.group.id, '报刀成功, 老' + str(current_boss) + '实际剩余血量：' + str(boss['real_hp']),
                              [member.id])
            # time.sleep(5)
            killers = boss['killers']
            if str(member.id) in killers:
                return await cancel_boss(app, member, '老' + str(current_boss), current_boss - 1, False, False)
    else:
        return await reply_group(app, member.group.id, ILLEGAL_ERR, [member.id])


async def update_hp(app, member, arg, index):
    global guild_data
    boss = guild_data['current_boss_data'][index - 1]
    if check_dmg(arg):
        boss['real_hp'] = int(arg)
        write_guild(member.group.id)
        return await reply_group(app, member.group.id, '老 ' + str(index) + ' 血量更新成功')
    else:
        return await reply_group(app, member.group.id, ILLEGAL_ERR, [member.id])


async def update_loop(app, member, arg):
    global guild_data
    if check_dmg(arg):
        guild_data['current_loop'] = int(arg)
        write_guild(member.group.id)
        return await reply_group(app, member.group.id, '修改圈数成功')
    else:
        return await reply_group(app, member.group.id, ILLEGAL_ERR, [member.id])


async def up_tree(app, member):
    global guild_data
    if str(member.id) in guild_data['tree_members']:
        return await reply_group(app, member.group.id, '不要重复上树', [member.id])
    guild_data['tree_members'][member.id] = member.memberName
    write_guild(member.group.id)
    return await reply_group(app, member.group.id, '上树成功', [member.id])


async def down_tree(app, member):
    global guild_data
    members = guild_data['tree_members'].keys()
    if len(members) == 0:
        return await reply_group(app, member.group.id, '树上无人')
    # print(members)
    await reply_group(app, member.group.id, 'boss已死亡', map(int, members))
    guild_data['tree_members'].clear()
    write_guild(member.group.id)
    return


async def tree_info(app, member):
    global guild_data
    members = guild_data['tree_members'].values()
    if len(members) == 0:
        return await reply_group(app, member.group.id, '树上无人')
    msg = '树上有 ' + str(len(members)) + ' 个人，分别是：'
    for name in members:
        msg += name + '、'
    msg = msg[:len(msg) - 1]
    return await reply_group(app, member.group.id, msg)
