import threading # To asynchronize a little bit. It's honestly underutilized, but I don't care to rewrite everything to get it to work
import string # Just for generating test letters
from random import randint, choice # Also for generating test data
from time import time_ns # Timing the function calculation, for debugging
from re import sub # Making sure the data looks clean.


class WordPair:
    """This class just holds each word, it's ascii key, and the number of occurences"""
    def __init__(self, word, key, number=1):
        self.word = word
        self.number = number
        self.key = key


class HashMap:
    def __init__(self): # These are obnoxious, and an expected, so we'll just get rid of them
        # This array holds a list of indices
        self.index_array = []
        self.funct = None
        self.array = []

        # Used for the asynchronous calculate_regression
        self.polyThread = None
        self.threadActive = False
        # Not really meant to be changed, for debugging
        """
        Technically this could be abused to force a collision but it should be suitable for this purpose
        It just goes through every letter in a word, takes it's uppercase ascii value, and concatenates them
        """
        self.l1Hash = lambda x: int("".join([str(ord(i.upper())) for i in list(x)]))


    def add(self, item):
        """
        This attempts to add an item to the HashMap
        First we try and get the item, if an Index or Type error is raised, we assume nonexistent
        If it does exist, we increase it's count by one
        Otherwise we add it onto the map, and update the array
        """
        if len(item) == 0:
            return
        try:
            a = self.__getitem__(item)[0]
            a.number += 1
            return
        except (IndexError, TypeError):
            # adds an item onto the map, then starts the regression calculation seperately
            self.soft_insert(item)
            self.update()
            

    def update(self):
        """This just goes through and actually triggers the function calculation"""
        print(f"Updating formulas for {len(self.array)} items")
        self.array.sort(key=lambda x: self.l1Hash(x.word))
        self.assert_safe()
        self.polyThread = threading.Thread(target=self.calculate_regression)
        self.polyThread.start()
        self.threadActive = True


    def calculate_regression(self):
        """
        Ok, in this function we take all the values from our array, and grab their ascii equivalent
        We then apply the Barycentric Langrange Interpolation, which creates a function mapping each of the
        input indices to their location in the main array. We then can use that function later on to find values in
        the HashMap

        This is actually the sixth iteration of this method. Previously we tried:
        1. Polynomial Regression
        2. Polynomial Regression split by word size
        3. A Neural Network
        4. Standard Lagrange Approximation
        5. Polynomial derived from barycentric approximation
        """

        lst = [i.key for i in self.array]
        
        def barycentric(x_vals, y_vals):
            """This is an algorithm designed to generate a function that passes through each of our supplied points"""
            n = len(x_vals)
            
            def barycentric_weights(xs):
                weights = [1] * n

                for i in range(n):
                    for j in range(n):
                        if i != j:
                            weights[i] /= (xs[i]-xs[j])
                return weights

            weights = barycentric_weights(x_vals)
            
            def evaluate(x):
                """
                Actually evaluates the barycentric function. Technically runs in O(n) instead of O(1) like a normal hashmap
                For the sake of the project though, this should count as a single "step", as it's running completly independent
                of whats actually in the array.
                """
                numerator = 0
                denominator = 0
                for i in range(n):
                    if x == x_vals[i]:
                        return y_vals[i]
                    temp = weights[i] / (x - x_vals[i])
                    numerator += temp * y_vals[i]
                    denominator += temp
                return numerator / denominator
            
            return evaluate

        self.funct = barycentric(lst, list(range(len(lst))))

    def soft_insert(self, item, count=1):
        """
        This function adds items into the array, but doesn't update functions
        This shouldn't be used unless you know what you're doing
        """
        
        # This just adds the items onto the array, 
        itemIndex = self.l1Hash(item)
        self.array.append(WordPair(item, itemIndex, count))
        self.array.sort(key=lambda x: x.key)


    def words_in(self, words):
        """Takes a list of words, adds them all up, then recalculates the function all at once"""
        unique_words = sorted(list(set(words)))
        
        for item in unique_words:
            self.soft_insert(item, 0)

        print("Added each unique word, populating counts, this may take a while")
            
        self.update()
        
        # Now we just go through and populate all the word counts
        for item in words:
            self.add(item)

        # We don't have any sub buckets, and we guarantee that there are no collisions
        return len(self.array), 0


    def assert_safe(self):
        """ This method checks to make sure that the regression function finished"""
        if self.threadActive:
            print("Waiting for regression thread to finish")
            time = time_ns()
            self.polyThread.join()
            self.threadActive = False
            print(f"Thread finished in {(time_ns() - time)/1000000000} seconds")


    def __getitem__(self, index):
        """Finds and scales the index, makes sure the function has finished updating, then runs it and gets the correct item"""

        scaled_index = self.l1Hash(index)
        # We run this last, just to give things the chance to process.
        self.assert_safe()

        if len(self.array) == 0:
            raise IndexError("The Hash Map is empty")
        else:
            # This is all the logic we need
            # Call and run our pre-defined function, then get that index
            result = self.funct(scaled_index)
            item = self.array[round(result)]
            
            # Just in case
            if item.key == self.l1Hash(index):
                return item, 1 # It only takes one step, there is a guaranteed zero collisions, so we don't check anything else
            else:
                raise IndexError("The item is not in the Hash Map, or there was a mismatch")
    

