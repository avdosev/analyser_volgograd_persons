import random
import re
import string
import json

from nltk import NaiveBayesClassifier
from nltk import classify
from nltk import word_tokenize
from nltk.corpus import twitter_samples, stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tag import pos_tag


def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token


def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield {token: True for token in tweet_tokens}


def tag_to_pos(tag):
    if tag.startswith("NN"):
        pos = 'n'
    elif tag.startswith('VB'):
        pos = 'v'
    else:
        pos = 'a'
    return pos


def remove_noise(tweet_tokens, stop_words=()):
    url_pattern = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'
                             '(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    word_pattern = re.compile("(@[A-Za-z0-9_]+)")
    lemmatizer = WordNetLemmatizer()
    for token, tag in pos_tag(tweet_tokens):
        token = url_pattern.sub('', token)
        token = word_pattern.sub('', token)
        pos = tag_to_pos(tag)
        token = lemmatizer.lemmatize(token, pos)
        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            yield token.lower()


if __name__ == "__main__":
    stop_words = stopwords.words('english')

    positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
    negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')

    # print(list(removed_noise(tweet_tokens[0], stop_words)))

    positive_cleaned_tokens = [remove_noise(tokens, stop_words) for tokens in positive_tweet_tokens]
    negative_cleaned_tokens = [remove_noise(tokens, stop_words) for tokens in negative_tweet_tokens]

    # all_pos_words = get_all_words(positive_cleaned_tokens)
    # freq_dist_pos = FreqDist(all_pos_words)

    positive_tokens_for_model = get_tweets_for_model(positive_cleaned_tokens)
    negative_tokens_for_model = get_tweets_for_model(negative_cleaned_tokens)

    positive_dataset = [(tweet_dict, "Positive")
                        for tweet_dict in positive_tokens_for_model]

    negative_dataset = [(tweet_dict, "Negative")
                        for tweet_dict in negative_tokens_for_model]

    dataset = positive_dataset + negative_dataset
    random.shuffle(dataset)
    train_data = dataset[:7000]
    test_data = dataset[7000:]

    classifier = NaiveBayesClassifier.train(train_data)

    print("Accuracy is:", classify.accuracy(classifier, test_data))

    print(classifier.show_most_informative_features(10))

    custom_tweets = json.load(open("custom_tweets.json"))

    custom_tokens = get_tweets_for_model(remove_noise(word_tokenize(custom_tweet)) for custom_tweet in custom_tweets)

    for i, custom_token in enumerate(custom_tokens):
        print(f"\"{custom_tweets[i]}\" is {classifier.classify(custom_token)}")
