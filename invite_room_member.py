# 关键词触发邀请好友进群

import sys
import ntchat

wechat = ntchat.WeChat()

# 打开pc微信, smart: 是否管理已经登录的微信
wechat.open(smart=True)

wechat.wait_login()

# 获取群
rooms = wechat.get_rooms()
for room in rooms:
    if room["nickname"] == "测试群":  # 精确查找群名为 测试群 的群
        room_wxid = room["wxid"]

# 注册消息回调
@wechat.msg_register(ntchat.MT_RECV_TEXT_MSG)
def on_recv_text_msg(wechat_instance: ntchat.WeChat, message):
    data = message["data"]
    from_wxid = data["from_wxid"]
    msg = data["msg"]
    self_wxid = wechat_instance.get_login_info()["wxid"]
    if from_wxid != self_wxid:  # 排除自己发的，否则一直回调
        if msg == "进群":  # 如果收到的消息是 进群 则邀请进群
            # 邀请微信好友加入群聊
            wechat.invite_room_member(room_wxid, [from_wxid])

try:
    while True:
        pass
except KeyboardInterrupt:
    ntchat.exit_()
    sys.exit()