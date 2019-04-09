利用代码来计算热门电视剧《都挺好》中人物关系，参考自 [用Python分析《都挺好》中的人物关系](https://mp.weixin.qq.com/s/c3g9qm1wNO_9dWG7YnaA9g)

## 依赖：

````
pip install jieba
pip install gensim
````

## 运行：

````
python analysis.py
````

## model 计算最相似的

````
model.most_similar(u'苏大强', topn=10)
````

content内容前加u，表示unicode编码

## model 计算两个字符串相似度  

````
model.similarity(u'苏大强', u'苏明玉')
````

## 导入model

````
gensim.models.Word2Vec.load(model_path)
````
