import time
from pprint import pprint

from mirai import Permission, Member

from plugins.common.constants import *
from plugins.common.commons import *
from plugins.guild.manage import is_guild_member

boss_data = [[]]


def init():
    global boss_data
    boss_data = read_json('data/boss_data.json')


init()


def write_battle(groupId, g_data):
    write_json('data/battle/' + str(groupId) + '.json', g_data)


def read_battle(groupId):
    try:
        return read_json('data/battle/' + str(groupId) + '.json')
    except FileNotFoundError:
        return {'battle_state': '关闭', 'current_stage': 1, 'current_boss': 1, 'current_loop': 1,
                'tree_members': {}, 'cache_boss': boss_data[0][0].copy(), 'current_boss_data': boss_data[0].copy()}


async def start_battle(app, member: Member, arg):
    if not await is_guild_member(app, member):
        return
    if member.permission == Permission.Member:
        return await reply_group(app, member.group.id, '无权限使用此命令，请联系会长或管理')
    guild_data = {'battle_state': '开启', 'current_stage': 1, 'current_boss': 1, 'current_loop': 1,
                  'tree_members': {}, 'cache_boss': boss_data[0][0].copy(), 'current_boss_data': boss_data[0].copy()}
    write_battle(member.group.id, guild_data)
    return await reply_group(app, member.group.id, '会战已开启')


async def end_battle(app, member, arg):
    if not await is_guild_member(app, member):
        return
    if member.permission == Permission.Member:
        return await reply_group(app, member.group.id, '无权限使用此命令，请联系会长或管理')
    guild_data = read_battle(member.group.id)
    guild_data['battle_state'] = '关闭'
    write_battle(member.group.id, guild_data)
    return await reply_group(app, member.group.id, '会战已关闭')


async def is_battle(app, member):
    if not await is_guild_member(app, member):
        return False
    guild_data = read_battle(member.group.id)
    if guild_data['battle_state'] == '关闭':
        await reply_group(app, member.group.id, '会战功能还未开启，请联系会长或管理')
        return False
    return True


async def exchange_stage(app, member, index):
    if not await is_battle(app, member):
        return
    guild_data = read_battle(member.group.id)
    if guild_data['current_stage'] == index:
        return await reply_group(app, member.group.id, '已进入 ' + str(index) + ' 阶段，不需要切换')
    elif guild_data['current_stage'] == index - 1:
        guild_data['current_stage'] = index
        guild_data['current_boss_data'] = boss_data[index - 1]
        write_battle(member.group.id, guild_data)
        await reply_group(app, member.group.id, '进入 ' + str(index) + ' 阶段')
        time.sleep(5)
        await boss_dead(app, member, 1, True)
    else:
        return await reply_group(app, member.group.id,
                                 '当前阶段为第 ' + str(guild_data['current_stage']) + ' 阶段, 不能进入 ' + str(index) + ' 阶段')


async def order_boss(app, member, arg: str, index):
    if not await is_battle(app, member):
        return
    guild_data = read_battle(member.group.id)
    boss = guild_data['current_boss_data'][index - 1]
    killers = boss['killers'].copy()
    killer = {'name': member.memberName, 'hp': 0, 'tail': 0}
    if check_dmg(arg):
        if arg.endswith('*'):
            killer['tail'] = 1
            arg = arg[:len(arg) - 1]
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
                    write_battle(member.group.id, guild_data)
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
                        write_battle(member.group.id, guild_data)
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
                    write_battle(member.group.id, guild_data)
                    return await reply_group(app, member.group.id, '老 ' + str(index) + ' 预约成功', [member.id])
                else:
                    return await reply_group(app, member.group.id,
                                             '预约血量超过老 ' + str(index) + ' 剩余预约血量(' + str(boss['pre_hp']) + '), 请重新预约',
                                             [member.id])
    else:
        return await reply_group(app, member.group.id, ILLEGAL_ERR, [member.id])


