from functools import reduce
from textblob import TextBlob

class User(object):
    """ classifies the attributes of the user and gets the overall sentiment of the users requests """
    def __init__(self, session, timestamp):
        self.log_list = [Request(session['chat'][log]) for log in session['chat']]
        self.sessionid = timestamp
        self.usertype = session['user_type']
        self.questions_asked = session['questions_asked']
        self.shops_asked = session['shops_asked']
        self.products_asked = session['products_asked']

    def get_sentiment_overall(self):
        request = [req.get_sentiment() for req in self.log_list]
        sen_array = []
        for sen in request:
            sen_array.append(sen[1])

        if len(sen_array) > 1:
            mean_sen = reduce((lambda x,y: x + y), sen_array) / len(sen_array)
            return mean_sen
        else:
            return sen_array[0]

    def get_usertype(self):
        request = [req.get_sentiment()[1] for req in self.log_list]
        request = np.array(request)
        length_neu = len([request[request == 0]])
        length_pos = len(request[request > 0])
        length_neg = len(request[request < 0])
        sum_pos_neg = (length_pos + length_neg)
        min = request.min()
        max = request.max()

        usertype = ''

        if length_neu > sum_pos_neg:
            usertype = 'neu'
        elif (length_pos > length_neg) or (length_pos == length_neg and max > (min*(-1))):
            usertype = 'pos'
        elif (length_pos < length_neg) or (length_pos == length_neg and max < (min*(-1))):
            usertype = 'neg'

        self.usertype = usertype

        return self.usertype

    def get_questions_asked(self):
        # Get every question asked but dont just one time
        self.questions_asked = {}
        all_questions_asked = {}
        for req in self.log_list:
            if not req.compare_string in all_questions_asked:
                all_questions_asked[req.compare_string] = req.text
        self.questions_asked = all_questions_asked
        
    def get_shops_asked(self):
        # Get every shop that was asked about but just one time
        self.shops_asked = [req.location for req in self.log_list]
        if len(self.shops_asked) != 0:
            self.shops_asked = set(self.shops_asked)
            self.shops_asked = list(self.shops_asked)
        if '' in self.shops_asked:
            self.shops_asked.remove('')

    def get_products_asked(self):
        # Get every product that was asked about but just one time
        self.products_asked = [req.product for req in self.log_list]
        if len(self.products_asked) != 0:
            self.products_asked = list(set(self.products_asked))
        if '' in self.products_asked:
            self.products_asked.remove('')

class Request(object):

    def __init__(self, log):
        self.id = id
        self.query = log['request']['query']
        self.client = log['request']['query']['client']
        self.location = log['request']['query']['location']
        self.notmatched = log['request']['query']['notmatched']
        self.product= log['request']['query']['product']
        self.product_key_words = log['request']['query']['product_key_words']
        self.question_key_words = log['request']['query']['question_key_words']
        self.question_words = log['request']['query']['question_words']
        self.verb = log['request']['query']['verb']
        self.sentiment = log['request']['sentiment']
        self.sentiment_type = log['request']['type']
        self.text = log['request']['text']
        self.response = log['response']['text']
        self.compare_string = log['request']['query']['compare_string']

    def get_sentiment(self):
        string = self.text
        polarity = TextBlob(string)
        pol = polarity.sentiment

        if pol[0] > 0:
            self.sentiment = pol[0]
            self.sentiment_type = 'pos'
        elif pol[0] == 0:
            self.sentiment = pol[0]
            self.sentiment_type = 'neu'
        else:
            self.sentiment = pol[0]
            self.sentiment_type = 'neg'

        return (self.sentiment_type, self.sentiment)
