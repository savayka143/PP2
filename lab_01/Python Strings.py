#'hello' is the same as "hello".
# You can use single or double quotes:

print("Hello")
print('Hello')

#Quotes inside quotes

print("It's alright")
print("He is called 'Johnny'")
print('He is called "Johnny"')

#Assign String to a Variable
a = "Hello"
print(a)

#Multiline Strings
a = """Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua."""
print(a)

#Strings are Arrays
a = "Hello, World!"
print(a[1])
# It will print 'e'

#Looping Through a String
for x in "banana":
    print(x)
#It wil itereaate through the string and print each character


#String Length
a = "Hello, World!"
print(len(a))
#It will print the length of the string. 
#In this case it will print 13


#Check String
txt = "The best things in life are free!"
print("free" in txt)
#It will print True because the word "free" is present in the string

txt = "The best things in life are free!"
if "free" in txt:
    print("Yes, 'free' is present.")
#It will print "Yes, 'free' is present."


#Check if NOT
txt = "The best things in life are free!"
print("expensive" not in txt)
#It will print True because the word "expensive" is not present in the string

txt = "The best things in life are free!"
if "expensive" not in txt:
    print("Yes, 'expensive' is NOT present.")
#It will print "Yes, 'expensive' is NOT present."

