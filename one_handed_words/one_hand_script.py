with open('words.txt', 'r') as file:
    contents = file.read()
    wordlist = contents.split()
dictionary_placeholder = ["word1", "word2", "word3", "word4","green", "blue", "orange", "qwer","asdf","zxcv", "ajghtoi"]

#list of letters in reach of left and right hands respectively
left = ["q","w","e","r","t","g","f","d","s","a","z","x","c","v","b"]
right = ["y","u","i","o","p","h","j","k","l","n","m",";","\'", "\"","."]

def generate_words(list = wordlist):
    print("Do you want words you can only type with your Left Hand or your Right Hand?")
    choice = input()
    if "left" in choice:
        hand = left
    if "right" in choice:
        hand = right
    newlist = []
    for word in range(len(list)):
        for letter in list[word]:
            if letter not in hand:
                newlist.append(list[word])
                break
    for i in newlist:
        list.remove(i)
    print("found " +  str(len(list)) + " words. Saved to one_hand.txt")
    with open("one_hand.txt", "w") as one_hand:
        for i in list:
            one_hand.write(i + "\n")
    one_hand.close
    return one_hand


generate_words()



