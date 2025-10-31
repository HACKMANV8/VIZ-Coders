import nltk
from nltk.stem import WordNetLemmatizer
import numpy as np
import json
import pickle
import random
from tensorflow.keras.models import load_model

# Load pre-trained components
lemmatizer = WordNetLemmatizer()
model = load_model('chatbot_model.h5')
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))

def clean_up_sentence(sentence):
    """Tokenizes and lemmatizes the user's input sentence."""
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence, words, show_details=True):
    """Creates the Bag of Words array for the input sentence, matching the model's input format."""
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)  # Initialize bag with 0s
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1 # Set 1 if word is found in the vocabulary
                if show_details:
                    print(f"found in bag: {w}")
    return np.array(bag)

def predict_class(sentence, model):
    """Predicts the intent (class) of the user's sentence."""
    # Filter out predictions below a threshold
    p = bag_of_words(sentence, words, show_details=False)
    # The model expects a batch of inputs, so we wrap the array
    res = model.predict(np.array([p]))[0]
    
    # Define an error threshold
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    
    # Sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    
    # Return a list of dictionaries containing intent tag and probability
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def get_response(ints, intents_json):
    """Retrieves a random response based on the predicted intent."""
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(msg):
    """The main function to call for a chatbot response."""
    ints = predict_class(msg, model)
    if ints:
        res = get_response(ints, intents)
        return res
    else:
        # Fallback if no intent is matched above threshold
        return "I'm sorry, I don't understand. Could you please rephrase?"

# --- Main Chat Loop ---
print("Hospital Bot: I'm ready to chat! (Type 'quit' to exit)")
while True:
    user_input = input("You: ")
    if user_input.lower() == 'quit':
        print("Hospital Bot: Thank you for chatting. Goodbye!")
        break
    
    response = chatbot_response(user_input)
    print(f"Hospital Bot: {response}")