# 从gensim导入词向量加载工具
from gensim.models import KeyedVectors

# 加载预训练Word2Vec模型（GoogleNews-vectors-negative300）
pretrained_model_path = r'E:\shi yan dai ma\Word2vec\archive\GoogleNews-vectors-negative300.bin'
# binary=True表示模型为二进制格式，是该预训练模型的固定参数
model = KeyedVectors.load_word2vec_format(pretrained_model_path, binary=True)

# 1. 计算两个词语的相似性（以cat和dog为例）
word1 = 'cat'
word2 = 'dog'
similarity = model.similarity(word1, word2)
# 保留4位小数打印相似性结果
print(f"The similarity between '{word1}' and '{word2}' is: {similarity:.4f}")

# 2. 词语类比推理（以king:man :: woman:? 为例）
word_a = 'king'
word_b = 'man'
word_c = 'woman'
# positive为正样本词，negative为负样本词，推理逻辑：king - man + woman
result = model.most_similar(positive=[word_b, word_c], negative=[word_a])
# 输出类比推理的最匹配结果
print(f"The result for the analogy '{word_a}:{word_b}::{word_c}:' is {result[0][0]}")
# 导入所需库
import jieba
import re
from gensim.models import Word2Vec

# 1. 定义文本处理函数：清洗+分词，转换为模型可识别的句子列表
def read_chinese_file_to_sentences(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        # 清洗文本：去除非中文字符、空白符、换行符（修正文档中错误的正则）
        text = re.sub(r'[^\u4e00-\u9fff]', '', text)  # 只保留中文字符
        text = re.sub(r'\s+', '', text)  # 去除所有空白
        text = re.sub(r'\n', '', text)   # 去除换行
        # 中文分词
        words = jieba.cut(text)
        # 转换为[['词1','词2'],...]格式（模型要求的输入格式）
        sentences = [list(words)]
    return sentences

# 2. 读取语料并处理
file_path = r'E:\shi yan dai ma\Word2vec\sanguoyanyi.txt'  # 你的语料路径
sentences = read_chinese_file_to_sentences(file_path)

# 3. 训练Word2Vec模型（核心参数配置）
model = Word2Vec(
    sentences=sentences,  # 分词后的句子列表
    vector_size=100,      # 词向量维度，可调整（如50/200/300）
    window=5,             # 上下文窗口大小：每个词考虑前后5个词
    min_count=1,          # 最小词频：出现次数≥1的词才保留
    workers=4             # 多线程训练，根据电脑核数调整
)

# 4. 保存模型（后续可直接加载，无需重复训练）
model.save("sanguo_w2v.model")
print("模型训练完成并保存为sanguo_w2v.model")

# 5. 加载已训练的模型
loaded_model = Word2Vec.load("sanguo_w2v.model")

# 6. 计算与指定词最相似的词（默认返回10个）
similar_words = loaded_model.wv.most_similar('刘备')
print("\n与刘备最相似的词：")
for word, sim in similar_words:
    print(f"{word}: {sim:.4f}")
    
similar_words = loaded_model.wv.most_similar('曹操')
print("\n与曹操最相似的词：")
for word, sim in similar_words:
    print(f"{word}: {sim:.4f}")

# 7. 中文类比推理（公式：刘备 - 关羽 + 张飞 = ?）
analogy_words = loaded_model.wv.most_similar(
    positive=['刘备', '张飞'],  # 加词
    negative=['关羽'],          # 减词
    topn=10                     # 返回前10个结果
)
print("\n类比推理（刘备-关羽+张飞）结果：")
for word, sim in analogy_words:
    print(f"{word}: {sim:.4f}")