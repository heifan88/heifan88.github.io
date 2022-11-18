import urllib.request as urlrequest
import json
import jsonpath
import time
import os

# 设置获取的网址
url_visit = 'http://api.vipmisss.com:81/xcdsw/json.txt'

# 请求网页源码
crawl_content_pt = urlrequest.urlopen(url_visit).read()

# 使用UTF8编码为JSON格式
json_content_pt = json.loads(crawl_content_pt.decode('utf8'))

# 获取平台名称，返回平台名称列表
title = jsonpath.jsonpath(json_content_pt,'$..title')

# 获取平台地址，返回列表
address = jsonpath.jsonpath(json_content_pt,'$..address')

# 创建文件写入操作
# 以UTF-8编码，覆盖方式写入平台信息
f_pt = open(os.getcwd() + '\pingtai_list.txt','w+',encoding='utf-8')

# 以UTF-8编码，追加方式写入所有平台主播信息
f_zb = open(os.getcwd() + '\zhubo_list.txt','w+',encoding='utf-8')

# 循环写入平台文件信息并打开下一级链接
for i in range(len(address)):
    pingtaiAddress = "http://api.vipmisss.com:81/xcdsw/"+address[i]
    # 写入平台信息
    f_pt.write(title[i]+','+pingtaiAddress+'\n')
    # time.sleep(3)
    # 打开下一级连接
    print("平台链接："+pingtaiAddress)
    crawl_content_zb = urlrequest.urlopen(pingtaiAddress,timeout=10).read()
    # 有些链接返回空，无法解析，需进行异常处理
    try:
        json_content_zb = json.loads(crawl_content_zb.decode('utf8'))
    except:
        print("平台："+title[i]+"编码失败！")
    else:
        # 获取主播名称，返回列表
        title_zb = jsonpath.jsonpath(json_content_zb,'$..title')
        # 获取主播地址，返回列表
        address_zb = jsonpath.jsonpath(json_content_zb,'$..address')
        # 写入平台信息信息用来区分
        f_zb.write("平台名称《" + title[i]+'》,'+address[i]+'\n')
        # 循环写入主播信息
        for j in range(len(address_zb)):
            f_zb.write(title_zb[j]+','+address_zb[j]+'\n')
        # print("平台："+title[i]+"写入成功！")

print("完成")
f_zb.close()
f_pt.close()