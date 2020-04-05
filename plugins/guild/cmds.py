from plugins.common.decorators import command
from plugins.guild.guild import *
from plugins.guild.activities import *


@command('公会菜单', aliases=['公会帮助', '菜单', '帮助', 'menu', 'help'])
async def _(app, ctx, args):
    await menu(app, ctx)


@command('一阶', aliases=['一阶了', '1阶', '1阶了'])
async def _(app, ctx, args):
    await exchange_stage(app, ctx, 1)


@command('二阶', aliases=['二阶了', '2阶', '2阶了'])
async def _(app, ctx, args):
    await exchange_stage(app, ctx, 2)


@command('三阶', aliases=['三阶了', '3阶', '3阶了'])
async def _(app, ctx, args):
    await exchange_stage(app, ctx, 3)


@command('四阶', aliases=['四阶了', '4阶', '4阶了'])
async def _(app, ctx, args):
    await exchange_stage(app, ctx, 4)


@command('预约老一', aliases=['预约老1', '预约1'])
async def _(app, ctx, args):
    await order_boss(app, ctx, args, 1)


@command('预约老二', aliases=['预约老2', '预约2'])
async def _(app, ctx, args):
    await order_boss(app, ctx, args, 2)


@command('预约老三', aliases=['预约老3', '预约3'])
async def _(app, ctx, args):
    await order_boss(app, ctx, args, 3)


@command('预约老四', aliases=['预约老4', '预约4'])
async def _(app, ctx, args):
    await order_boss(app, ctx, args, 4)


@command('预约老五', aliases=['预约老5', '预约5'])
async def _(app, ctx, args):
    await order_boss(app, ctx, args, 5)


@command('预约下轮', aliases=['预约下一轮'])
async def _(app, ctx, args):
    await order_next_boss(app, ctx, args)


@command('取消老一', aliases=['取消预约老一', '取消老1', '取消预约老1', '取消1', '取消预约1'])
async def _(app, ctx, args):
    await cancel_boss(app, ctx, 1)


@command('取消老二', aliases=['取消预约老二', '取消老2', '取消预约老2', '取消2', '取消预约2'])
async def _(app, ctx, args):
    await cancel_boss(app, ctx, 2)


@command('取消老三', aliases=['取消预约老三', '取消老3', '取消预约老3', '取消3', '取消预约3'])
async def _(app, ctx, args):
    await cancel_boss(app, ctx, 3)


@command('取消老四', aliases=['取消预约老四', '取消老4', '取消预约老4', '取消4', '取消预约4'])
async def _(app, ctx, args):
    await cancel_boss(app, ctx, 4)


@command('取消老五', aliases=['取消预约老五', '取消老5', '取消预约老5', '取消5', '取消预约5'])
async def _(app, ctx, args):
    await cancel_boss(app, ctx, 5)


@command('取消下轮', aliases=['取消下一轮'])
async def _(app, ctx, args):
    await cancel_next_boss(app, ctx)


@command('老几了', aliases=['当前进度', '当前状态', '预约情况', '预约状态', '查询预约', '预约查询'])
async def _(app, ctx, args):
    await stage_info(app, ctx)


@command('打了', aliases=['报刀', '鲨了', '杀了', '恰了'])
async def _(app, ctx, args):
    await report_dmg(app, ctx, args)


@command('重置')
async def _(app, ctx, args):
    await reset_boss(app, ctx, args)


@command('更新老一', aliases=['更1'])
async def _(app, ctx, args):
    await update_hp(app, ctx, args, 1)


@command('更新老二', aliases=['更2'])
async def _(app, ctx, args):
    await update_hp(app, ctx, args, 2)


@command('更新老三', aliases=['更3'])
async def _(app, ctx, args):
    await update_hp(app, ctx, args, 3)


@command('更新老四', aliases=['更4'])
async def _(app, ctx, args):
    await update_hp(app, ctx, args, 4)


@command('更新老五', aliases=['更5'])
async def _(app, ctx, args):
    await update_hp(app, ctx, args, 5)


@command('修改圈')
async def _(app, ctx, args):
    await update_loop(app, ctx, args)


@command('老一了', aliases=['老1了'])
async def _(app, ctx, args):
    await boss_dead(app, ctx, 1)


@command('老二了', aliases=['老2了'])
async def _(app, ctx, args):
    await boss_dead(app, ctx, 2)


@command('老三了', aliases=['老3了'])
async def _(app, ctx, args):
    await boss_dead(app, ctx, 3)


@command('老四了', aliases=['老4了'])
async def _(app, ctx, args):
    await boss_dead(app, ctx, 4)


@command('老五了', aliases=['老5了'])
async def _(app, ctx, args):
    await boss_dead(app, ctx, 5)


@command('上树', aliases=['挂树'])
async def _(app, ctx, args):
    await up_tree(app, ctx)


# @command('下树')
# async def _(app, ctx, args):
#     await down_tree(app, ctx)


@command('树上情况', aliases=['树上状态', '可以下树吗', '能下树吗'])
async def _(app, ctx, args):
    await tree_info(app, ctx)


@command('我的活跃度', aliases=['我的排名', '活跃度', '排名'])
async def _(app, ctx, args):
    await query_points(app, ctx)
