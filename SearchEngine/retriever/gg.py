def stringMod(sentence,position,length):
    li = list(sentence.split())
    print(li)
    correctingFactor = 0
    for element in position:
        element +=correctingFactor
        li.insert(element,"<span>")
        after = element+length+1
        li.insert(after,"</span>")
        correctingFactor += 2
        print(after)
    return ' '.join(li)



sentence = "hello world     I am  computer science student at university  of Rwanda in year 2022"

position = [2, 8]
length = 2
print(stringMod(sentence,position,length))