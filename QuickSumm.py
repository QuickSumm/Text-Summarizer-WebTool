import nltk
import spacy
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Load SpaCy English model
nlp = spacy.load("en_core_web_sm")

def summarize_text(text, ratio=0.3, include_named_entities=False):
    sentences = sent_tokenize(text)
    words = [word.lower() for sentence in sentences for word in word_tokenize(sentence) if word.isalnum()]
    words = [word for word in words if word not in stopwords.words('english')]

    freq_dist = FreqDist(words)

    # Calculate sentence importance based on frequency distribution
    sentence_importance = {sentence: sum(freq_dist[word] for word in word_tokenize(sentence) if word in freq_dist) for sentence in sentences}

    # Use SpaCy for Named Entity Recognition
    if include_named_entities:
        doc = nlp(text)
        named_entities = set()
        for ent in doc.ents:
            named_entities.add(ent.text)
        # Exclude named entities from word frequency calculation
        words = [word for word in words if word not in named_entities]

    # Recalculate sentence importance after excluding named entities
    freq_dist = FreqDist(words)
    sentence_importance = {sentence: sum(freq_dist[word] for word in word_tokenize(sentence) if word in freq_dist) for sentence in sentences}

    # Select top sentences based on importance
    top_sentences = sorted(sentence_importance, key=sentence_importance.get, reverse=True)[:int(len(sentences) * ratio)]

    return ' '.join(top_sentences)

# Example usage:
# text = input("Please enter the text you'd like to summarize: ")
# summary = summarize_text(text, include_named_entities=True)
# print("Summarized text:")
# print(summary)
