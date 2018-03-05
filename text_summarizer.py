#import libraries needed for this program 
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from string import punctuation
from heapq import nlargest
import nltk
from bs4 import BeautifulSoup
import requests
#This class is used for summarizing the given text
class FrequencySummarizer:
  def __init__(self, min_cut=0.1, max_cut=0.9):
    self._min_cut = min_cut
    self._max_cut = max_cut 
    self._stopwords = set(stopwords.words('english') + list(punctuation))

  def _compute_frequencies(self, word_sent):
    freq = defaultdict(int)
    for s in word_sent:
      for word in s:
        if word not in self._stopwords:
          freq[word] += 1
    # frequencies normalization and fitering
    m = float(max(freq.values()))
    for w in freq.keys():
      freq[w] = freq[w]/m
      if freq[w] >= self._max_cut or freq[w] <= self._min_cut:
        del freq[w]
    return freq
#Return a list of n sentences which represent the summary of text.
  def summarize(self, text, n):
    sents = sent_tokenize(text)
    assert n <= len(sents)
    word_sent = [word_tokenize(s.lower()) for s in sents]
    self._freq = self._compute_frequencies(word_sent)
    ranking = defaultdict(int)
    for i,sent in enumerate(word_sent):
      for w in sent:
        if w in self._freq:
          ranking[i] += self._freq[w]
    sents_idx = self._rank(ranking, n)    
    return [sents[j] for j in sents_idx]
#return the first n sentences with highest ranking
  def _rank(self, ranking, n):
    return nlargest(n, ranking, key=ranking.get)
#This function is used to get url from the webpage and parse it
def getTextFromURL(url):
	r = requests.get(url)
	soup = BeautifulSoup(r.text, "html.parser")
	text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
	return text
#This function is used for generating summarized text by calling frequencysummarizer
#class and gettextfromurl function which was built in this program     
def summarizeURL(url, total_pars):
	url_text = getTextFromURL(url)
	fs = FrequencySummarizer()
	final_summary = fs.summarize(url_text.replace("\n"," "), total_pars)
	return " ".join(final_summary)

url = raw_input("Enter a URL\n")
final_summary = summarizeURL(url, 5)
print (final_summary)
