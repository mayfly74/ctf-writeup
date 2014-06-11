#-*- coding:utf-8 -*-
import numpy, sys, os, struct   

# code for secuinside2014 findkey 
# by mayfly74

# 0x804F180
result = [0x00029344, 0x00029b98, 0x00020630, 0x0003a1f8,
0x0001db6e, 0x00028a16, 0x00008e42, 0x000503c3,
0x000547c2, 0x000557e3, 0x0005932c, 0x00056746,
0x00058315, 0x0004c52d, 0x0005650a, 0x000497dd,
0x0005841b, 0x0005d457, 0x00055db6, 0x0005a0ee,
0x00049f50, 0x00056415, 0x0005601d, 0x0005552c,
0x000524e7, 0x00037c93, 0x0003ba56, 0x0003c681,
0x00038782, 0x0003c827, 0x00037e33, 0x0003a18d,
0x000323be, 0x00039fc0, 0x0003db20, 0x00051e82,
0x0005402b, 0x000555a5, 0x00047343, 0x0004fdcd,
0x00052656, 0x0004cfb8, 0x00056153, 0x0005864c,
0x000579c3, 0x000575f0, 0x00045213, 0x00051aa8,
0x000558bd, 0x00056a64, 0x0004c639, 0x0004f711,
0x0003f162, 0x0004d9f6, 0x0005188a, 0x00052808]

# 0x804F0A0
strtab = [ "No pain, No gain - gogil",
"Fighting! - lokihardt",
"Rock'n Roll~ - anncc",
"WTF(Welcome To Facebook) - hellsonic",
"Enjoy~ :) - hkpco",
"I love meat - wooyaggo",
" - v0n",
"An algorithm must be seen to be believed. - Donald Knuth",
"The purpose of computing is insight, not numbers. - Richard Hamming",
"If you don't know anything about computers, just remember that they are machines that do exactly what you tell them but often surprise you in the result. - Richard Dawkins",
"Computers are good at following instructions, but not at reading your mind. - Donald Knuth",
"UNIX is user-friendly, it just chooses its friends. - Andreas Bogk",
"The most important property of a program is whether it accomplishes the intention of its user. - C.A.R. Hoare",
"The computing scientist’s main challenge is not to get confused by the complexities of his own making. -  Edsger W. Dijkstra",
"One of my most productive days was throwing away 1000 lines of code. - Ken Thompson",
"When in doubt, use brute force. - Ken Thompson",
"The most effective debugging tool is still careful thought, coupled with judiciously placed print statements. - Brian W. Kernighan",
"Controlling complexity is the essence of computer programming. - Brian W. Kernighan",
"Mathematicians stand on each others' shoulders and computer scientists stand on each others' toes. - Richard Hamming",
"Simplicity is prerequisite for reliability. - Edsger W. Dijkstra",
"This ‘users are idiots, and are confused by functionality’ mentality of Gnome is a disease. If you think your users are idiots, only idiots will use it. - Linux",
"Young man, in mathematics you don't understand things. You just get used to them. - John von Neumann",
"If people do not believe that mathematics is simple, it is only because they do not realize how complicated life is.  -  John von Neumann",
"The first principle is that you must not fool yourself - and you are the easiest person to fool. -Richard Feynman",
"I don't know what's the matter with people: they don't learn by understanding; they learn by some other way - by rote or something. Their knowledge is so fragile! - Richard Feynman",
"http://youtu.be/3O1_3zBUKM8 - youtube",
"http://youtu.be/vc6vs-l5dkc - youtube",
"http://youtu.be/v_3svzxSF4w - youtube",
"http://youtu.be/AGlKJ8CHAg4 - youtube",
"http://youtu.be/atz_aZA3rf0 - youtube",
"http://youtu.be/KID8HAU2eBA - youtube",
"http://youtu.be/_CL6n0FJZpk - youtube",
"http://vimeo.com/70486448 - youtube",
"http://youtu.be/HQPAN5dGbmc - youtube",
"http://youtu.be/Sqz5dbs5zmo - youtube",
"Be who you are and say what you feel, because those who mind don't matter, and those who matter don't mind. - Bernard M. Baruch",
"Be yourself; everyone else is already taken.  - Oscar Wilde",
"Two things are infinite: the universe and human stupidity; and I'm not sure about the universe. - Albert Einstein",
"So many books, so little time. - Frank Zappa",
"Be the change that you wish to see in the world. - Mahatma Gandhi",
"Live as if you were to die tomorrow. Learn as if you were to live forever - Mahatma Gandhi",
"Don't walk behind me; I may not lead. Don't walk in front of me; I may not follow. Just walk beside me and be my friend. - Albert Camus",
"If you tell the truth, you don't have to remember anything. - Mark Twain",
"Whenever you find yourself on the side of the majority, it is time to pause and reflect. - Mark Twain",
"A friend is someone who knows all about you and still loves you. - Elbert Hubbard",
"The first step toward success is taken when you refuse to be a captive of the environment in which you first find yourself - Mark Caine",
"I have not failed. I’ve just found 10,000 ways that won’t work. - Thomas A. Edison",
"A successful man is one who can lay a firm foundation with the bricks others have thrown at him. - David Brinkley",
"No one can make you feel inferior without your consent - Eleanor Roosevelt",
"The successful warrior is the average man, with laser-like focus. - Bruce Lee",
"If you don’t build your dream, someone else will hire you to help them build theirs - Dhirubhai Ambani",
"There are but two powers in the world, the sword and the mind. In the long run the sword is always beaten by the mind. - Napoleon Bonaparte",
"Stay hungry, Stay foolish. - Steve Jobs",
"We're here to put a dent in the universe. - Steve Jobs",
"Older people sit down and ask, 'What is it?' but the boy asks, 'What can I do with it? - Steve Jobs",
"If you live each day as it was your last, someday you'll most certainly be right.  - Steve Jobs"]

### Stage-1 ###
print "[+] Stage-1 ... "
n = 0x31
matrix_a = [] 
for i in range(len(strtab)) : 
	#print strtab[i], result[i] 		
	a = [struct.unpack('b', x)[0] for x in strtab[i].ljust(0x31, '\0')[:0x31]] 
	matrix_a.append( a )
key = numpy.matrix(matrix_a).I * numpy.matrix(result).T	

key = ''.join([ chr(int(round(x.item(0)))) for x in key ])
print "[>] 1st argument : ", key 

### Stage-2 ###
print "[+] Stage-2 ... "

# 0x804F280
table = [0, 1, 0, 1, 1, 1, 2, 4, 1, 3, 
1, 6, 2, 4, 5, 2, 16, 17, 0, 16, 
2, 14, 9, 1, 15, 9, 10, 14, 0, 15, 
17, 27, 4, 17, 14, 10, 5, 7, 13, 21, 
35, 9, 28, 25, 42, 23, 8, 45, 27]

numbers = range(n)
numbers.reverse()
ans = [0]*n
for i in range(n-1, -1, -1): 
	num = numbers[table[i]]
	ans[i]=num
	numbers.remove(num)
order = ans

# check 
#print '[>]', ''.join([ key[order.index(i)] for i in range(n)])

ans = 0 
for i in order[:0:-1] :
	ans += i
	ans *= n 
ans += order[0] 
order = str(ans)

print "[>] 2nd argument : ", order 

### run given file ### 
print "[+] run program ... "
target = "findkey_b2191f33d95fa6d2d0718efdbc78f8ae"
os.execv(target, (target, key, order)) 


