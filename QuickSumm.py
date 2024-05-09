import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist

nltk.download('punkt')
nltk.download('stopwords')

def summarize_text(text, ratio=0.3):
    sentences = sent_tokenize(text)
    words = [word.lower() for sentence in sentences for word in word_tokenize(sentence) if word.isalnum()]
    words = [word for word in words if word not in stopwords.words('english')]

    # Calculate word frequency
    freq_dist = FreqDist(words)

    # Calculate sentence importance based on word frequency
    sentence_importance = {sentence: sum(freq_dist[word] for word in word_tokenize(sentence) if word in freq_dist) for sentence in sentences}

    # Sort sentences by importance and select the top ones
    top_sentences = sorted(sentence_importance, key=sentence_importance.get, reverse=True)[:int(len(sentences) * ratio)]

    return ' '.join(top_sentences)

# Get user input for the text
# text = input("Please enter the text you'd like to summarize: ")

# summary = summarize_text(text)

# print("Summarized text:")
# print(summary)