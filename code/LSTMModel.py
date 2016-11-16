

import tensorflow as tf
from tensorflow.python.ops import rnn_cell, seq2seq
import numpy as np

import constants as c
from utils import unkify


class LSTMModel:
    def __init__(self, sess, vocab, batch_size, seq_len, cell_size, num_layers, test=False):
        """
        Initializes an LSTM Model.

        @param sess: The TensorFlow Session.
        @param vocab: A list of all the words on which the model will be trained.
        @param batch_size: The batch size for training.
        @param seq_len: The sequence length. (The number of words in each element of the batch.)
        @param cell_size: The size of the hidden layers in the LSTM cells.
                          (also the size of the word embeddings.)
        @param num_layers: The number of LSTM layers in the network.
        @param test: Whether to test or train the model. Default = False.
        """
        self.sess = sess

        self.vocab = vocab
        self.vocab_size = len(self.vocab)
        self.batch_size = batch_size
        self.seq_len = seq_len
        self.cell_size = cell_size
        self.num_layers = num_layers

        self.build_graph(test)

    def build_graph(self, test):
        """
        Builds an LSTM graph in TensorFlow.
        """
        if test:
            self.batch_size = 1
            self.seq_len = 1





        lstm_cell = rnn_cell.BasicLSTMCell(self.cell_size)
        self.cell = rnn_cell.MultiRNNCell([lstm_cell] * self.num_layers)






        self.inputs = tf.placeholder(tf.int32, [self.batch_size, self.seq_len])
        self.targets = tf.placeholder(tf.int32, [self.batch_size, self.seq_len])
        self.initial_state = self.cell.zero_state(self.batch_size, tf.float32)




        with tf.variable_scope('lstm_vars'):
            self.ws = tf.get_variable('ws', [self.cell_size, self.vocab_size])
            self.bs = tf.get_variable('bs', [self.vocab_size])

            with tf.device('/cpu:0'):
                self.embeddings = tf.get_variable('embeddings', [self.vocab_size, self.cell_size])


                input_embeddings = tf.nn.embedding_lookup(self.embeddings, self.inputs)



                inputs_split = tf.split(1, self.seq_len, input_embeddings)
                inputs_split = [tf.squeeze(input_, [1]) for input_ in inputs_split]

















        def loop(prev, _):
            prev = tf.matmul(prev, self.ws) + self.bs
            prev_symbol = tf.stop_gradient(tf.argmax(prev, 1))
            return tf.nn.embedding_lookup(self.embeddings, prev_symbol)

        lstm_outputs_split, self.final_state = seq2seq.rnn_decoder(inputs_split,
                                                                   self.initial_state,
                                                                   self.cell,
                                                                   loop_function=loop if test else None,
                                                                   scope='lstm_vars')
        lstm_outputs = tf.reshape(tf.concat(1, lstm_outputs_split), [-1, self.cell_size])






























        logits = tf.matmul(lstm_outputs, self.ws) + self.bs
        self.probs = tf.nn.softmax(logits)





        total_loss = seq2seq.sequence_loss_by_example([logits],
                                                      [tf.reshape(self.targets, [-1])],
                                                      [tf.ones([self.batch_size * self.seq_len])],
                                                      self.vocab_size)
        self.loss = tf.reduce_sum(total_loss) / self.batch_size / self.seq_len

        self.global_step = tf.Variable(0, trainable=False, name='global_step')
        self.optimizer = tf.train.AdamOptimizer(learning_rate=c.L_RATE, name='optimizer')
        self.train_op = self.optimizer.minimize(self.loss,
                                                global_step=self.global_step,
                                                name='train_op')


    def generate(self, num_out=200, prime=None, sample=True):
        """
        Generate a sequence of text from the trained model.

        @param num_out: The length of the sequence to generate, in num words.
        @param prime: The priming sequence for generation. If None, pick a random word from the
                      vocabulary as prime.
        @param sample: Whether to probabalistically sample the next word, rather than take the word
                       of max probability.
        """
        state = self.sess.run(self.cell.zero_state(1, tf.float32))



        if prime is None:
            prime = np.random.choice(self.vocab)
        else:
            prime = unkify(prime, self.vocab)


        for word in prime.split():
            print word
            last_word_i = self.vocab.index(word)
            input_i = np.array([[last_word_i]])

            feed_dict = {self.inputs: input_i, self.initial_state: state}
            state = self.sess.run(self.final_state, feed_dict=feed_dict)


        gen_seq = prime
        for i in xrange(num_out):

            input_i = np.array([[last_word_i]])
            feed_dict = {self.inputs: input_i, self.initial_state: state}
            probs, state = self.sess.run([self.probs, self.final_state], feed_dict=feed_dict)
            probs = probs[0]


            if sample:
                gen_word_i = np.random.choice(np.arange(len(probs)), p=probs)
            else:
                gen_word_i = np.argmax(probs)


            gen_word = self.vocab[gen_word_i]
            gen_seq += ' ' + gen_word
            last_word_i = gen_word_i

        return gen_seq
