from apscheduler.schedulers.asyncio import AsyncIOScheduler

from plugins.common.commons import *
from plugins.scheduler.jobs import *

scheduler = AsyncIOScheduler()


def run_scheduler():
    try:
        # 重置活跃度数据
        # scheduler.add_job(func=init_all_group_active, args=[app, manage_groups], trigger='date',
        #                   run_date='2020-03-25 05:00:00')
        # scheduler.add_job(func=kill_warn, args=[app, 1027426994], trigger='cron',
        #                   hour='21', start_date='2020-03-25 05:00:00', end_date='2020-03-30 23:00:00')
        # 启动定时任务调度器工作
        scheduler.start()
        print_msg(msg='定时任务调度器已启动')
    except SystemError:
        print_msg(tag='Error', msg='定时任务调度器启动失败')


async def add_job(app: Mirai, member: Member, arg: str):
    # content = eval(textList[1])
    content = deal_job(arg)
    print('content:', content)
    if content is None:
        return await app.sendGroupMessage(member.group, [At(target=member.id), Plain(text='格式不合法')])
    current_t = datetime.datetime.now().timestamp()
    pre_t = datetime.datetime.strptime(content['time'], "%Y-%m-%d %H:%M:%S").timestamp()
    if pre_t < current_t:
        return await app.sendGroupMessage(member.group, [At(target=member.id), Plain(text='不能添加比现在还早的任务')])
    job_id = uniqueNumStr()
    job_name = str(member.group.id) + '#' + str(member.id) + '#' + content['task']
    msg = '当前任务ID：' + job_id + '\n 可可萝将会在' + content['time'] + '提醒主人：' + content['task']
    if '艾特所有人' in content['task']:
        tmp = content['task'][5:]
        scheduler.add_job(id=job_id, name=job_name, func=aps_job, args=[app, tmp, member, True],
                          trigger='date', run_date=content['time'])
        msg = '当前任务ID：' + job_id + '\n 可可萝将会在' + content['time'] + '艾特所有人：' + tmp
    else:
        scheduler.add_job(id=job_id, name=job_name, func=aps_job, args=[app, content['task'], member],
                          trigger='date', run_date=content['time'])
    print('任务内容', msg)
    return await app.sendGroupMessage(member.group, [At(target=member.id), Plain(text=msg)])


async def remove_job(app: Mirai, member: Member, arg: str):
    if not check_job(arg):
        return await app.sendGroupMessage(member.group, [At(target=member.id), Plain(text='格式不合法')])
    job_id = arg
    scheduler.remove_job(job_id)
    return await app.sendGroupMessage(member.group,
                                      [At(target=member.id), Plain(text='任务' + job_id + '已被可可萝移除 ~ ')])


async def query_job(app: Mirai, member: Member, arg: str):
    jobs = scheduler.get_jobs()
    # print(jobs)
    plains = []
    for job in jobs:
        jobStr = str(job.name).split('#')
        # print(jobStr)
        if jobStr[0] == str(member.group.id) and jobStr[1] == str(member.id):
            msg = '任务ID：' + job.id + '\t 时间：' + job.next_run_time.strftime('%Y-%m-%d %H:%M:%S') + '\t 内容：' + jobStr[
                2] + '\n'
            plains.append(Plain(text=msg))
    if len(plains) > 0:
        m = [At(target=member.id), Plain(text='可可萝为你查询到的所有任务如下：\n')] + plains
        await app.sendGroupMessage(member.group, m)
    else:
        return await app.sendGroupMessage(member.group, [At(target=member.id), Plain(text='可可萝未查询到你的任务')])
