# coding:utf-8
import requests, re

import sys  
import os
import MySQLdb
import json
import datetime
reload(sys)  
class Post_test():
    rootDir = '/data/dearMrLei/data/'
    download_url = 'http://www.shclearing.com/wcm/shch/pages/client/download/download.jsp'
    #获取待下载的pdf数据
    def main(self):
        for i in range(1,2):
            items = self.get_item(20)
            for item in items:
                news_id = item[0]
                url = item[1]
                filename = item[2]
                #设置保存路径
                path = self.rootDir + self.set_path(url,filename)
                #执行下载操作
                sys.setdefaultencoding('utf8')   
                self.save_file(filename,path)
                #下载成功后，更新数据状态
                self.update_item(news_id, path)
    
    def get_conn(self):
        conn=MySQLdb.connect(host="localhost",port=3306,user="root",passwd="KeYpZrZx",db="scrapy",charset="utf8")
        return conn 

    #从数据库中获取待下载的文件信息
    def get_item(self, num):
        conn = self.get_conn()
        cursor = conn.cursor()
        sql = "select id,url,pdf_filename "
        sql = sql + "from shclearing_news where is_download=0 order by id asc limit "+str(num)
        n = cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

     #设置文件保存的相对路径
    def set_path(self, url, filename):
        tail = 'default'
        m = re.match(r".*?/t(\d{4})(\d{2})(\d{2})_(\d+).*?", url)
        if m:
            tail = m.group(1) + "/" + m.group(2) + "/" + m.group(3) + "/" + m.group(4) + "/"                 
            fileDir = 'shclearing/'+tail
            relative_path = fileDir+filename
            if not os.path.exists(self.rootDir + fileDir):
                os.makedirs(self.rootDir + fileDir)
        return relative_path

    # 下载文件
    def save_file(self,filename,path):
        #文件是否存在
        is_exist = os.path.exists(path) 
        if not is_exist:
            #若不存在，调用接口下载文件
            session = requests.Session()
            params = {'FileName': filename, 'DownName': filename}
            r = session.post(self.download_url, data=params)
            if r.status_code == 200:
                with open(path, 'wb') as f:
                     f.write(r.content)

    # 文件下载成功后，更新数据库状态
    def update_item(self,news_id,path):
        conn = self.get_conn() 
        cursor = conn.cursor()
        update_time = str(datetime.datetime.now())
        sql = "update shclearing_news set is_download=1,pdf_path='"+path + "',update_time='"+update_time+"'"
        sql = sql + " where id="+str(news_id)
        print(sql)
        try:
        # 执行SQL语句
            cursor.execute(sql)
            # 提交到数据库执行
            conn.commit()
        except:
        # 发生错误时回滚
            conn.rollback()
        cursor.close()
        
aa = Post_test()
aa.main()
