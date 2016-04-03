import nltk
import corenlp

file = open("appendix1.txt", "r")
props = Properties()
props.setProperty("annotators", "tokenize, ssplit, pos, lemma, ner, parse, dcoref")
pipeline = StanfordCoreNLP(props)

#read some text in the text variable
text = str(file) #Add your text here!

#create an empty Annotation just with the given text
document = Annotation(text)

#run all Annotators on this text
pipeline.annotate(document)