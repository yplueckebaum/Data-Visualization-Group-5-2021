from titleprocessor import *

# TESTING

print("-----> Testing for parenthesis")
assert(did_use_parenthesis_or_square_brackets("ahwewaheaje(") == False) #FALSE
assert(did_use_parenthesis_or_square_brackets("ahwe)waheaje)") == False) #FALSE
assert(did_use_parenthesis_or_square_brackets("ahwewa)heaje(") == False) #FALSE
assert(did_use_parenthesis_or_square_brackets("ahwewa)heaje(") == False) #FALSE
assert(did_use_parenthesis_or_square_brackets("ahwewa(heaje)") == True) #TRUE
print("PASSED")

print("-----> Testing for square brackets")
assert(did_use_parenthesis_or_square_brackets("ahwewaheaje[") == False) #FALSE
assert(did_use_parenthesis_or_square_brackets("ahwe]waheaje]") == False) #FALSE
assert(did_use_parenthesis_or_square_brackets("ahwewa]heaje[") == False) #FALSE
assert(did_use_parenthesis_or_square_brackets("ahwewa]heaje[") == False) #FALSE
assert(did_use_parenthesis_or_square_brackets("ahwewa[heaje]") == True) #TRUE
print("PASSED")

print("-----> Testing for combination of parenthesis and square brackets")
assert(did_use_parenthesis_or_square_brackets("ahwewa(heaje]") == False) #FALSE
assert(did_use_parenthesis_or_square_brackets("ahwe]waheaje(") == False) #FALSE
assert(did_use_parenthesis_or_square_brackets("ahwewa[he(aje]") == True) #TRUE
assert(did_use_parenthesis_or_square_brackets("ahwewa(he[aje)") == True) #TRUE
assert(did_use_parenthesis_or_square_brackets("ahw[ewa(heaje(]") == True) #TRUE
print("PASSED")

print("-----> Testing for CAPS")
assert(did_use_caps("hej med dig, jeg hedder kaj") == False)
assert (did_use_caps("hej med dig, jeg hedder Kaj") == False)
assert (did_use_caps("hej med DIG, jeg hedder Kaj") == True)
print("PASSED")

print("-----> Testing for emojis")
assert (did_use_emojis("für 😊😎 Liebe Grüße Nora & Bertil") == True)
assert(did_use_emojis("vielen Dank Euch dafür 😊😎 Liebe Grüße Nora & Bertil") == True)
assert (did_use_emojis("vielen Dank Euch dafür Liebe Grüße Nora & Bertil") == False)
print("PASSED")