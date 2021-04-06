# Problem Set 4C
# Name: Matthew Vogel
# Collaborators:
# Time Spent: x:xx

import string
from ps4a import get_permutations
import re

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    
    #print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    #print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

# you may find these constants helpful
VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'

class SubMessage(object):
    def __init__(self, text):
        '''
        Initializes a SubMessage object
                
        text (string): the message's text

        A SubMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words('words.txt')
        
    
    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return(self.message_text)

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        return(self.valid_words.copy())
                
    def build_transpose_dict(self, vowels_permutation):
        '''
        vowels_permutation (string): a string containing a permutation of vowels (a, e, i, o, u)
        
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to an
        uppercase and lowercase letter, respectively. Vowels are shuffled 
        according to vowels_permutation. The first letter in vowels_permutation 
        corresponds to a, the second to e, and so on in the order a, e, i, o, u.
        The consonants remain the same. The dictionary should have 52 
        keys of all the uppercase letters and all the lowercase letters.

        Example: When input "eaiuo":
        Mapping is a->e, e->a, i->i, o->u, u->o
        and "Hello World!" maps to "Hallu Wurld!"

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        
        # create a dictionary of all upper and lowercase letters, mapped to themselves
        permuted_dict = {}
        all_letters = VOWELS_LOWER + VOWELS_UPPER + CONSONANTS_LOWER + CONSONANTS_UPPER
        for l in all_letters:
            permuted_dict[l] = l
        
        # itterate over vowels_lower, and map the first vowel (a) to the first item in vowels_permutations
        count = 0
        for c in VOWELS_LOWER:
            permuted_dict[c] = vowels_permutation[count]
            count +=1
        # do the same thing with an uppercase version of vowels+permutation and vowels_upper
        count_u = 0
        for c in VOWELS_UPPER:
            permuted_dict[c] = vowels_permutation[count_u].upper()
            count_u += 1
        
        # retrun this new dictionary
        return(permuted_dict)
    
    def apply_transpose(self, transpose_dict):
        '''
        transpose_dict (dict): a transpose dictionary
        
        Returns: an encrypted version of the message text, based 
        on the dictionary
        '''
        
        # create a variable which contains the message to be encoded
        text = self.get_message_text()
        
        # create a new variable for the encoded message, and loop over messages letters, adding their key in transpose dict to the new variable
        encoded_text = ''
        for c in text:
            if c in string.ascii_letters:
                encoded_text += transpose_dict[c]
            else: encoded_text += c
        
        # return the new variable
        return(encoded_text)
        
class EncryptedSubMessage(SubMessage):
    def __init__(self, text):
        '''
        Initializes an EncryptedSubMessage object

        text (string): the encrypted message text

        An EncryptedSubMessage object inherits from SubMessage and has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words('words.txt')

    def decrypt_message(self):
        '''
        Attempt to decrypt the encrypted message 
        
        Idea is to go through each permutation of the vowels and test it
        on the encrypted message. For each permutation, check how many
        words in the decrypted text are valid English words, and return
        the decrypted message with the most English words.
        
        If no good permutations are found (i.e. no permutations result in 
        at least 1 valid word), return the original string. If there are
        multiple permutations that yield the maximum number of words, return any
        one of them.

        Returns: the best decrypted message    
        
        Hint: use your function from Part 4A
        '''

        
        # get the permutations of all vowels
        vowels_permuted = get_permutations(VOWELS_LOWER)

        # build a transpose dictionary with these permutations
        valid_words = self.get_valid_words()
        greatest_valid = 0
        greatest_permutation = 0
        for perm in vowels_permuted:
            transpose_dict = self.build_transpose_dict(perm)

        # apply transpose on the origional message using these transpose dicts
            new_message = self.apply_transpose(transpose_dict)

        
        # test each of these new messages to see how many words are valid
            valid_count = 0 
            new_message_list = re.split('\s+', new_message)
            for w in new_message_list:
                if is_word(valid_words, w):
                    valid_count +=1
        # if the number of valid words is greater than the p
            if valid_count > greatest_valid:
                greatest_valid = valid_count
                greatest_permutation = perm
        
        # retrun the decrypted message with the best permutation
        return(self.apply_transpose(self.build_transpose_dict(greatest_permutation)))
if __name__ == '__main__':

    # Example test case
    # message = SubMessage("Hello World!")
    # permutation = "eaiuo"
    # enc_dict = message.build_transpose_dict(permutation)
    # print("Original message:", message.get_message_text(), "Permutation:", permutation)
    # print("Expected encryption:", "Hallu Wurld!")
    # print("Actual encryption:", message.apply_transpose(enc_dict))
    # enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    # print("Decrypted message:", enc_message.decrypt_message())
    
     
    #TODO: WRITE YOUR TEST CASES HERE
    message = SubMessage('Hello World!')
    permutation = 'eaiuo'
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Hallu Wurld!")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())
    
    message2 = SubMessage('TesTING: CAPitol!  $  and. PUNNctuation')
    permutation2 = 'ieuoa'
    enc_dict2 = message2.build_transpose_dict(permutation2)
    print("Original message:", message2.get_message_text(), "Permutation:", permutation2)
    print('expected encryption:', 'TesTUNG: CIPutol!  $  ind. PANNctaituon')
    print("Actual encryption:", message2.apply_transpose(enc_dict2))
    enc_message2 = EncryptedSubMessage(message2.apply_transpose(enc_dict2))
    print("Decrypted message:", enc_message2.decrypt_message())