aglflaglHash = HashMap()

def words_in(words):
    words.sort()
    result = aglflaglHash.words_in(words)
    return result[0], result[1]

def lookup_word_count(word, hash=aglflaglHash):
    item = hash[word]
    return item[0].number, item[1]

if __name__ == "__main__":
    test = HashMap()
    def generate_random_word():
        return ''.join([choice(string.ascii_lowercase) for _ in range(randint(1, 8))])
        
    
    inwords = ["a", "a", "as", "at", "-"]
    #inwords = [generate_random_word() for _ in range(1000)]
    #inwords = ['g', 'n', 'n', 'hp', 'ij', 'md', 'ra', 'so', 'ty', 'xu', 'drd', 'fhj', 'gyg', 'hih', 'mfk', 'pae', 'umc', 'xfk', 'zee', 'cxou', 'iwld', 'pdiw', 'zovk', 'clyeb', 'efjsw', 'gxvwc', 'wjoaa', 'yxxut', 'zxrnn', 'etmlxo', 'fthzoy', 'ichyvk', 'jenazu', 'nauwew', 'noimfc', 'bvvxnxy', 'cjemair', 'etqdcxt', 'hqwdqwy', 'thlmfrt', 'busivlqg', 'cfiypojm', 'dygpsqae', 'dzmqapfz', 'gzzhtrfz', 'ijikhyik', 'iwcejujv', 'jeviteai', 'wacbjbgu', 'jsnljcsbl', 'wynnqimrf', 'zajxxsoyl', 'lbwrppygrf', 'nceakmbixb', 'pkikkfxwlq', 'pouzguexyb', 'rxeneqraeg', 'scaqrxfnbl', 'slxybsnqjg', 'vdqrmlhazb', 'ypalccnbqb', 'cnwkpgoqybz', 'jmlmrywfhfx', 'jrsqrmtapse', 'kpulqqoowke', 'ldutizxiwad', 'ndvyrivxgdb', 'vbvjlifparc', 'dhjklzdazgpg', 'irgerzyfassi', 'reahnbgvkpro', 'ucokdsosmeeo', 'xinmxqjbweik', 'aaeuxpgyuoxcl', 'bhwcmrlyngjwa', 'ctavuaziyaafd', 'ddajvmfhjdpqv', 'drrslvcboezlc', 'hdpptoamcjgtr', 'kmqvqmzowbknv', 'liyqlbuxveadq', 'ydmtegpfhqiay', 'dcvlmlogruamud', 'dyzavdxmywmczn', 'edureokkyvvddv', 'fredpmyenviqdm', 'fznnqbfracwrsb', 'gyptnhcqtxfjwf', 'hhhemhumvpxgxo', 'ivngvcmibhedvo', 'nsxfyebfbywddn', 'ponrfhqorynrfe', 'pqhowqpnwzurse', 'stfwtfvprikmjl', 'udctpexupkbxdz', 'hgptibmszdbkaaf', 'rhcxvbggscymcyf', 'xkiowecbuawlwbt', 'yvefzsvpqbjqrlt', 'zmfvryuuvkzsfki']
    _, hsh = words_in(inwords)
    finished = True
    print("Output: ")
    print("\n".join(" ".join([i, str(lookup_word_count(i))]) for i in sorted(inwords, key=lambda x: test.l1Hash(x))))
    print("Done!")
