import time

from mirai import MessageChain, MemberJoinEvent
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc

from plugins.guild.guild import initData
from plugins.guild.activities import *
import plugins.guild.cmds  # 注册命令必须
from plugins.common.decorators import commands
from pprint import pprint
from plugins.common.commons import *
import yaml

from plugins.schedulers.jobs import kill_warn
from plugins.schedulers.manage import task_manage

f = open('config/bot.yaml', encoding="utf-8")
cfg = yaml.load(f, Loader=yaml.FullLoader)

app = Mirai(f"{cfg['host']}?authKey={cfg['authKey']}&qq={cfg['qq']}", websocket={cfg['enableWebsocket']})

manage_groups = cfg['groups']


@app.receiver("MemberJoinEvent")
async def member_join(app: Mirai, event: MemberJoinEvent):
    await app.sendGroupMessage(
        event.member.group.id,
        [
            At(target=event.member.id),
            Plain(text="欢迎大佬进群 ヾ(@^▽^@)ノ ")
        ]
    )


last_received_time = datetime.datetime.now()


@app.receiver("GroupMessage")
async def event_gm(app: Mirai, message: MessageChain, member: Member):
    global manage_groups, last_received_time
    # print(manage_groups)
    if member.group.id not in manage_groups:
        return

    # print(message)
    await calculate_points(app, member)

    first_plain = message.getFirstComponent(Plain)
    if first_plain is None:
        return
    msg = first_plain.toString().strip()
    if msg == '':
        return
    print_msg(msg=msg)

    if datetime.datetime.now().timestamp() - last_received_time.timestamp() < 5:
        time.sleep(random.randint(0, 2))
    last_received_time = datetime.datetime.now()

    sp = msg.split(maxsplit=1)
    print_msg(sp=sp)
    cmd, *args = sp
    arg = ''.join(args)
    print_msg(cmd=cmd)
    print_msg(arg=arg)
    handler = commands.get(cmd)
    print_msg(handler=handler)

    if handler:
        initData(member)
        return await handler(app, member, arg)
    else:
        await task_manage(app, message, member, scheduler)


scheduler = AsyncIOScheduler()


def run_scheduler():
    try:
        # 重置活跃度数据
        scheduler.add_job(func=init_all_group_active, args=[app, manage_groups], trigger='date',
                          run_date='2020-03-25 05:00:00')
        scheduler.add_job(func=kill_warn, args=[app, 1027426994], trigger='cron',
                          hour='21', start_date='2020-03-25 05:00:00', end_date='2020-03-30 23:00:00')
        # 启动定时任务调度器工作
        scheduler.start()
        print_msg(msg='定时任务调度器已启动')
    except SystemError:
        print('exit')
        exit()


@app.subroutine
async def _(app: Mirai):
    await init_active(app)


if __name__ == "__main__":
    run_scheduler()
    print_msg(manage_groups=manage_groups)
    app.run()
