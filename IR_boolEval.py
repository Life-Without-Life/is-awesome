#get set of documents with the word
def get_set(word):
    return set(inv_index[word]) if word in inv_index else set()
#evaluate the boolean query by splitting by OR and handling NOt and AND
def bool_eval(query):
    query_words = query.split(' ')
    query_words = [i for i in query_words if i in keywords]
    docs = [get_set(w) for w in query_words]
    result = list(set.intersection(*docs))
    print("Matched Documents: ")
    for i in range(len(result)):
        print('Document {:02d} : '.format(i+1), documents[result[i]])
#create inverted index by reading each document for all the words
keywords = open("keywords.txt").readlines()
keywords = [x.strip() for x in keywords]
documents = open("documents.txt", encoding='utf-8-sig').read().split('\n\n')
inv_index = {key:[] for key in keywords}
for i in range(len(documents)):
    for w in keywords:
        if any(x in documents[i] for x in [' ' + w, w + ' ', w + 's', w + "'"]) and i not in inv_index[w]:
                inv_index[w].append(i)
query = 'machine learning model'
bool_eval(query)
