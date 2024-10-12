from metrics import bertcos

text1 = ["Hello, my dog is very cute", "Be careful, my cat can bite you"]
text2 = ["Привет, моя собака очень милая", "Осторожно, моя кошка кусается"]
print(bertcos(text1, text2))

text1 = ["Hello, my dog is very cute", "Be careful, my cat can bite you"]
text2 = [ "Осторожно, моя кошка кусается", "Привет, моя собака очень милая"]
print(bertcos(text1, text2))

text1 = ["Hello, my dog is very cute", "Be careful, my cat can bite you"]
text2 = [ "Моя корова курит травку", "Осторожно, моя коза работает в полиции"]
print(bertcos(text1, text2))