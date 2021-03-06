'''
Note: this script will never work unless you already
prepared the necessary data that the different classifiers will use.
To create them, you will first choose one of the four different features
    (Naive Bayes
    Cosine distance
    Rocchio
    Neural network)
and then go to the related .py file and follow the instructions.
These instructions will ask you to use function written inside the .py
to write 'training' files that will be used by the classifiers.
Those functions will almost everytime start with 'write_'.
Attention: Cosine distance classifier provides two different possibilities:
    the first one is to choose one of the 3 different embedding types (
        one hot        encoding
        term frequency encoding
        tfidf          encoding),
        it will be slower because it will compute
        as many cosine products as the number of files
        in the collection (in fact, every document
        must have already been converted into a vector,
        and you'll be able to do that using 'encoder.py')
    the second one is to use the optimized version of cosine distance,
    available in 'optimized_cosine_distance.py', it will use only tfidf encoding.
As a suggestion, it will be easier if the user
focuses on Naive Bayes first,
then on optimized cosine distance (for these first two, the file 'indexer.py' will be the
most important one),
then on cosine distance rocchio and neural network (for this two, all the vectors will
be needed, and you'll have to look at 'encoder.py').


Neural network will be automatically instantiated
loading precomputed weights from mine training
on the 7063 available files, using tfidf vectors,
unfortunately I won't be able to attach
the precomputed weights because the nodes of
the output layer are only some MB,
but the nodes of the hidden layer are more that 1 GB,
only a few selected people will receive those weights :P
of course the user can train it himself looking at 'neural_network_pilot.py'
    'neural_network_pilot.py'
'''

from cosine_distance import document_query
from naive_bayes import naive_bayes
from neural_network_pilot import instantiate_neural_network, query_neural_network
from optimized_cosine_distance import optimized_improved_cosine_distance_tfidf
from reuter_handler import get_topics_from_list_ids, get_content_from_newid
from rocchio import rocchio
from util import get_first_n_instances_from_top_score


def driver():
    top = 5
    encoding_type = 'term_frequency'
    fast = False

    while(True):

        print('1 -> Query')
        print('2 -> Document ID')
        print('-> ')
        choice = int(input())

        if choice == 1:
            print('Insert a query:\n-> ')
            query = input()
        elif choice == 2:
            print('Insert an id: \n-> '),
            newid = input()
            query = get_content_from_newid(newid)
            print(query[:200] + '...')
        else:
            print('Bye')
            exit(-1)

        print("")

        print('1 -> Naive Bayes')
        print('2 -> Cosine distance')
        print('3 -> Rocchio')
        print('4 -> Neural network')
        print('-> ')
        algorithm = int(input())

        if algorithm == 2 or algorithm == 3:
            print('1 -> hot encoding')
            print('2 -> term frequency')
            print('3 -> tfidf')
            encoding = int(input())
            if encoding == 1:
                encoding_type = 'hot_encoding'
            elif encoding == 2:
                encoding_type = 'term_frequency'
            elif encoding == 3:
                encoding_type = 'tfidf'

        if algorithm == 2:
            print('optimized: [Y/N]')
            print('-> ')
            flag = str(input()).lower()
            if flag == 'y':
                fast = True

        print("")

        if algorithm == 1:
            print("naive bayes -> " + str(get_first_n_instances_from_top_score(naive_bayes(query), top)))

        elif algorithm == 2:
            if fast:
                top_optimized_ids = optimized_improved_cosine_distance_tfidf(query)
                result = get_first_n_instances_from_top_score(top_optimized_ids, top)
                print('optimized cosine distance with tfidf -> ' + str(result))
                print('topics on optimized cosine distance with tfidf -> ' + str(get_topics_from_list_ids(result)))
                fast = False
            else:
                top_non_optimized_ids = document_query(query, encoding_type)
                print("cosine distance with encoding: " + encoding_type + " -> " + str(
                    get_first_n_instances_from_top_score(top_non_optimized_ids, top)))
                print("topics from cosine distance with encoding " + encoding_type + " -> " + str(
                    get_topics_from_list_ids(get_first_n_instances_from_top_score(top_non_optimized_ids, top))))

        elif algorithm == 3:
            print("rocchio with encoding: " + encoding_type + " -> " + str(
                get_first_n_instances_from_top_score(rocchio(query, encoding_type), top)))

        elif algorithm == 4:
            nn = instantiate_neural_network(0.001, load=True)
            print("neural network with tfidf: -> " + str(query_neural_network(nn, query)))

        print("")


if __name__ == '__main__':
    driver()
