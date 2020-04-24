from plugins.common.commons import reply_group


async def menu(app, member):
    msg = '公会管理相关命令：管理菜单\n'
    msg += "公会战相关命令: 会战菜单\n"
    msg += "公会战作业相关命令: 作业菜单\n"
    msg += "定时提醒任务相关命令: 任务菜单"
    await reply_group(app, member.group.id, msg)


async def manage_menu(app, member):
    msg = '创建公会：创建/新建公会 公会名-不加就默认群名（需要管理权限）\n'
    msg += "开启/关闭成员入会: 开启/关闭公会（需要管理权限）\n"
    msg += "入会/退会: 加入/退出公会\n"
    msg += "查询公会信息: 公会信息\n"
    msg += "查询活跃度: 我的活跃度/排名"
    await reply_group(app, member.group.id, msg)


async def battle_menu(app, member):
    msg = '开启会战: 开启会战/会战开始\n'
    msg += '关闭会战: 关闭会战/会战结束\n'
    msg += '预约boss: 预约老一/预约1 数字（单位w，有空格；尾刀/补偿刀在数字后面加*）\n'
    msg += "预约下一轮boss: 预约下轮\n"
    msg += "取消预约: 取消老一/取消1\n"
    msg += "取消下一轮预约: 取消下轮\n"
    msg += "查询进度/预约/boss当前状态: 老几了/预约情况/预约状态\n"
    msg += "报刀: 报刀/打了/杀了/恰了（纯数字，单位是w，有空格）\n"
    msg += "设置boss实际剩余血量: 更新老一/更1 数字（单位w，有空格）\n"
    msg += "boss死亡后: 老一了/老1了\n"
    msg += "上树: 上树/挂树\n"
    msg += "查询挂树情况: 树上情况/状态\n"
    msg += "切换阶段: 一阶了\n"
    msg += "修改圈数: 修改圈 数字"
    await reply_group(app, member.group.id, msg)


async def task_menu(app, member):
    msg = "记录作业: 导入作业 1-1 狼克剑圣猫拳511 700\n"
    msg += "查询作业: 查询作业 1-1（可选，不加是查询全部）\n"
    msg += "查询当前boss作业: 当前作业"
    await reply_group(app, member.group.id, msg)


async def job_menu(app, member):
    msg = "预订任务: 添加任务 x月x号x点x分和可可萝一起洗澡\n"
    msg += "取消任务: 删除任务 任务id（查询获得）\n"
    msg += "查询任务: 我的任务"
    await reply_group(app, member.group.id, msg)
