# 根据关键词回复消息

import sys
import ntchat

wechat = ntchat.WeChat()

# 打开pc微信, smart: 是否管理已经登录的微信
wechat.open(smart=True)

wechat.wait_login()

# 注册消息回调
@wechat.msg_register(ntchat.MT_RECV_TEXT_MSG)
def on_recv_text_msg(wechat_instance: ntchat.WeChat, message):
    data = message["data"]
    from_wxid = data["from_wxid"]
    msg = data["msg"]
    self_wxid = wechat_instance.get_login_info()["wxid"]

    if from_wxid != self_wxid:  # 排除自己发的，否则一直回调
        if msg == "菜单":  # 如果收到的消息是 菜单 则回复以下内容
            wechat_instance.send_text(
                to_wxid=from_wxid,
                content="——————菜单——————\n"
                        "发送 进群 邀请进群"
            )

try:
    while True:
        pass
except KeyboardInterrupt:
    ntchat.exit_()
    sys.exit()