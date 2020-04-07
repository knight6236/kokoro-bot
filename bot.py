import time
import yaml

# 注册命令必须先导入
import plugins.command.cmds

from mirai import MessageChain, MemberJoinEvent

from plugins.guild.manage import *
from plugins.common.decorators import commands
from plugins.scheduler.manage import run_scheduler

f = open('config/bot.yaml', encoding="utf-8")
cfg = yaml.load(f, Loader=yaml.FullLoader)

app = Mirai(f"{cfg['host']}?authKey={cfg['authKey']}&qq={cfg['qq']}", websocket={cfg['enableWebsocket']})

manage_groups = cfg['groups']


@app.receiver("MemberJoinEvent")
async def member_join(app: Mirai, event: MemberJoinEvent):
    print(event)
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
    if member.group.id not in manage_groups:
        return

    await calculate_points(member)

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
        return await handler(app, member, arg)


if __name__ == "__main__":
    print_msg(在管的群=manage_groups)
    run_scheduler()
    init_path()
    app.run()
