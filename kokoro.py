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

manage_groups: list = cfg['groups']

groups_config_path = 'config/manage_groups.json'


@app.receiver("MemberJoinEvent")
async def member_join(app: Mirai, event: MemberJoinEvent):
    print(event)
    await app.sendGroupMessage(
        event.member.group.id,
        [
            At(target=event.member.id),
            Plain(text="可可萝欢迎新主人进群 ヾ(@^▽^@)ノ ")
        ]
    )


last_received_time = datetime.datetime.now()


@app.receiver("GroupMessage")
async def event_gm(app: Mirai, message: MessageChain, member: Member):
    global manage_groups, last_received_time
    if os.path.exists(groups_config_path):
        manage_groups = read_json(groups_config_path)

    await calculate_points(member)

    first_plain = message.getFirstComponent(Plain)
    if first_plain is None:
        return
    msg = first_plain.toString().strip()
    if msg == '':
        return

    if '开启可可萝' == msg:
        if member.permission == Permission.Member:
            return await app.sendGroupMessage(member.group, [Plain(text='无权限使用此命令，请联系会长或管理')])
        manage_groups.append(member.group.id)
        write_json(groups_config_path, manage_groups)
        return await app.sendGroupMessage(member.group, [Plain(text='可可萝将会全力照顾主人的(*￣︶￣)~')])
    elif '关闭可可萝' == msg:
        if member.permission == Permission.Member:
            return await app.sendGroupMessage(member.group, [Plain(text='无权限使用此命令，请联系会长或管理')])
        if member.group.id in manage_groups:
            manage_groups.remove(member.group.id)
            write_json(groups_config_path, manage_groups)
            return await app.sendGroupMessage(member.group, [Plain(text='很遗憾，可可萝以后不能再照顾主人了o(╥﹏╥)o')])

    if member.group.id not in manage_groups:
        return

    if datetime.datetime.now().timestamp() - last_received_time.timestamp() < 5:
        time.sleep(random.randint(0, 2))
    last_received_time = datetime.datetime.now()

    print_msg(msg=msg)
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
