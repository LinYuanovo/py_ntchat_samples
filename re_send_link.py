# 转发别人发过来的链接

import sys
import ntchat
import re

wechat = ntchat.WeChat()

# 打开pc微信, smart: 是否管理已经登录的微信
wechat.open(smart=True)

wechat.wait_login()

# 消息回调
@wechat.msg_register(ntchat.MT_RECV_LINK_MSG)
def on_recv_link_msg(wechat_instance: ntchat.WeChat, message):
    data = message["data"]
    from_wxid = data["from_wxid"]
    self_wxid = wechat_instance.get_login_info()["wxid"]
    temp_data = data["raw_msg"]
    url = re.findall(r'<url>(.*?)</url>', temp_data)[0]  # 正则匹配出链接
    if from_wxid != self_wxid:  # 排除自己发的链接，否则一直回调
        # 转发给想转发的人
        wechat.send_link_card(to_wxid="wxid_xxx", title="标题", desc="描述", url=f"{url}", image_url="图片链接（可不填）")

try:
    while True:
        pass
except KeyboardInterrupt:
    ntchat.exit_()
    sys.exit()