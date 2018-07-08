#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# @Author:GoldsNow(891699904@qq.com)
# date: 2018-07-08 22:43:44

def init():
    uud_file = 'uud_base.txt'
    fp_out = open(uud_file,'wb')
    fp_out.write('\xFF\xFE\x46\x00\x6F\x00\x72\x00\x6D\x00\x61\x00\x74\x00\x56\x00\x65\x00\x72\x00\x73\x00\x69\x00\x6F\x00\x6E\x00\x3D\x00\x76\x00\x31\x00\x2E\x00\x30\x00\x0A\x00\x0A\x00')
    fp_py = open('sgim_py.bin','rb')
    fp_od = open('sgim_gd_usr_od.bin','rb')
    checkfile(fp_od)
    return fp_out,fp_py,fp_od
   
def end(fp_py, fp_od, fp_out):
    fp_py.close()
    fp_od.close()
    fp_out.close()

def checkfile(fp):
    if fp.read(4) == "SGOU":
        pass
    else:
        print "sgim_gd_usr_od.bin check fail!"
        exit()
   
def seek_py(fp,offset):
    fp.seek((offset+1)*16)
    return fp.read(16).replace('\x00\x00','')

def ReadInt(fp,offset):
    fp.seek(offset)
    return int(fp.read(4)[::-1].encode('hex'),16)
    
def ReadShort(fp,offset):
    fp.seek(offset)
    return int(fp.read(2)[::-1].encode('hex'),16)
    
def Asc2Unicode(data):
    return "".join(t + '\x00' for t in "%d"%(data))
    
def GetPinYin(fp_od,fp_py,offset,count):
    pinyin = ''
    for i in range(count):
        tmp = ReadShort(fp_od,offset)
        if tmp > 0x19c:
            pinyin += '[\x00'+chr(tmp-0x19c-1+ord('a'))+'\x00]\x00'
        else:
            pinyin += '[\x00'+seek_py(fp_py,tmp)+']\x00'
        offset = offset + 2    
    return pinyin

def ReadChinese(fp,offset,count):
    fp.seek(offset)
    return fp.read(count)
    
def main():
    fp_out,fp_py,fp_od = init()
    count = ReadInt(fp_od,0x38)
    offset_base = ReadInt(fp_od,0x3c)
    print 'count  = ',count
    print 'offset = ',offset_base
    for i in range(count): 
        offset = offset_base + ReadInt(fp_od, 0x80 + i * 4 + 4)
        wordcount = ReadShort(fp_od, offset)
        wordlen =  ReadShort(fp_od, offset + 2 ) / 2
        wordpingyin = GetPinYin(fp_od, fp_py, offset + 4, wordlen)
        wordzhongwen = ReadChinese(fp_od, offset + 4 + wordlen * 2 + 4, wordlen * 2)
        wordline = wordpingyin + '\x09\x00' + wordzhongwen + '\x09\x00' + Asc2Unicode(wordcount)+'\x0a\x00'
        fp_out.write(wordline)
    end(fp_py, fp_od, fp_out)


if __name__ == '__main__':
    main()