akruti_to_unicode = {
    'Dç': 'अ', 'Kç': 'ख', 'kç': 'क्', 'çÆ': 'ि',
    'l': 'त्', 'l': 'ा', 'yç': 'ब्', 'cç': 'म', 'á': 'ू',
    'o': 'द', 'vç': 'न', 'v': 'न्', 'Jç': 'व', 'es': 'छ',
}

vowel = [u'ा', u'ि', u'ी', u'ु', u'ू',
         u'ृ', u'ॄ', u'ॅ', u'ॆ', u'े', u'ै', u'ॉ', u'ॊ', u'ो', u'ौ', u'्']


def convert_akruti_to_unicode(akruti_text):
    arr = []
    i = 0
    unicode_text = ''
    for char in akruti_text:
        # print(char)
        arr.append(char)

        # print(arr)
        # print(len(arr))
        # print(i)

        for key, value in akruti_to_unicode.items():

            if char == ' ' or char == '\n':
                unicode_text += ' '
                break

            if i > 1:
                print(arr[i-2] + arr[i-1] + arr[i], arr[i-1] + arr[i], arr[i])
            # if i > 1:
                if arr[i-2] + arr[i-1] + arr[i] == key:
                    unicode_text += akruti_to_unicode.get(key, value)
            # elif i > 1:
                elif arr[i-1] + arr[i] == key:
                    unicode_text += akruti_to_unicode.get(key, value)
                elif arr[i] == key:
                    unicode_text += akruti_to_unicode.get(key, value)

        i = i + 1

    arr = []
    i = 0

    for char in unicode_text:
        for matra in vowel:
            if arr[i - 1] + arr[i] == '्' + matra:
                unicode_text = unicode_text.replace(
                    '्' + matra, arr[i-2] + matra)

        i = i + 1

    return unicode_text
