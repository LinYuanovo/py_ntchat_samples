# 获取二维码中的url

import sys
import os
import time
import ntchat
from pyzbar.pyzbar import decode
from PIL import Image

wechat = ntchat.WeChat()

# 打开pc微信, smart: 是否管理已经登录的微信
wechat.open(smart=True)

wechat.wait_login()

"""
微信图片解密dat格式
代码来自CSDN博主：推广策划师阿宝
文章链接：https://blog.csdn.net/weixin_42360467/article/details/112521463
"""
def imageDecode(f):
    try:
        with open(f, "rb") as dat_read:
            first = dat_read.read(1)
            second = dat_read.read(1)
            if ord(first) ^ 0xff == ord(second) ^ 0xd8 :
                # jpeg
                pwd = ord(first) ^ 0xff
                fmt = ".jpg"
            elif ord(first) ^ 0x89 == ord(second) ^ 0x50 :
                # png
                pwd = ord(first) ^ 0x89
                fmt = ".png"
            elif ord(first) ^ 0x47 == ord(second) ^ 0x49 :
                # gif
                pwd = ord(first) ^ 0x47
                fmt = ".gif"
            else:
                print("未知文件格式，跳过！")
                return
        with open(f, "rb") as dat_read:
            out = f.replace(".dat", "") + fmt
            with open(out, "wb") as png_write:
                for now in dat_read:
                    for nowByte in now:
                        newByte = nowByte ^ pwd
                        png_write.write(bytes([newByte]))
            return out
    except Exception as e:
        print(e)

# 注册消息回调
@wechat.msg_register(ntchat.MT_RECV_IMAGE_MSG)
def on_recv_image_msg(wechat_instance: ntchat.WeChat, message):
    data = message["data"]
    from_wxid = data["from_wxid"]
    self_wxid = wechat_instance.get_login_info()["wxid"]

    if from_wxid != self_wxid:  # 排除自己发的，否则一直回调
        image_path = data["image"]
        time.sleep(5)  # 休眠5秒，太快读取不到
        out_path = imageDecode(image_path)
        os.remove(image_path)
        # 将所得二维码转成url
        url = decode(Image.open(out_path))[0].data.decode("utf-8")
        wechat.send_text(to_wxid=from_wxid, content=f"{url}")

try:
    while True:
        pass
except KeyboardInterrupt:
    ntchat.exit_()
    sys.exit()
