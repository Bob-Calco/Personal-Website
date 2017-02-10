import math

class Decrypt:

    def __init__(self, s):
        self.s = list(s.lower())
        self.alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    # ## decrypt that s**t ## #
    def decrypt(self, method, keys):

        if method == "caesar":

            answers = {}
            if keys is None:
                # performs all shifts, prints shifts by score of frequency analysis
                for n in range(0,26):
                    shift = self.caesarian_shift(n)
                    answers[self.analyze_frequencies(shift)] = (shift, 26-n)
                return answers

            else:
                shift = self.caesarian_shift(26-keys)
                answers[self.analyze_frequencies(shift)] = (shift, keys)
                return answers

        elif method == "affine":
            answers = {}

            if keys is None:
                for n in range(1,26):
                    if math.gcd(n, len(self.alphabet)) == 1:
                        for i in range(0,26):
                            m = self.affine_cipher(n, i)
                            answers[self.analyze_frequencies(m)] = (m, (n ,i))
                return answers

            elif keys[0] is None and keys[1] is not None:
                for n in range(1,26):
                    if math.gcd(n, len(self.alphabet)) == 1:
                        m = self.affine_cipher(n, keys[1])
                        answers[self.analyze_frequencies(m)] = (m, (n, keys[1]))
                return answers

            elif keys[0] is not None and keys[1] is None:
                for i in range(0,26):
                    m = self.affine_cipher(keys[0], i)
                    answers[self.analyze_frequencies(m)] = (m, (keys[0] ,i))
                return answers

            else:
                m = self.affine_cipher(keys[0], keys[1])
                answers[self.analyze_frequencies(m)] = (m, keys)
                return answers

        elif method == "atbash":
            m = self.affine_cipher(25,25)
            return {self.analyze_frequencies(m): m}

    # ## try a Ceaserian cipher ## #
    # x = the amount to shift
    def caesarian_shift(self, x):
        output = ""

        for c in self.s:
            try:
                newCharIndex = (self.alphabet.index(c) + x) % 26
                output += self.alphabet[newCharIndex]
            except ValueError: # current char isn't in a letter
                output += c

        return output

    # ## try a Affine cipher ## #
    # also cracks the Atbash cipher #
    # 'a' needs to be coprime with the size of the alphabet
    def affine_cipher(self, a, b):
        # are 'a' and the size of the alphabet coprime?
        divisors = []
        al = len(self.alphabet)
        coprime = True
        for i in range(2, a):
            if a%i == 0:
                divisors.append(i)
        for i in range(2, al):
            if al%i == 0:
                if al in divisors:
                    coprime = False

        if coprime == False:
            return

        # calculate modular multiplicative inverse
        mmi = 0
        for i in range(1, len(self.alphabet)):
            if (a*i)%len(self.alphabet) == 1:
                mmi = i

        # make decoding keys
        keys = {}
        for c in self.alphabet:
            keys[c] = (mmi*(self.alphabet.index(c)-b)) % len(self.alphabet)

        # decode string
        output = ""
        for c in self.s:
            try:
                output += self.alphabet[keys[c]]
            except KeyError: # current char isn't in a letter
                output += c

        return output

    # ## count how often all letters appear ## #
    # return (print result)
    def analyze_frequencies(self, s):

        # English language expected results (Wikipedia)
        en_expected = {'a': 8.12, 'b': 1.49, 'c': 2.71, 'd': 4.32, 'e': 12.02, 'f': 2.3, 'g': 2.03, 'h': 5.92, 'i': 7.31, 'j': 0.10, 'k': 0.69, 'l': 3.98, 'm': 2.61, 'n': 6.95, 'o': 7.68, 'p': 1.82, 'q': 0.11, 'r': 6.02, 's': 6.28, 't': 9.10, 'u': 2.88, 'v': 1.11, 'w': 2.09, 'x': 0.17, 'y': 2.11, 'z': 0.07 }

        # setup dictionary keys
        frequencies = {}
        for c in self.alphabet:
            frequencies[c] = 0

        # fill dictionary with values
        for c in s:
            try:
                frequencies[c] = frequencies[c] + 1
            except KeyError: # current char isn't in a letter
                None

        # turn counts into percentages (and calculate score)
        total_letters = len(s)
        score = 0
        for k in frequencies:
            frequencies[k] = frequencies[k] / total_letters * 100
            score += abs(frequencies[k] - en_expected[k])

        return round(score, 2)

class Encrypt:

    def __init__(self, s):
        self.s = list(s.lower())
        self.alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    def encrypt(self, method, keys):
        if method == "caesar":
            return self.caesarian_shift(keys)
        elif method == "affine":
            return self.affine_cipher(keys[0], keys[1])
        elif method == "atbash":
            return self.affine_cipher(25,25)

    def caesarian_shift(self, x):
        output = ""

        for c in self.s:
            try:
                newCharIndex = (self.alphabet.index(c) + x) % 26
                output += self.alphabet[newCharIndex]
            except ValueError: # current char isn't in a letter
                output += c

        return output

    def affine_cipher(self, a, b):
        # are a and the size of the alphabet coprime?
        divisors = []
        al = len(self.alphabet)
        coprime = True
        for i in range(2, a):
            if a%i == 0:
                divisors.append(i)
        for i in range(2, al):
            if al%i == 0:
                if al in divisors:
                    coprime = False

        if coprime == False:
            return

        keys = {}
        for c in self.alphabet:
            keys[c] = (a * self.alphabet.index(c) + b) % len(self.alphabet)

        output = ""
        for c in self.s:
            try:
                output += self.alphabet[keys[c]]
            except KeyError: # current char isn't in a letter
                output += c

        return output
