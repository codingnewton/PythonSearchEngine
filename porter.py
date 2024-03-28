class Porter:
    # UTILS
    # check if the letter is not a vowel
    def __init__(self):
        pass

    def consonant(self, letter):
        letter = letter.lower()
        if letter == 'a' or letter == 'e' or letter == 'i' or letter == 'o' or letter == 'u':
            return False
        else:
            return True

    # check if the letter is a consonant
    def isConsonant(self, word, position):
        letter = word[position]
        letter = letter.lower()
        if self.consonant(letter):
            if letter == 'y' and self.consonant(word[position - 1]):
                return False
            else:
                return True
        else:
            return False

    # check if the letter is  a vowel
    def isVowel(self, word, i):
        return not(self.isConsonant(word, i))

    """
        Every word in the Porter form is [C](VC)^m[V], where
        - [C] possiblie set of Consonants sequence of lenght > 0;
        - (VC)^m sequence of Vowels and Consonants of lenght m;
        - [V] possiblie set of Vowels sequence of lenght > 0.
    """
    # rule that check the word's form
    def wordForm(self, word):
        form = []
        formStr = ''
        for position in range(len(word)):
            if self.isConsonant(word, position):
                if position != 0:
                    previous = form[-1]
                    if previous != 'C':
                        form.append('C')
                else:
                    form.append('C')
            else:
                if position != 0:
                    previous = form[-1]
                    if previous != 'V':
                        form.append('V')
                else:
                    form.append('V')
        for type in form:
            formStr += type
        return formStr

    # obtain the lenght of the (VC) sequence from the form (the m param)
    # m=2 => TROUBLES, PRIVATE, OATEN, ORRERY.
    def getM(self, word):
        form = self.wordForm(word)
        m = form.count('VC')
        return m

    # replace the removePart with the replacePart in the word
    def replace(self, word, removePart, replacePart):
        position = word.rfind(removePart)
        base = word[:position]
        replaced = base + replacePart
        return replaced

    # replace the removePart with the replacePart in the word if M is > 0
    def replaceM0(self, word, removePart, replacePart):
        position = word.rfind(removePart)
        base = word[:position]
        if self.getM(base) > 0:
            replaced = base + replacePart
            return replaced
        else:
            return word

    # replace the removePart with the replacePart in the word if M is > 1
    def replaceM1(self, word, removePart, replacePart):
        position = word.rfind(removePart)
        base = word[:position]
        if self.getM(base) > 1:
            replaced = base + replacePart
            return replaced
        else:
            return word


    """
        CONDITION PART
    """

    # *S - the stem ends with S (and similarly for the other letters).
    def endsWith(self, stem, letter):
        if stem.endswith(letter):
            return True
        else:
            return False


    # *v* - the stem contains a vowel.
    def containsVowel(self, stem):
        for letter in stem:
            if not self.consonant(letter):
                return True
        return False


    # *d - the stem ends with a double consonant (e.g. -TT, -SS).
    def doubleCons(self, stem):
        if len(stem) >= 2:
            if self.isConsonant(stem, -1) and self.isConsonant(stem, -2):
                return True
            else:
                return False
        else:
            return False


    # *o - the stem ends cvc, where the second c is not W, X or Y (e.g. -WIL, -HOP).
    def cvc(self, word):
        if len(word) >= 3:
            lastConsonant = word[-1]
            if self.isConsonant(word, -3) and self.isVowel(word, -2) and self.isConsonant(word, -1):
                if lastConsonant != 'w' and lastConsonant != 'x' and lastConsonant != 'y':
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False


    """
        STEP 1a:
    - SSES -> SS 
    - IES -> I 
    - SS -> SS 
    - S -> 
    """
    def step1a(self, word):
        if word.endswith('sses'):
            word = self.replace(word, 'sses', 'ss')
        elif word.endswith('ies'):
            word = self.replace(word, 'ies', 'i')
        elif word.endswith('ss'):
            word = self.replace(word, 'ss', 'ss')
        elif word.endswith('s'):
            word = self.replace(word, 's', '')
        return word

    """
        STEP 1b:
    - (m>0) EED -> EE 
    - (v) ED -> 
    - (v) ING -> 
    - S -> 
    If the second or third of the rules in Step 1b is successful, the following is done:
    - AT -> ATE 
    - BL -> BLE 
    - IZ -> IZE 
    - S -> 
    - (*d and not (*L or *S or *Z)) -> single letter
    - (m=1 and *o) -> E 

    The rule to map to a single letter causes the removal of one of the double letter pair. The -E is put back on -AT, 
    -BL and -IZ, so that the suffixes -ATE, -BLE and -IZE can be recognised later. This E may be removed in step 4.
    """
    def step1b(self, word):
        optionalStep = False
        if word.endswith('eed'):
            position = word.rfind('eed')
            base = word[:position]
            word = self.replaceM0(base, 'eed', 'ee')
        elif word.endswith('ed'):
            position = word.rfind('ed')
            base = word[:position]
            if self.containsVowel(base):
                word = base #truncate the part ed
                optionalStep = True     # the optional step will be executed
        elif word.endswith('ing'):
            position = word.rfind('ing')
            base = word[:position]
            if self.containsVowel(base):
                word = base #truncate the part ed
                optionalStep = True     # the optional step will be executed
        if optionalStep:
            if word.endswith('at') or word.endswith('bl') or word.endswith('iz'):
                word += 'e'
            elif self.doubleCons(word) and not self.endsWith(word, 'l') and not self.endsWith(word, 's') and not self.endsWith('z'):
                word = word[:-1]
            elif self.getM(word) == 1 and self.cvc(word):
                word += 'e'
        return word


    """
        STEP 1c:
    - (\*v\*) Y -> I 
    """
    def step1c(self, word):
        if word.endswith('y'):
            position = word.rfind('y')
            base = word[:position]
            if self.containsVowel(base):
                word = base
                word += 'i'
        return word

    """
        STEP 2:   
    -(m>0) ATIONAL -> ATE 
    -(m>0) TIONAL -> TION 
    -(m>0) ENCI -> ENCE 
    -(m>0) ANCI -> ANCE 
    -(m>0) IZER -> IZE 
    -(m>0) ABLI -> ABLE 
    -(m>0) ALLI -> AL 
    -(m>0) ENTLI -> ENT 
    -(m>0) ELI -> E 
    -(m>0) OUSLI -> OUS 
    -(m>0) IZATION -> IZE 
    -(m>0) ATION -> ATE 
    -(m>0) ATOR -> ATE 
    -(m>0) ALISM -> AL 
    -(m>0) IVENESS -> IVE 
    -(m>0) FULNESS -> FUL 
    -(m>0) OUSNESS -> OUS 
    -(m>0) ALITI -> AL 
    -(m>0) IVITI -> IVE 
    -(m>0) BILITI -> BLE 
    """
    def step2(self, word):
        if word.endswith('ational'):
            word = self.replaceM0(word, 'ational', 'ate')
        elif word.endswith('tional'):
            word = self.replaceM0(word, 'tional', 'tion')
        elif word.endswith('enci'):
            word = self.replaceM0(word, 'enci', 'ence')
        elif word.endswith('anci'):
            word = self.replaceM0(word, 'anci', 'ance')
        elif word.endswith('izer'):
            word = self.replaceM0(word, 'izer', 'ize')
        elif word.endswith('abli'):
            word = self.replaceM0(word, 'abli', 'able')
        elif word.endswith('alli'):
            word = self.replaceM0(word, 'alli', 'al')
        elif word.endswith('entli'):
            word = self.replaceM0(word, 'entli', 'ent')
        elif word.endswith('eli'):
            word = self.replaceM0(word, 'eli', 'e')
        elif word.endswith('ousli'):
            word = self.replaceM0(word, 'ousli', 'ous')
        elif word.endswith('ization'):
            word = self.replaceM0(word, 'ization', 'ize')
        elif word.endswith('ation'):
            word = self.replaceM0(word, 'ation', 'ate')
        elif word.endswith('ator'):
            word = self.replaceM0(word, 'ator', 'ate')
        elif word.endswith('alism'):
            word = self.replaceM0(word, 'alism', 'al')
        elif word.endswith('iveness'):
            word = self.replaceM0(word, 'iveness', 'ive')
        elif word.endswith('fulness'):
            word = self.replaceM0(word, 'fulness', 'ful')
        elif word.endswith('ousness'):
            word = self.replaceM0(word, 'ousness', 'ous')
        elif word.endswith('aliti'):
            word = self.replaceM0(word, 'aliti', 'al')
        elif word.endswith('iviti'):
            word = self.replaceM0(word, 'iviti', 'ive')
        elif word.endswith('biliti'):
            word = self.replaceM0(word, 'biliti', 'ble')
        return word


    """
        STEP 3:   
    -(m>0) ICATE -> IC 
    -(m>0) ATIVE -> 
    -(m>0) ALIZE -> AL 
    -(m>0) ICITI -> IC 
    -(m>0) ICAL -> IC 
    -(m>0) FUL -> 
    -(m>0) NESS -> 
    """
    def step3(self, word):
        if word.endswith('icate'):
            word = self.replaceM0(word, 'icate', 'ic')
        elif word.endswith('ative'):
            word = self.replaceM0(word, 'ative', '')
        elif word.endswith('alize'):
            word = self.replaceM0(word, 'alize', 'al')
        elif word.endswith('iciti'):
            word = self.replaceM0(word, 'iciti', 'ic')
        elif word.endswith('ical'):
            word = self.replaceM0(word, 'ical', 'ic')
        elif word.endswith('ful'):
            word = self.replaceM0(word, 'ful', '')
        elif word.endswith('ness'):
            word = self.replaceM0(word, 'ness', '')
        return word

    """
        STEP 4:   
    -(m>1) AL -> 
    -(m>1) ANCE -> 
    -(m>1) ENCE -> 
    -(m>1) ER -> 
    -(m>1) IC -> 
    -(m>1) ABLE -> 
    -(m>1) IBLE -> 
    -(m>1) ANT ->
    -(m>1) EMENT -> 
    -(m>1) MENT -> 
    -(m>1) ENT -> 
    -(m>1 and (*S or *T)) ION -> 
    -(m>1) OU -> 
    -(m>1) ISM -> 
    -(m>1) ATE -> 
    -(m>1) ITI ->
    -(m>1) OUS -> 
    -(m>1) IVE -> 
    -(m>1) IZE ->
    """
    def step4(self, word):
        if word.endswith('al'):
            word = self.replaceM1(word, 'al', '')
        elif word.endswith('ance'):
            word = self.replaceM1(word, 'ance', '')
        elif word.endswith('ence'):
            word = self.replaceM1(word, 'ence', '')
        elif word.endswith('er'):
            word = self.replaceM1(word, 'er', '')
        elif word.endswith('ic'):
            word = self.replaceM1(word, 'ic', '')
        elif word.endswith('able'):
            word = self.replaceM1(word, 'able', '')
        elif word.endswith('ible'):
            word = self.replaceM1(word, 'ible', '')
        elif word.endswith('ant'):
            word = self.replaceM1(word, 'ant', '')
        elif word.endswith('ement'):
            word = self.replaceM1(word, 'ement', '')
        elif word.endswith('ment'):
            word = self.replaceM1(word, 'ment', '')
        elif word.endswith('ent'):
            word = self.replaceM1(word, 'ent', '')
        elif word.endswith('ion'):
            position = word.rfind('ion')
            base = position[:position]
            if self.getM(base) > 1 and (self.endsWith(base, 's') or self.endsWith(base, 't')):
                word = base
            word = self.replaceM1(word, '', '')
        elif word.endswith('ou'):
            word = self.replaceM1(word, 'ou', '')
        elif word.endswith('ism'):
            word = self.replaceM1(word, 'ism', '')
        elif word.endswith('ate'):
            word = self.replaceM1(word, 'ate', '')
        elif word.endswith('iti'):
            word = self.replaceM1(word, 'iti', '')
        elif word.endswith('ous'):
            word = self.replaceM1(word, 'ous', '')
        elif word.endswith('ive'):
            word = self.replaceM1(word, 'ive', '')
        elif word.endswith('ize'):
            word = self.replaceM1(word, 'ize', '')
        return word

    """
        STEP 5a:   
    -(m>1) E -> 
    -(m=1 and not *o) E -> 
    """
    def step5a(self, word):
        if word.endswith('e'):
            base = word[:-1]
            if self.getM(base) > 1:
                word = base
            elif self.getM(base) > 1 and not self.cvc(base):
                word = base
        return word

    """
        STEP 5b:
    - (m > 1 and *d and *L) -> single letter
    """
    def step5b(self, word):
        if self.getM(word) > 1 and self.doubleCons(word) and self.endsWith(word, 'l'):
            word = word[:-1] #remove the last one
        return word


    # given a word as argument, returns the stem by applying the Porter algorithm
    def getStem(self, word):
        word = self.step1a(word)
        word = self.step1b(word)
        word = self.step1c(word)
        word = self.step2(word)
        word = self.step3(word)
        word = self.step4(word)
        word = self.step5a(word)
        word = self.step5b(word)
        return word