async def order_next_boss(app, member, arg):
    if not await is_battle(app, member):
        return
    guild_data = read_battle(member.group.id)
    current_boss = guild_data['current_boss']
    cache_boss = guild_data['cache_boss']
    cache_killers = cache_boss['killers'].copy()
    killer = {'name': member.memberName, 'hp': 0}
    if check_dmg(arg):
        if arg.endswith('*'):
            killer['tail'] = 1
            arg = arg[:len(arg) - 1]
        killer['hp'] = int(arg)
        if str(member.id) in cache_killers:
            # await cancel_boss(app, member, name, index, False)
            # return await order_boss(app, member, arg, name, index)
            return await reply_group(app, member.group.id, '你已经预约过【下一轮】老 ' + str(current_boss) + ' 了', [member.id])
        if int(arg) <= cache_boss['pre_hp']:
            cache_boss['pre_hp'] -= int(arg)
            cache_killers[member.id] = killer
            cache_boss['killers'] = cache_killers
            write_battle(member.group.id, guild_data)
            return await reply_group(app, member.group.id, '【下一轮】老 ' + str(current_boss) + ' 预约成功', [member.id])
        else:
            return await reply_group(app, member.group.id,
                                     '预约血量超过【下一轮】老 ' + str(current_boss) + ' 剩余预约血量(' + str(
                                         cache_boss['pre_hp']) + ', ' + str(
                                         cache_boss['pre_hp']) + '), 请重新预约', [member.id])
    else:
        return await reply_group(app, member.group.id, ILLEGAL_ERR, [member.id])


async def cancel_boss(app, member, index, reply=True, report=True):
    if not await is_battle(app, member):
        return
    guild_data = read_battle(member.group.id)
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
            write_battle(member.group.id, guild_data)
            if reply:
                return await reply_group(app, member.group.id, '【本轮】老 ' + str(index) + ' 取消成功', [member.id])
        elif str(member.id) in cache_killers:
            preKiller = cache_killers[str(member.id)]
            cache_boss['pre_hp'] += preKiller['hp']
            del cache_killers[str(member.id)]
            write_battle(member.group.id, guild_data)
            if reply:
                return await reply_group(app, member.group.id, '【下一轮】老 ' + str(index) + ' 取消成功', [member.id])
    else:
        if str(member.id) not in killers and reply:
            return await reply_group(app, member.group.id, '你还没预约老 ' + str(index), [member.id])
        preKiller = killers[str(member.id)]
        boss['pre_hp'] += preKiller['hp']
        del killers[str(member.id)]
        write_battle(member.group.id, guild_data)
        if reply:
            return await reply_group(app, member.group.id, '老 ' + str(index) + ' 取消成功', [member.id])


async def cancel_next_boss(app, member):
    if not await is_battle(app, member):
        return
    guild_data = read_battle(member.group.id)
    current_boss = guild_data['current_boss']
    cache_boss = guild_data['cache_boss']
    cache_killers = cache_boss['killers']
    if str(member.id) not in cache_killers:
        return await reply_group(app, member.group.id, '你还没预约【下一轮】老 ' + str(current_boss), [member.id])
    if str(member.id) in cache_killers:
        preKiller = cache_killers[str(member.id)]
        cache_boss['pre_hp'] += preKiller['hp']
        del cache_killers[str(member.id)]
        write_battle(member.group.id, guild_data)
        return await reply_group(app, member.group.id, '【下一轮】老 ' + str(current_boss) + ' 取消成功', [member.id])


async def boss_dead(app, member, index, next_stage=False):
    if not await is_battle(app, member):
        return
    guild_data = read_battle(member.group.id)
    current_boss = guild_data['current_boss']
    if current_boss == index:
        return await reply_group(app, member.group.id, '目前的boss就是老 ' + str(current_boss))
    elif (current_boss != 5 and current_boss == index - 1) or (current_boss == 5 and index == 1) or next_stage:
        # 先重置打完boss的数据
        current = guild_data['current_boss_data'][current_boss - 1]
        cache_boss: dict = guild_data['cache_boss'].copy()
        cache_boss['real_hp'] = cache_boss['all_hp']
        current.update(cache_boss)
        # 在初始化下一个boss的数据
        boss = guild_data['current_boss_data'][index - 1]
        guild_data['cache_boss'] = boss_data[guild_data['current_stage'] - 1][current_boss].copy()

        await down_tree(app, member)

        time.sleep(5)

        guild_data['current_boss'] = index
        if index == 1:
            guild_data['current_loop'] += 1
        write_battle(member.group.id, guild_data)
        killers = boss['killers']
        members = []
        msg = '老 ' + str(index) + ' 了\n'
        if len(killers) > 0:
            rank_list = sort_dmg(killers)
            for rank in rank_list:
                members.append(int(rank[0]))
                msg += rank[1] + ' ' + str(rank[2])
                if rank[3] == 1:
                    msg += ' 是尾刀/补偿刀'
                msg += ', '
            msg += '请遵守尾刀和大刀优先的原则，按顺序出刀'
        return await reply_group(app, member.group.id, msg, members)
    else:
        return await reply_group(app, member.group.id, '当前boss为老 ' + str(current_boss) + ', 不能跳到老 ' + str(index))


