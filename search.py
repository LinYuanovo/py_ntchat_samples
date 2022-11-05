# 查找微信好友的wxid

import sys
import ntchat
import re

wechat = ntchat.WeChat()

# 打开pc微信, smart: 是否管理已经登录的微信
wechat.open(smart=True)

wechat.wait_login()

"""
参数（查找时可以直接替换）
account 微信号
nickname 昵称
remark 备注
wxid 微信id（发送消息用的）
"""

"""根据微信名查找wxid"""
# 1. 精确查找，仅查找微信好友
contacts = wechat.get_contacts()
for contact in contacts:
    if contact["nickname"] == "小杨":  # 精确查找微信名为小杨的好友
        print(contact)
        print(contact["nickname"], contact["wxid"])
# 2. 模糊查找，查找微信好友和群聊
contacts = wechat.search_contacts(nickname="小")  # 模糊查找包含昵称包含小的微信好友
for contact in contacts:
    print(contact["nickname"], contact["remark"], contact["wxid"])

try:
    while True:
        pass
except KeyboardInterrupt:
    ntchat.exit_()
    sys.exit()