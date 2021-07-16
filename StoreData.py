# -*- coding:utf-8 -*-
import codecs
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class DataOutput(object):

    def output_json(self, datas):
        fout = codecs.open('/home/liupei/Files/ZOL_Data.json','a+',encoding = 'utf-8')
        for data in datas:
            fout.write('功能类别: %s,' % data[0])
            fout.write('设备类别: %s,' % data[1])
            fout.write('设备品牌: %s,' % data[2])
            fout.write('设备详情: %s,' % data[3])
            fout.write('设备网址: %s\n' % data[4])
            print('%s %s %s %s %s\n' % (data[0], data[1], data[2], data[3], data[4]))
        fout.close()