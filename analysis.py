# coding:utf-8
# 分析人物关系
import sys
import jieba
import jieba.posseg as pseg
import gensim
import codecs
from gensim.models import word2vec
reload(sys)
sys.setdefaultencoding('utf8')


class Analysis(object):

    def __init__(self):
        super(Analysis, self).__init__()

    # 加载文件内容
    def get_content(self, filename):
        with open(filename, 'r') as f:
            return f.read().replace('\n', '').replace('\t', '').replace(' ', '').strip()

    # 加载用户自定义词典
    def load_user_dict(self, user_dict_path):
        jieba.load_userdict(user_dict_path)
        fp = open(user_dict_path, 'r')
        for line in fp:
            line = line.strip()
            jieba.suggest_freq(line, tune=True)

    # 加载停用词
    def load_stop_words(self, stopwords_path):
        return [line.strip() for line in open(stopwords_path, 'r').readlines()]

    # 分词和词性
    def cut_text_pseg(self, text, cut_file, cut_file_pseg, path_stop_words):
        self.load_user_dict("dict/dict.txt")
        cut_text = pseg.cut(text)

        stop_words = self.load_stop_words(path_stop_words)
        out_cut_text = []
        out_cut_pseg = []

        index = 0
        print cut_text
        for key, pg in cut_text:
            if index % 100 == 0:
                print index
            index += 1
            if key not in stop_words:
                out_cut_text.append(key)
                out_cut_pseg.append(pg)

        fo = codecs.open(cut_file, 'w', 'utf-8')
        fo.write(' '.join(out_cut_text))
        fo.close()

        fo = codecs.open(cut_file_pseg, 'w', 'utf-8')
        fo.write(' '.join(out_cut_pseg))
        fo.close()

    # 根据key获取对应的词性
    def key_to_pseg(self, key, cut_file, cut_pseg):
        index = cut_file.index(key)
        return cut_pseg[index]

    # 训练形成模型
    def train(self, train_file_name, save_model_name):
        # 加载语料
        setences = word2vec.LineSentence(train_file_name)

        model = gensim.models.Word2Vec(setences, min_count=1, size=200)

        model.save(save_model_name)

        model.wv.save_word2vec_format(save_model_name+'.bin', binary=True)

    # 寻找相似的词
    def get_similar(self, content, path_cut_pseg, path_cut_text, model_path):
        psegs = ['nr', 'n']
        cut_pseg, cut_text = [], []
        # 读取词性文件
        with codecs.open(path_cut_pseg, 'r', 'utf-8') as f:
            cut_pseg = f.read().split()

        # 读取分词文件
        with codecs.open(path_cut_text, 'r', 'utf-8') as f:
            cut_text = f.read().split()

        lenK = len(cut_text)

        # 载入模型
        model_1 = gensim.models.Word2Vec.load(model_path)

        y2 = model_1.most_similar(u'%s' % content, topn=lenK)

        print("和%s最相似的词有：" % content)

        y1 = model_1.similarity(u'苏大强', u'苏明玉')
        print '苏大强与苏明玉相似度为 %s' % str(y1)

        cnt = 1
        k = 10
        for item in y2:
            if self.key_to_pseg(item[0], cut_text, cut_pseg) in psegs and len(item[0]) > 1:
                print '%s, %s' % (item[0], item[1])
                cnt += 1
            if cnt > k:
                break

    # 使用用户字典中关键词计算相似度，并且排名
    def get_similar2(self, content, path_cut_pseg, path_cut_text, model_path, user_dict_path):
        psegs = ['nr', 'n']
        cut_pseg, cut_text = [], []
        # 读取词性文件
        with codecs.open(path_cut_pseg, 'r', 'utf-8') as f:
            cut_pseg = f.read().split()

        # 读取分词文件
        with codecs.open(path_cut_text, 'r', 'utf-8') as f:
            cut_text = f.read().split()

        lenK = len(cut_text)

        # 载入模型
        model_1 = gensim.models.Word2Vec.load(model_path)

        fp = open(user_dict_path, 'r')

        user_dict = {}

        for line in fp:
            line = line.strip()
            try:
                user_dict[line] = model_1.similarity(u'%s' % content, u'%s' % line)
            except:
                print 'error %s' % line

        user_dict = sorted(user_dict.items(), key=lambda x:x[1], reverse = True)

        for item in user_dict:
            print '%s 与 %s的相似度为：%.6f' % (content, item[0], item[1])


    def main(self):
        content = self.get_content("都挺好.txt")
        self.cut_text_pseg(content, 'results/cutfile.txt', 'results/cutpseg.txt', 'dict/stopwords.txt')

        self.train('results/cutfile.txt','results/model')

        personame = '苏大强'

        self.get_similar(personame, "results/cutpseg.txt", "results/cutfile.txt", 'results/model')

        print '-----------------'

        self.get_similar2(personame, "results/cutpseg.txt", "results/cutfile.txt", 'results/model', "dict/dict.txt")

# main
if __name__ == '__main__':
    Analysis().main()