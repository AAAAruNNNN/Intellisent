import numpy as np
import sys
import pandas as pd
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Activation
from keras.layers import Embedding
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau
from keras.layers import LSTM
from keras.utils import to_categorical
import utils
from keras.preprocessing.sequence import pad_sequences
import csv

FREQ_DIST_FILE = 'tweets_new_train-freqdist.pkl'
BI_FREQ_DIST_FILE = 'tweets_new_train-freqdist-bi.pkl'
TRAIN_PROCESSED_FILE = 'tweets_new_train.csv'
TEST_PROCESSED_FILE = 'tweets_new_test.csv'
GLOVE_FILE = 'glove.twitter.27B.200d.txt'
dim = 200

def get_glove_vectors(vocab):
    print 'Looking for GLOVE vectors'
    glove_vectors = {}
    found = 0
    with open(GLOVE_FILE, 'r') as glove_file:
        for i, line in enumerate(glove_file):
            utils.write_status(i + 1, 0)
            tokens = line.split()
            word = tokens[0]
            if vocab.get(word):
                vector = [float(e) for e in tokens[1:]]
                glove_vectors[word] = np.array(vector)
                found += 1
    print '\n'
    print 'Found %d words in GLOVE' % found
    return glove_vectors

def get_feature_vector(tweet):
    words = tweet.split()
    feature_vector = []
    for i in range(len(words) - 1):
        word = words[i]
        if vocab.get(word) is not None:
            feature_vector.append(vocab.get(word))
    if len(words) >= 1:
        if vocab.get(words[-1]) is not None:
            feature_vector.append(vocab.get(words[-1]))
    return feature_vector


def process_tweets(csv_file, test_file=True):
    tweets = []
    labels = []
    print 'Generating feature vectors'
    df = pd.read_csv(csv_file)

    def get_info(text, tweet_class):
    	feature_vector = get_feature_vector(text)
    	if test_file:
    		tweets.append(feature_vector)
    	else:
    		tweets.append(feature_vector)
    		labels.append(tweet_class)

	# df['clean']  = df.apply(lambda x: clean_tweets(x['text'], x['query']), axis=1)

    df.apply(lambda row: get_info(row['text'], row['tweet_class']), axis=1)

    return tweets, np.array(labels)

