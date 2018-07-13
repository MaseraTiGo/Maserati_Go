from pydub import AudioSegment
batman = AudioSegment.from_file("batman2.wma", "wma")
HALFHOUR = 1000*60*30

for i in range(len(batman)/HALFHOUR):
    batman[i*HALFHOUR: (i+1)*HALFHOUR].export('\s.mp3', format='mp3')

#循环目录下所有文件
# for each in os.listdir('.'):
    # filename = re.findall(r"(.*?)\.mp3", each) # 取出.mp3后缀的文件名
    # if filename:
        # filename[0] += '.mp3'
        # mp3 = AudioSegment.from_mp3(filename[0]) # 打开mp3文件
        # mp3[17*1000+500:].export(filename[0], format="mp3") # 切割前17.5秒并覆盖保存
    