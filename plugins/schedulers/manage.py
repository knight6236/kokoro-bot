from apscheduler.schedulers.asyncio import AsyncIOScheduler
from mirai import MessageChain

from plugins.common.commons import *
from plugins.schedulers.jobs import *


async def task_manage(app: Mirai, message: MessageChain, member: Member, scheduler: AsyncIOScheduler):
    first_plain = message.getFirstComponent(Plain)
    if first_plain is None:
        return
    textStr = first_plain.toString().strip()
    # print(textStr)
    textStr = strQ2B(textStr)
    # print(textStr)
    if textStr.startswith('添加任务'):
        textList = textStr.split(':', maxsplit=1)
        # print(textList)
        if len(textList) < 2:
            return await app.sendGroupMessage(member.group, [At(target=member.id), Plain(text='格式不合法')])
        # content = eval(textList[1])
        content = deal_task(textList[1])
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
    elif textStr.startswith('删除任务'):
        textList = textStr.split(':', maxsplit=1)
        if len(textList) < 2:
            return await app.sendGroupMessage(member.group, [At(target=member.id), Plain(text='格式不合法')])
        job_id = textList[1]
        scheduler.remove_job(job_id)
        return await app.sendGroupMessage(member.group,
                                          [At(target=member.id), Plain(text='任务' + job_id + '已被可可萝移除 ~ ')])
    elif textStr.startswith('我的任务'):
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
            # print(m)
            await app.sendGroupMessage(member.group, m)
        else:
            return await app.sendGroupMessage(member.group, [At(target=member.id), Plain(text='可可萝未查询到你的任务')])
