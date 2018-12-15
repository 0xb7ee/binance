# -*- coding:utf-8 -*-
import StringIO
import gzip
import re
import urllib2

'''
gzip 解压
'''


def gzip_decompress(url, csv_filename):
    req = urllib2.Request(url)
    try:
        response = urllib2.urlopen(req)
        data = response.read()
    except:
        return

    header = response.headers.dict
    file_real_names = re.findall("(?<=filename=\").*?(?=.zip)", response.headers.dict["content-disposition"])
    file_real_name = "\\" + file_real_names[0]
    if 'content-type' in header and 'application/vnd.ms-excel' == header['content-type']:
        data = StringIO.StringIO(data)
        gz = gzip.GzipFile(fileobj=data)
        data = gz.read().decode("gbk")
        f = open(csv_filename + file_real_name, "w+")
        # windows版本下面的utf-8改为gbk
        f.write(data.encode("utf8"))
        gz.close()


if __name__ == "__main__":
    url = "http://api.agent.sogou.com/DownloadReport.report?accountId=18680688&fid=panama_default_class_286cb298-f310-47fa-94af-08a6dcd517e0_e2759c91a55e97edda7c3f00e40dcf4a"
    filename = "D:\out"
    gzip_decompress(url, filename)
