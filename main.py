"""
照片处理工具
1.排序照片
2.根据年份和月份存放
3.去重复照片
"""
import time
import os,shutil
import datetime
import filecmp
import exifread
import configparser


def mkdir(path):
    """创建文件夹"""
    # 引入模块
    import os

    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)

        print("[+]" + path + ' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print("[+]" + path + ' 已存在')
        return False


def TimeStampToTime(timestamp):
    """时间转换"""
    timeStruct = time.localtime(timestamp)
    return timeStruct

def getFileTime(src_path):
    """获取文件创建时间"""
    statinfo = os.stat(src_path)
    dt = TimeStampToTime(statinfo.st_mtime)
    return dt

def moveToNewFilePath(src_path,tar_path,fileName ,fo):
    #dt = getFileTime(src_path)
    dt = getFileDate(src_path)


    folder_name = dt
    dst_path = tar_path + folder_name
    mkdir(dst_path)
    file_path =  dst_path + "\\" + fileName
    shutil.move(src_path, file_path)

    #, time.strftime('%Y-%m-%d %H:%M:%S', dt)
    fo.write("%s --> %s  \n" % (src_path,file_path))
    print("%s --> %s" % (src_path,file_path))


    return file_path

def findAllFile(base):
    """获取文件"""
    list = []
    for path, d, filelist in base:

        for filename in filelist:
            filenameEnd = os.path.splitext(filename)[-1]
            if filenameEnd == '.jpg' or filenameEnd=='.png' or filenameEnd=='.gif' or filenameEnd=='.JPG' or filenameEnd=='.jpeg':
                #print(os.path.join(path, filename))
                list.append(os.path.join(path, filename))

    return list

def getFileDate(src_path):
     f = open(src_path,'rb')
     tags = exifread.process_file(f)
     dateTime_p = None
     try:
        if tags.get('Image DateTime') != None:
            dt = tags.get('Image DateTime')
            dt2 = datetime.datetime.strptime(str(dt),'%Y:%m:%d %H:%M:%S')
            dateTime_p = dt2.strftime("%Y-%m")
        else:
            dt = getFileTime(src_path)
            dateTime_p = time.strftime('%Y', dt) + "-" + time.strftime('%m', dt)
     except Exception as e:
        print(e)
        dt = getFileTime(src_path)
        dateTime_p = time.strftime('%Y', dt) + "-" + time.strftime('%m', dt)
     
    
     
     f.close()
     return dateTime_p
     
if __name__ == '__main__':

    config = configparser.ConfigParser()  # 类实例化

    # 定义文件路径
    path = 'config.ini'

    config.read(path, encoding="utf-8")  # python3

    base_path = config.get('db', 'base_path')
    target_path = config.get('db', 'target_path')

    print("需要整理的文件目录:%s" %base_path)
    print("归档目录:%s" %target_path)


    #需要整理的文件目录
    #base_path = "V:\\备份文件\\手机文件备份\\"

    #归档目录
    #target_path = "Y:\\图片资源\\图片\\手机照片\\相册\\"

    time_start = time.time()

    allFiles = findAllFile(os.walk(base_path))

    dt = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))

    fo = open("log\\log-"+dt+".txt","w",encoding="utf-8")

    fo.write("================================================================" + '\n')

    fo.write("当前搜索到文件数量:%s \n" % len(allFiles))
    print("当前搜索到文件数量:%s \n" % len(allFiles))

    fo.write("================================================================" + '\n')

    for item in allFiles:
        print(item)
        file_name = item.split("\\")[-1]
        moveToNewFilePath(item,target_path, file_name , fo)

    fo.write("================================================================" + '\n')

    time_end = time.time()
    fo.write("已经处理文件:%s \n" % len(allFiles))
    print("已经处理文件:%s \n" % len(allFiles))
    fo.write("耗时: %.03f seconds \n" % (time_end-time_start))
    print("耗时: %.03f seconds \n" % (time_end-time_start))

    fo.write("================================================================" + '\n')

    fo.close()
