#Puzzle 0

print(2**38)

#Puzzle 1
encrypted = "g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj."
alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "a", "b"]

new_word = ""

for let in encrypted:
    if let not in alphabet:
        new_word += let
    else:
        for letter in alphabet:
            if let == letter:
                let = alphabet[((alphabet.index(letter))+2)]
                new_word += let
                break

print(new_word)