async def reset_boss(app, member, index):
    if not await is_battle(app, member):
        return
    guild_data = read_battle(member.group.id)
    if index < 1 or index > 5:
        return await reply_group(app, member.group.id, '只能重置1-5')
    current = guild_data['current_boss_data'][int(index) - 1]
    current['pre_hp'] = current['real_hp'] = current['all_hp']
    current['killers'] = {}
    write_battle(member.group.id, guild_data)
    await reply_group(app, member.group.id, '重置老 ' + str(index) + ' 成功')


async def stage_info(app, member):
    if not await is_battle(app, member):
        return
    guild_data = read_battle(member.group.id)
    current_stage = guild_data['current_stage']
    current_boss = guild_data['current_boss']
    current_loop = guild_data['current_loop']
    msg = '当前为第 ' + str(current_stage) + ' 阶 - 第 ' + str(current_loop) + ' 圈\n\n'
    boss_list: list = guild_data['current_boss_data']
    boss_list.insert(current_boss - 1, guild_data['cache_boss'])
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
    if not await is_battle(app, member):
        return
    guild_data = read_battle(member.group.id)
    current_boss = guild_data['current_boss']
    boss = guild_data['current_boss_data'][current_boss - 1]
    if check_dmg(arg):
        if arg.endswith('*'):
            arg = arg[:len(arg) - 1]
        if int(arg) > boss['real_hp']:
            return await reply_group(app, member.group.id, '无效数据，伤害不会比剩余血量高, 实际剩余血量：' + str(boss['real_hp']),
                                     [member.id])
        else:
            boss['real_hp'] -= int(arg)
            write_battle(member.group.id, guild_data)
            await reply_group(app, member.group.id, '报刀成功, 老' + str(current_boss) + '实际剩余血量：' + str(boss['real_hp']),
                              [member.id])

            killers = boss['killers']
            if str(member.id) in killers:
                return await cancel_boss(app, member, current_boss - 1, False, False)
    else:
        return await reply_group(app, member.group.id, ILLEGAL_ERR, [member.id])


async def update_hp(app, member, arg, index):
    if not await is_battle(app, member):
        return
    guild_data = read_battle(member.group.id)
    boss = guild_data['current_boss_data'][index - 1]
    if check_dmg(arg):
        if arg.endswith('*'):
            arg = arg[:len(arg) - 1]
        boss['real_hp'] = int(arg)
        write_battle(member.group.id, guild_data)
        return await reply_group(app, member.group.id, '老 ' + str(index) + ' 血量更新成功')
    else:
        return await reply_group(app, member.group.id, ILLEGAL_ERR, [member.id])


async def update_loop(app, member, arg):
    if not await is_battle(app, member):
        return
    guild_data = read_battle(member.group.id)
    if check_dmg(arg):
        if arg.endswith('*'):
            arg = arg[:len(arg) - 1]
        guild_data['current_loop'] = int(arg)
        write_battle(member.group.id, guild_data)
        return await reply_group(app, member.group.id, '修改圈数成功')
    else:
        return await reply_group(app, member.group.id, ILLEGAL_ERR, [member.id])


async def up_tree(app, member):
    if not await is_battle(app, member):
        return
    guild_data = read_battle(member.group.id)
    if str(member.id) in guild_data['tree_members']:
        return await reply_group(app, member.group.id, '不要重复上树', [member.id])
    guild_data['tree_members'][member.id] = member.memberName
    write_battle(member.group.id, guild_data)
    return await reply_group(app, member.group.id, '上树成功', [member.id])


async def down_tree(app, member):
    if not await is_battle(app, member):
        return
    guild_data = read_battle(member.group.id)
    members = guild_data['tree_members'].keys()
    if len(members) == 0:
        return await reply_group(app, member.group.id, '树上无人')
    await reply_group(app, member.group.id, 'boss已死亡', map(int, members))
    guild_data['tree_members'].clear()
    write_battle(member.group.id, guild_data)
    return


async def tree_info(app, member):
    if not await is_battle(app, member):
        return
    guild_data = read_battle(member.group.id)
    members = guild_data['tree_members'].values()
    if len(members) == 0:
        return await reply_group(app, member.group.id, '树上无人')
    msg = '树上有 ' + str(len(members)) + ' 个人，分别是：'
    for name in members:
        msg += name + '、'
    msg = msg[:len(msg) - 1]
    return await reply_group(app, member.group.id, msg)
