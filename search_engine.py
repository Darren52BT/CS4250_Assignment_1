#-------------------------------------------------------------------------
# AUTHOR: Darren Banhthai
# FILENAME: search_engine.py
# SPECIFICATION: 
#   reads the collection.csv file for documents and labels, 
#   removes predetermined stop words and stems document words,
#   calculates document term weight matrix,
#   calculates document scores in relation to query
#   shows the retrieved, relevant, hit, missed, and noise docs
#   calculates precision and recall
# FOR: CS 4250- Assignment #1
# TIME SPENT: 3 hours
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with standard arrays

#importing some Python libraries
import csv
import math 

documents = []
labels = []

#reading the data in a csv file
with open('./collection.csv', 'r') as csvfile:
  reader = csv.reader(csvfile)
  for i, row in enumerate(reader):
         if i > 0:  # skipping the header
            documents.append (row[0])
            labels.append(row[1])

#trim whitespace from labels
for i, label in enumerate(labels):
  currentLabel = label
  while currentLabel[0] == ' ':
    currentLabel = currentLabel[1:]
  labels[i] = currentLabel
   
#Conduct stopword removal.
#--> add your Python code here
stopWords = {'I', 'and', 'She', 'They', 'her', 'their'}

#convert documents array into split word array for each doc
documents = [ doc.split(" ") for doc in documents]

#remove stopwords
for i, doc in enumerate(documents):
  newDoc = []
  for word in doc:
    if word not in stopWords:
      newDoc.append(word)
  documents[i] = newDoc


#Conduct stemming.
#--> add your Python code here
steeming = {
  "cats": "cat",
  "dogs": "dog",
  "loves": "love",
}

#start stemming words
for doc in documents:
  for i, word in enumerate(doc):
    #replaces with stem word if it exists or just itself if not
    doc[i] = steeming.get(word, word)

#Identify the index terms.
#--> add your Python code here
terms = []

#get terms
foundTerms = set()
#go through words in docs, if we have not encountered the current word, add it to terms
for doc in documents:
  for word in doc:
    if word not in foundTerms:
      terms.append(word)
      foundTerms.add(word)

#Build the tf-idf term weights matrix.
#--> add your Python code here

#helper functions for getting tf, df, idf, and tf-idf

def tf(word: str, doc: list[str]):
  return doc.count(word) / len(doc)

def df(word: str):
  count = 0
  for doc in documents:
    count += 1 if word in doc else 0
  return count 

def idf (word: str):
  return math.log(len(documents) / df(word), 10)

def tf_idf(word:str, doc: list[str]):
  return tf(word, doc) * idf(word)


docMatrix = []
#calculate matrix, term columns are love, cat, dog in this respective order
for i, doc in enumerate(documents):
  currentDoc = []
  for term in terms:
    currentDoc.append(round(tf_idf(term, doc), 4))
  docMatrix.append(currentDoc)

#Calculate the document scores (ranking) using document weigths (tf-idf) calculated before and query weights (binary - have or not the term).
#--> add your Python code here
docScores = []

query = "cat and dogs"
#tokenize query
tokenizedQuery = query.split(" ")

#remove stop words
stopRemoved = []
for word in tokenizedQuery:
    if word not in stopWords:
      stopRemoved.append(word)
tokenizedQuery = stopRemoved.copy()

#stem query
for i, word in enumerate(tokenizedQuery):
    #replaces with stem word if it exists or just itself if not
    tokenizedQuery[i] = steeming.get(word, word)

#get query weights
queryWeight = [ (1 if term in tokenizedQuery else 0) for term in terms]

#get document scores
for docIndex, doc in enumerate(documents):
  score = 0
  for termIndex, term in enumerate(terms):
    score += queryWeight[termIndex] * docMatrix[docIndex][termIndex]
  docScores.append(score)





#print out tokenized docs
for i, doc in enumerate(documents):
  print("Doc", (i + 1), "Tokens: ", doc )
print()

#print term weights matrix

termColumns = ""
for term in terms:
  termColumns += "          " + term
print(termColumns)
for i, docTermWeights in enumerate(docMatrix):
  scores = "Doc " + str(i+ 1) + ":"
  for termWeight in docTermWeights:
    scores += "      " + str(termWeight)
  print(scores)
print()

#pring query, query tokens, query weights
print("Query:", query)
print("Query tokens", tokenizedQuery)
print("Query Weight (binary):", queryWeight)
print()

#print doc scores
for i, docScore in enumerate(docScores):
  print("Doc", (i+1), "Score:", docScore)


#Calculate and print the precision and recall of the model by considering that the search engine will return all documents with scores >= 0.1.
#--> add your Python code here

#get retrieved
retrieved = []
for i, docScore in enumerate(docScores):
  if docScore >= .1:
    retrieved.append((i+1))

#get relevant
relevant = []
for i, label in enumerate(labels):
  if label == "R":
    relevant.append( i + 1)

#get hits 
hits = []
for retrievedDoc in retrieved:
  if retrievedDoc in relevant:
    hits.append(retrievedDoc)

#get misses
missed = []
for relevantDoc in relevant:
  if relevantDoc not in retrieved:
    missed.append(relevantDoc)

#get noise
noise = []
for retreivedDoc in retrieved:
  if retrievedDoc not in relevant:
    noise.append(retrievedDoc)


#calculate precision and recall

precision = round( (len(hits)/ (len(hits) + len(noise))), 4) * 100
recall = round( (len(hits) / (len(hits) + len(missed))), 4) * 100


#print results

print("Retrieved Docs:", retrieved)
print("Relevant Docs:", relevant)
print("Hit Docs:", hits)
print("Missed Docs:", missed)
print("Noise:", noise)

print()
print("Precision:", str(precision) + "%")
print("Recall:", str(recall) + "%")