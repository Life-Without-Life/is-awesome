from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
#perform cosine similarity on tfidf of the query and documents
def query_search(query, X):
    q_tfidf = vectorizer.fit_transform([query])
    results = cosine_similarity(X,q_tfidf).reshape((-1,))
    print("Top 10 Documents matched: ")
    j = 0
    for i in results.argsort()[-10:][::-1]:
        j += 1
        print("Document {:02d}: ".format(j), documents[i])

keywords = open("keywords.txt").readlines()
keywords = [x.strip() for x in keywords]
documents = open("documents.txt", encoding='utf-8-sig').read().split('\n\n')
vectorizer = TfidfVectorizer(vocabulary=keywords)
X = vectorizer.fit_transform(documents)
query = 'neural machine learning'
query_search(query, X)
