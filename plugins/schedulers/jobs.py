import datetime
from mirai import Mirai, At, AtAll, Member, Plain


# 定义定时任务
async def aps_job(app: Mirai, msg: str, member: Member, isAll=False):
    if isAll:
        await app.sendGroupMessage(member.group, [AtAll(), Plain(text=msg)])
    else:
        await app.sendGroupMessage(member.group, [At(target=member.id), Plain(text=msg)])


async def kill_warn(app: Mirai, group):
    await app.sendGroupMessage(group, [AtAll(), Plain(text='可可萝提醒主人，该出刀了')])
