#! /usr/bin/python
# -*-encoding:utf-8 -*-

class update:

    def readTxt(self):
        f = open("info.txt",'r')
        lines = f.readlines()
        i = 0
        for line in lines:
            i = i + 1
            print(i)
            if i == 100:
                print(line[:-3])



aa = update()
aa.readTxt()
