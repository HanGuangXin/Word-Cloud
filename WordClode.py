# - * - coding: utf - 8 -*-
#
# 作者：田丰(FontTian)
# 创建时间:'2017/5/23'
# 邮箱：fonttian@163.com
# CSDN：http://blog.csdn.net/fontthrone
# 修改者：韩广鑫
# 修改内容：
#   1. python 2 到 python 3
#   2. 修复词云中词语重复的现象
from os import path
from scipy.misc import imread
import matplotlib.pyplot as plt
import jieba
# jieba.load_userdict("txt\userdict.txt")
# 添加用户词库为主词典,原词典变为非主词典
from wordcloud import WordCloud, ImageColorGenerator

# 获取当前文件路径
# __file__ 为当前文件, 在ide中运行此行会报错,可改为
d = path.dirname('.')           # 获取当前文件路径
# d = path.dirname(__file__)

stopwords = {}                  # 初始化stopwords字典
isCN = 1                                    # 默认启用中文分词
back_coloring_path = "dressgirl.png"        # 设置背景图片文件名
text_path = 'data.txt'                      # 设置要分析的文本路径
font_path = 'D:\Fonts\simkai.ttf'           # 为matplotlib设置中文字体路径（楷体）
stopwords_path = 'stopwords.txt'            # 停用词文本路径
imgname1 = "WordCloudDefautColors.png"              # 保存的图片名字1(只按照背景图片形状)
imgname2 = "WordCloudColorsByImg.png"               # 保存的图片名字2(颜色按照背景图片颜色布局生成)

# 在结巴的词库中添加新词，即新词被识别为整词
my_words_list = ['廖雪峰','深度学习','崇天老师','开源项目','学习笔记','Hyperspectral-Classification',
                 'paper reading']

back_coloring = imread(path.join(d, back_coloring_path))        # 读取背景图片

# 设置词云属性
wc = WordCloud(font_path=font_path,             # 设置字体
               collocations=False,              # 不统计搭配词，从而避免词语重复
               background_color="white",        # 背景颜色
               max_words=2000,                  # 词云显示的最大词数
               mask=back_coloring,              # 设置背景图片
               max_font_size=100,               # 字体最大值
               random_state=42,
               width=2000, height=1720, margin=2,    # 设置图片默认的大小，但是如果使用背景图片的话，那么保存的图片大小将
                                                    # 会按照其大小保存，margin为词语边缘距离
               )

# 添加自己的分词词库 到 jieba分词词库
def add_word(list):
    for items in list:
        jieba.add_word(items)

add_word(my_words_list)

# 读取待处理的文本文件
text = open(path.join(d, text_path),'rb').read()    # python 2 to python 3

def jiebaclearText(text):
    mywordlist = []
    seg_list = jieba.cut(text, cut_all=False)
    liststr="/ ".join(seg_list)
    f_stop = open(stopwords_path,'rb')              # python 2 to python 3
    try:
        # 停止词文件的读取和格式转换
        f_stop_text = f_stop.read( )
        f_stop_text = str(f_stop_text)              # python 2 to python 3
    finally:
        f_stop.close( )                             # 停止词文件读取结束
    f_stop_seg_list=f_stop_text.split('\n')
    for myword in liststr.split('/'):
        if not(myword.strip() in f_stop_seg_list) and len(myword.strip())>1:
            mywordlist.append(myword)
    return ''.join(mywordlist)

if isCN:
    text = jiebaclearText(text)

# 生成词云, 可以用generate输入全部文本(wordcloud对中文分词支持不好,建议启用中文分词),
# 也可以我们计算好词频后使用generate_from_frequencies函数
wc.generate(text)
# wc.generate_from_frequencies(txt_freq)
# txt_freq例子为[('词a', 100),('词b', 90),('词c', 80)]



# 显示图片
plt.figure()
plt.imshow(wc)
plt.axis("off")
plt.show()
# 保存图片
wc.to_file(path.join(d, imgname1))

# 从背景图片生成颜色值，绘制背景图片为颜色的图片
image_colors = ImageColorGenerator(back_coloring)

plt.imshow(wc.recolor(color_func=image_colors))
plt.axis("off")
plt.figure()
plt.imshow(back_coloring, cmap=plt.cm.gray)
plt.axis("off")
plt.show()
# 保存图片
wc.to_file(path.join(d, imgname2))
