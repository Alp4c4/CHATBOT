import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


from wordcloud import WordCloud, STOPWORDS
from pythainlp import word_tokenize
from pythainlp.corpus.common import thai_stopwords
from pythainlp import word_tokenize
df = pd.read_csv('sen.txt', sep='\t', names=['text', 'sentiment'], header=None)
thai_stopwords=list(thai_stopwords())
def text_process(text):
    final = "".join(u for u in text if u not in ("?", ".", ";", ":", "!", '"', "ๆ", "ฯ"))
    final = word_tokenize(final)
    final = " ".join(word for word in final)
    final = " ".join(word for word in final.split() 
                     if word.lower not in thai_stopwords)
    return final
df['text_tokens'] = df['text'].apply(text_process)
df

df_pos = df[df['sentiment'] == 'pos']
pos_word_all = " ".join(text for text in df_pos['text_tokens'])
reg = r"[ก-๙a-zA-Z']+"
fp = 'THSarabunNew.ttf'
wordcloud = WordCloud(stopwords=thai_stopwords, background_color = 'white', max_words=2000, height = 2000, width=4000, font_path=fp, regexp=reg).generate(pos_word_all)
plt.figure(figsize = (16,8))
plt.imshow(wordcloud)
plt.axis('off')
plt.show()