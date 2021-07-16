# -*- coding:utf-8 -*-

import urlparse

from bs4 import BeautifulSoup


class HtmlParser(object):

    def parser_ccmu(self, ccmu, html_cont):

        """
        :param ccmu: 下载页面的元组
        :param html_cont: 下载的网页内容
        :return: 返回数据
        """

        if ccmu is None or html_cont is None:
            return
        # soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        soup = BeautifulSoup(html_cont, 'html.parser')
        new_ccmus = self.get_new_ccmus(ccmu, soup)
        return new_ccmus

    def get_new_ccmus(self, ccmu, soup):

        """
        :param ccmu:下载页面的元组
        :param soup: 传递参数soup
        :return: 返回的新的URL集合
        """

        new_ccmus = []
        page_url = ccmu[4]
        if 'subcategory' in page_url:
            # 这是分类根网页
            for device_class in soup.find('div', class_='wrapper mod-cate-box' ).find_all('ul', class_='clearfix'):
                class_first = device_class.find('li', class_='first')
                if class_first is not None:
                    # 设备类别T1级别
                    device_class_T1 = class_first.find('a').get_text().strip('：')
                    print(device_class_T1)
                    for a in device_class.find_all('a'):
                        device_class_T2 = a.get_text()
                        new_url = a.get('href')
                        new_url_split = new_url.split('/')
                        if len(new_url_split) > 2:
                            # 增加页面设置
                            new_url_tail = '1.html***'
                            if new_url_split[len(new_url_split) - 1] == '':
                                # 或者new_url[-1] == '/'
                                new_url = new_url + new_url_tail
                            else:
                                new_url = new_url[:-6] + new_url_tail
                            # 拼接成为完整的URL链接
                            first_page_url = 'http://detail.zol.com.cn' + new_url
                            # 构造三元组（类型1，类型2，URL）
                            new_ccmu = (device_class_T1, device_class_T2, '', '', first_page_url)
                            # 链接集合中补充进入新网址
                            new_ccmus.append(new_ccmu)
            print("—————————————————已处理完初始页面的所有大类———————————————")

        # 获取每类设备的所有品牌及每个品牌第一页
        elif page_url[-10:] == '/1.html***' or page_url[-10:] == '_1.html***':
            Brand_All_1 = soup.find('div', id = "J_BrandAll")
            Brand_All_2 = soup.find('div', id = "J_ParamBrand")
            if Brand_All_1 is not None:
                for a in Brand_All_1.find_all('a'):
                    href = a.get('href')
                    device_name = a.get_text()
                    first_page_url = 'http://detail.zol.com.cn' + href
                    new_ccmu = (ccmu[0], ccmu[1], device_name, '', first_page_url)
                    new_ccmus.append(new_ccmu)
                print("*************已获得%s类设备的所有品牌*************"%ccmu[1])

            elif Brand_All_2 is not None:
                for a in Brand_All_2.find('a'):
                    href = a.get('href')
                    device_name = a.get_text()
                    first_page_url = 'http://detail.zol.com.cn' + href
                    new_ccmu = (ccmu[0], ccmu[1], device_name, '', first_page_url)
                    new_ccmus.append(new_ccmu)
                print("##############已获得%s类设备的所有品牌##############" % ccmu[1])

        else:
            # 处理简图
            # 获取下一页
            next = soup.find('a', class_ = 'small-page-next')
            if next is not None:
                href = next.get('href')
                next_page_url = 'http://detail.zol.com.cn' + href
                new_ccmu = (ccmu[0], ccmu[1], ccmu[2], '', next_page_url)
                new_ccmus.append(new_ccmu)
                print('****************下一页****************')
            else:
                new_ccmus.append('None')
            # 简图页面中每件商品的具体链接，简图有两种排布方式
            Content1 = soup.find(class_='content').find(class_="pic-mode-box")
            Content2 = soup.find(class_='content').find(class_="list-box")
            if Content1 is not None:
                for li in Content1.find('ul', id = 'J_PicMode').find_all('li'):
                    # 获取到了设备的具体地址
                    # print('Content1 get')
                    h3 = li.find('h3')
                    if h3 is not None:
                        a = h3.find('a')
                        if a is not None:
                            device_url = a.get('href')
                            device_full_url = 'http://detail.zol.com.cn' + device_url
                            device_detail = a.get_text()
                            span = a.find('span')
                            if span is not None:
                                span_text = span.get_text()
                                device_detail = device_detail.replace(span_text,'').strip()
                            new_ccmu = (ccmu[0], ccmu[1], ccmu[2], device_detail, device_full_url)
                            new_ccmus.append(new_ccmu)
                print("##############已获得该页面的所有设备信息##############")

            elif Content2 is not None:
                for pi in Content2.find_all('div',class_ = 'pro-intro'):
                    # print('Content2 get')
                    h3 = pi.find('h3')
                    if h3 is not None:
                        a = h3.find('a')
                        if a is not None:
                            device_url = a.get('href')
                            device_full_url = 'http://detail.zol.com.cn' + device_url
                            device_detail = a.get_text()
                            new_ccmu = (ccmu[0], ccmu[1], ccmu[2], device_detail, device_full_url)
                            new_ccmus.append(new_ccmu)
                print("****************已获得该页面的所有设备信息****************")
            else:
                return
        return new_ccmus

    '''
    def parser_data(self, ccmu, html_cont):
        """
        :param ccmu: 下载页面的URL
        :param html_cont: 下载的网页内容
        :return: 返回数据
        """
        if ccmu is None or html_cont is None:
            return
        # soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        # 只有满足最后的条件时，才会进行数据爬取
        soup = BeautifulSoup(html_cont, 'html.parser')
        return self.get_new_data(ccmu, soup)

    def get_new_data(self, ccmu, soup):
        """
        抽取有效数据
        :param ccmu: 类别，类别，属性，（具体的）类别网址
        :param soup: soup
        :return: 返回获取到的数据
        """
        # 获取设备的详细信息
        if soup.find("h1", class_="product-model__name") is not None:
            device_details = soup.find("h1", class_="product-model__name").get_text()
            detailed_ccmu = (ccmu[0], ccmu[1], ccmu[2], device_details, ccmu[4])
            return detailed_ccmu
        return
    '''
