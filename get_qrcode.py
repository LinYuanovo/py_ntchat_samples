# 发送url所转换的二维码

import sys
import ntchat
import os
import time
import qrcode

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
        if msg.startswith("二维码"):  # 如果收到的消息是 二维码+链接（不用加空格） 则发送一张二维码
            # 示例：二维码https://www.baidu.com
            url = msg.replace("二维码", "")
            # url转为二维码
            img = qrcode.make(url)
            img.save("qrcode.png")
            # 获取当前工作路径，以便发送后删除
            path = os.path.abspath(os.path.dirname(__file__))
            wechat_instance.send_image(to_wxid=from_wxid, file_path="{}\qrcode.png".format(path))
            time.sleep(5)
            os.remove("qrcode.png")

try:
    while True:
        pass
except KeyboardInterrupt:
    ntchat.exit_()
    sys.exit()