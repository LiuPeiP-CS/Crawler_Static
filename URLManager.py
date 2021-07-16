# -*- coding:utf-8 -*-


class CcmuManager(object):
    def __init__(self):
        self.new_ccmus = set() # 未爬取的ccmu集合

    def has_new_ccmu(self):
        """
        判断是否有未爬取的ccmu信息
        :return:
        """
        return self.new_ccmus_size() != 0

    def get_new_ccmu(self):
        """
        获取一个暂未爬取的URL
        :return:
        """
        new_ccmu = self.new_ccmus.pop()
        return new_ccmu

    def add_new_ccmu(self, ccmu):
        """
        将新的ccmu添加到未爬取的ccmu集合
        :param ccmu单个ccmu
        :return:
        """
        if ccmu is None:
            return
        if ccmu not in self.new_ccmus:
            # 既不是未爬取的列表中，也不是已经爬取的列表中
            self.new_ccmus.add(ccmu)


    def add_new_ccmus(self, ccmus):
        """
        将新的多个ccmus添加到未爬取的ccmu列表中
        :param ccmus: ccmu集合
        :return:
        """
        if ccmus is None or len(ccmus) == 0:
            return
        for ccmu in ccmus:
            self.add_new_ccmu(ccmu)

    def new_ccmus_size(self):
        """
        获取未爬取的ccmu集合的大小
        :return:
        """
        return len(self.new_ccmus)