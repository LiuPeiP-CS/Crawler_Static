# -*- coding:utf-8 -*-

from HtmlDownload import HtmlDownload
from HtmlParser import HtmlParser
from StoreData import DataOutput
from URLManager import CcmuManager


class SpiderMan(object):
    def __init__(self):
        # 初始化对象
        self.manager = CcmuManager()
        self.dataoutput = DataOutput()
        self.htmlparser = HtmlParser()
        self.htmldownload = HtmlDownload()
        self.count = 0

    def crawl(self, root_ccmu):
        # 添加对象入口
        self.manager.add_new_ccmu(root_ccmu)
        while self.manager.has_new_ccmu():
            try:
                # 从ccmu管理器获取新的ccmu
                new_ccmu = self.manager.get_new_ccmu()
                # 从ccmu中解析出网页
                new_url = new_ccmu[4]
                # HTML下载器下载网页全部内容
                html = self.htmldownload.download(new_url)
                new_ccmus = self.htmlparser.parser_ccmu(new_ccmu, html)
                if new_ccmus is not None:
                    # 包括获取每类设备的页面网址以及获取每类设备的所有品牌
                    if 'subcategory' in new_url or new_url[-10:] == '/1.html***' or new_url[-10:] == '_1.html***':
                        # 将抽取出来的ccmu添加到ccmu管理器中
                        self.manager.add_new_ccmus(new_ccmus)
                    # 获取每个品牌的所有页面
                    else:
                        if new_ccmus[0] != 'None':
                            # 包含下一页的页面信息
                            self.manager.add_new_ccmu(new_ccmus[0])
                        self.dataoutput.output_json(new_ccmus[1:])
                        self.count = self.count + len(new_ccmus[1:])
                        print('目前已经获得了%s个数据'%self.count)
                """
                # 获取每个设备的详细信息
                if 'shtml' in new_url:
                    data = self.htmlparser.parser_data(new_ccmu, html)
                    if data is not None:
                        # 注意，中关村在线中返回来的是单个数据
                        self.dataoutput.output_json(data)
                        self.count = self.count + 1
                        print('当前在中关村在线获取到了%s个数据' % self.count)

                else:
                    new_ccmus = self.htmlparser.parser_ccmu(new_ccmu, html)
                    # 包括获取每类设备的页面网址以及获取每类设备的所有品牌
                    if 'subcategory' in new_url or new_url[-7:] == '/1.html' or new_url[-7:] == '_1.html':
                        # 将抽取出来的ccmu添加到ccmu管理器中
                        if new_ccmus is not None:
                            self.manager.add_new_ccmus(new_ccmus)
                    # 获取每个品牌的所有页面
                    else:
                        if new_ccmus is not None:
                            if new_ccmus[0] != 'None':
                                # 包含下一页的页面信息
                                self.manager.add_new_ccmus(new_ccmus)
                            else:
                                self.manager.add_new_ccmus(new_ccmus[1:])
                """

            except Exception as e:
                print e
                print "crawler failed"


if __name__ == '__main__':
    spiderman = SpiderMan()
    # 中关村在线网站的主网址
    # CCMU包含：类别1，类别2，品牌，型号，网址
    DecoderCCMU = ("", "", "", "", "http://detail.zol.com.cn/subcategory.html")
    spiderman.crawl(DecoderCCMU)
