from sklearn.feature_extraction.text import TfidfVectorizer
from os import listdir
from os.path import isfile, join
import numpy as np
mypath="artists/Linkin_Park"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
mydoclist=[]
k=0
for fil in onlyfiles:
	file_name=mypath+'/'+fil;
	# print file_name
	temp=""
	k=k+1
	with open(file_name,"r") as fp:
		for line in fp:
			#print line
			temp=temp+line
	#print temp
	mydoclist.append(temp)


# mydoclist = ['Julie loves me more than Linda loves me',
# 'Jane likes me more than Julie loves me',
# 'He likes basketball more than baseball']

tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(mydoclist)
# print tfidf_vectorizer.get_feature_names()
print tfidf_matrix.todense()
file_name="artists/linkinpark.txt"
temp=""
with open(file_name,"r") as fp:
	for line in fp:
		#print line
		temp=temp+line
new_docs=[]
new_docs.append(temp)
new_term_freq_matrix = tfidf_vectorizer.transform(new_docs)
print tfidf_matrix.shape
print new_term_freq_matrix.shape
transpose_matrix=new_term_freq_matrix.transpose()
print transpose_matrix.shape
product=tfidf_matrix.dot(transpose_matrix)
print product

col=product.getcol(0)
N = col.shape[0]
sqr = col.copy() # take a copy of the col
sqr.data **= 2 # square the data, i.e. just the non-zero data
variance = sqr.sum()/N - col.mean()**2
print variance
# print type(tfidf_matrix[0][0])
# print type(new_term_freq_matrix[0])
# # for tf_vector in tfidf_matrix:
# # 	product.append(np.dot(tf_vector,new_term_freq_matrix))
# print new_term_freq_matrix
# print product
print len(mydoclist)