if __name__ == '__main__':
    train = len(sys.argv) == 1
    np.random.seed(1337)
    vocab_size = 90000
    batch_size = 500
    max_length = 40
    filters = 600
    kernel_size = 3
    vocab = utils.top_n_words(FREQ_DIST_FILE, vocab_size, shift=1)
    glove_vectors = get_glove_vectors(vocab)

    tweets, labels = process_tweets(TRAIN_PROCESSED_FILE, test_file=False)
    embedding_matrix = np.random.randn(vocab_size + 1, dim) * 0.01
    for word, i in vocab.items():
        glove_vector = glove_vectors.get(word)
        if glove_vector is not None:
            embedding_matrix[i] = glove_vector
    tweets = pad_sequences(tweets, maxlen=max_length, padding='post')
    shuffled_indices = np.random.permutation(tweets.shape[0])
    tweets = tweets[shuffled_indices]
    labels = labels[shuffled_indices]
    if train:
        model = Sequential()
        model.add(Embedding(vocab_size + 1, dim, weights=[embedding_matrix], input_length=max_length))
        model.add(Dropout(0.4))
        model.add(LSTM(128))
        model.add(Dense(64))
        model.add(Dropout(0.5))
        model.add(Activation('relu'))
        model.add(Dense(4))
        model.add(Activation('softmax'))
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        filepath = "./models/lstm-{epoch:02d}-{loss:0.3f}-{acc:0.3f}-{val_loss:0.3f}-{val_acc:0.3f}.hdf5"
        checkpoint = ModelCheckpoint(filepath, monitor="loss", verbose=1, save_best_only=True, mode='min')
        reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=2, min_lr=0.000001)
        print model.summary()

        transformed_labels = to_categorical(labels)

        model.fit(tweets, transformed_labels, batch_size=128, epochs=30, validation_split=0.1, shuffle=True, callbacks=[checkpoint, reduce_lr])
    else:
        model = load_model(sys.argv[1])
        print model.summary()
        text = pd.read_csv(TEST_PROCESSED_FILE)
        text = text[['text', 'tweet_class']]
        test_tweets, _ = process_tweets(TEST_PROCESSED_FILE, test_file=True)
        test_tweets = pad_sequences(test_tweets, maxlen=max_length, padding='post')
        predictions = model.predict(test_tweets, batch_size=128, verbose=1)
        # results = zip(map(str, range(len(test_tweets))), np.round(predictions[:, 0]).astype(int))
        results = zip(map(str, range(len(test_tweets))), predictions)
        # utils.save_results_to_csv(results, 'lstm.csv')

        #confusion matrix

        # negneg, negneu, negpos, negjunk = 0, 0, 0, 0
        # neuneg, neuneu, neupos, neujunk = 0, 0, 0, 0
        # posneg, posneu, pospos, posjunk = 0, 0, 0, 0
        # junkneg, junkneu, junkpos, junkjunk = 0, 0, 0, 0

        # cmatrix = [ [0, 0, 0, 0],
        #             [0, 0, 0, 0],
        #             [0, 0, 0, 0],
        #             [0, 0, 0, 0] ] 

        # for value, p in [0, 1, 2, 3]: 
        #     for p in predictions:
        #         p = np.argmax(p)
                # if value == 3 and p == 0:
                #     cmatrix[value][p] += 1 
                # if value == 3 and p == 1: 
                #     cmatrix[value][p] += 1 
                # if value == 3 and p ==2:
                #     cmatrix[value][p] += 1 
                # if value == 3 and p == 3:
                #     cmatrix[value][p] += 1 
                # if value == 0 and p == 0:
                #     cmatrix[value][p] += 1 
                # if value == 0 and p == 1:
                #     cmatrix[value][p] += 1 
                # if value == 0 and p == 2:
                #     cmatrix[value][p] += 1 
                # if value == 0 and p == 3:
                #     cmatrix[value][p] += 1 
                # if value == 1 and p == 0:
                #     cmatrix[value][p] += 1 
                # if value == 1 and p == 1:
                #     cmatrix[value][p] += 1 
                # if value == 1 and p == 2:
                #     cmatrix[value][p] += 1 
                # if value == 1 and p == 3:
                #     cmatrix[value][p] += 1 
                # if value == 2 and p == 0:
                #     cmatrix[value][p] += 1 
                # if value == 2 and p == 1:
                #     cmatrix[value][p] += 1 
                # if value == 2 and p == 2:
                #     cmatrix[value][p] += 1 
                # if value == 2 and p == 3:
                #     cmatrix[value][p] += 1 

        # for i in range(4):
        #     print cmatrix[i] 
        #     print('\n')

        with open('lstm.csv', 'w') as f:
            fieldnames = ['id', 'text', 'prediction', 'predicted label', 'label'] 
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for i in range(len(results)):
                l = {'id': i, 'text': text.loc[i, 'text'] , 'prediction' : results[i][1], 'predicted label': np.argmax(results[i][1]),'label': text.loc[i, 'tweet_class']}
                writer.writerow(l)

        df = pd.read_csv('lstm.csv')


        cmatrix = [ [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0] ] 

        for i, row in df.iterrows():
            p = row['predicted label']
            value = row['label']

            if value == 3 and p == 0:
                cmatrix[value][p] += 1 
            if value == 3 and p == 1: 
                cmatrix[value][p] += 1 
            if value == 3 and p ==2:
                cmatrix[value][p] += 1 
            if value == 3 and p == 3:
                cmatrix[value][p] += 1 
            if value == 0 and p == 0:
                cmatrix[value][p] += 1 
            if value == 0 and p == 1:
                cmatrix[value][p] += 1 
            if value == 0 and p == 2:
                cmatrix[value][p] += 1 
            if value == 0 and p == 3:
                cmatrix[value][p] += 1 
            if value == 1 and p == 0:
                cmatrix[value][p] += 1 
            if value == 1 and p == 1:
                cmatrix[value][p] += 1 
            if value == 1 and p == 2:
                cmatrix[value][p] += 1 
            if value == 1 and p == 3:
                cmatrix[value][p] += 1 
            if value == 2 and p == 0:
                cmatrix[value][p] += 1 
            if value == 2 and p == 1:
                cmatrix[value][p] += 1 
            if value == 2 and p == 2:
                cmatrix[value][p] += 1 
            if value == 2 and p == 3:
                cmatrix[value][p] += 1 

        for i in range(4):
            print(str(i) + " :")
            print cmatrix[i] 
            print('\n')