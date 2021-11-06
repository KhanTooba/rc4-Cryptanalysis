from os import truncate
import random
import numpy as np
import csv

def countBits(text):
    zero=0
    one=0
    for i in range(len(text)):
        if text[i]==0:
            zero=zero+1
        else:
            one=one+1
    return zero, one

def encryption(key):
	key_list=[]
	S=[]
	pt=[]
	key_stream=[]
	# print("Plain text : ", plain_text)
	# print("Key : ", key)
	# print("n : ", n)

	# print(" ")
	n1=2**b1
	# The initial state vector array
	S = [i for i in range(0, n1)]
	# print("S : ", S)

	key_list = [key[i:i + n1] for i in range(0, len(key), n1)]

	# Convert to key_stream to decimal
	for i in range(len(key_list)):
		key_list[i] = int(key_list[i], 2)

	# Making key_stream equal
	# to length of state vector
	diff = int(len(S)-len(key_list))

	if diff != 0:
		for i in range(0, diff):
			key_list.append(key_list[i])

	# print("Key list : ", key_list)
	# print(" ")

	# print("KSA iterations : ")
	# print(" ")
	j = 0
	N = len(S)
		
	for i in range(0, N):
		j = (j + S[i]+key_list[i]) % N
		S[i], S[j] = S[j], S[i]
		# print(i, " ", end ="")
			
		# print(S)

	initial_permutation_array = S
		
	# Perform PGRA algorithm

	# print("PGRA iterations : ")
	# print(" ")
	N = len(S)
	i = j = 0
	key_stream = []
	y=int(2**(n)/8)
	for k in range(0, y):
		i = (i + 1) % N
		j = (j + S[i]) % N
			
			# Update S[i] and S[j]
		S[i], S[j] = S[j], S[i]
		# print(k, " ", end ="")
		# print(S)
		t = (S[i]+S[j]) % N
		key_stream.append(S[t])

		# Print the key stream
	# print("Key stream : ", key_stream)
	# print(" ")
	key_to_bits = ""
	for i in key_stream:
		key_to_bits += '0'*(8-len(bin(i)[2:]))+bin(i)[2:]
	return key_to_bits

def flipBits(text, index):
	position = index
	new_character = '0'
	
	if text[position]=='0':
		new_character = '1'
	#print(text)
	text = text[:position] + new_character + text[position+1:]
	return text

def flipCounter(text, p):
	p=random.randint(0,2**n-1)
	text=flipBits(text, p)
	return text

def convert(num):
	d=int(num,2)
	return d

def counter(text):
	c=[0] * (2**b)
	for i in range(len(text)-b):
		temp_text=text[i:i+b]
		d=convert(temp_text)
		c[d]=c[d]+1
	return c

def main(k1, k2, f1, f2):
	text=k2
	# fields=["number of bits","1st","2nd"]
	rows=[]
	for i in range(1,33):
		text=flipCounter(text, i)
		encrypted1 = encryption(k1)
		#print("Cipher text with key1: ",encrypted1)

		encrypted2 = encryption(text)
		#print("Cipher text with key2: ",encrypted2)
		xored = []
		for j in range(len(encrypted1)):
				c = int(encrypted1[j]) ^ int(encrypted2[j])
				xored.append(c)
		#print(xored)

		zero, one=countBits(xored)

		c=counter(text)
		# print(c)
		numberSamples=(2**n)
		numberCounters=(2**b)
		stdDev=np.std(c)
		R=(numberCounters*stdDev)/numberSamples
		# print(zero)
		# print(one)

		# print("With ",i,"bits flipped: ",round(one*100/(zero+one),2)," with Randomness: ",round(R,4))
		t=[i,round(one*100/(zero+one),2)]
		rows.append(t)
	
	with open("graph2.csv", 'w') as csvfile: 
    # creating a csv writer object 
		csvwriter = csv.writer(csvfile) 	
		# writing the fields 
		#csvwriter.writerow(fields) 
		# writing the data rows 
		csvwriter.writerows(rows)
	
def main2(k1, k2, f1, f2):
	text=k2
	# fields=["number of bits","1st","2nd"]
	encrypted1 = encryption(k1)
	#print(encrypted1)
	rows=[]
	for i in range(1,33):
		#print("For value of i:",i)
		text=flipCounter(text, i)
		encrypted2 = encryption(text)
		#print("Cipher text with key1: ",encrypted1)
		#print(encrypted2)
		
		#print("Cipher text with key2: ",encrypted2)
		xored = []
		for j in range(len(encrypted1)):
				c = int(encrypted1[j]) ^ int(encrypted2[j])
				xored.append(c)
		#print(xored)

		zero, one=countBits(xored)

		c=counter(text)
		# print(c)
		numberSamples=(2**n)
		numberCounters=(2**b)
		stdDev=np.std(c)
		R=(numberCounters*stdDev)/numberSamples
		# print(zero)
		# print(one)

		#print("With ",i,"bits flipped: ",round(one*100/(zero+one),2)," with Randomness: ",round(R,4)," Standard Deviation: ", stdDev)
		t=round(one*100/(zero+one),2)
		rows.append(t)
	
	rows2=[]
	x=0
	# print(len(rows))
	with open(f1, mode ='r')as file: 
		# reading the CSV file 
		csvFile = csv.reader(file) 	
		# displaying the contents of the CSV file 
		for lines in csvFile: 
				lines.append(rows[x])
				# print(x)
				x=x+1
				rows2.append(lines)

	with open(f2, 'w') as csvfile: 
    # creating a csv writer object 
		csvwriter = csv.writer(csvfile) 	
		csvwriter.writerows(rows2)
	
"""
Declarartion of all usefull variables and calling main.
"""
data=open("keys.txt",'r').readlines()
plain_text=data[0].rstrip()
k1=data[1].rstrip()
n = 11
b1 = 7
plain_text=plain_text[0:(2**b1)]*(2**(n-b1))
k1=k1[0:(2**b1)]*(2**(n-b1))

k2=k1
# print(len(k1))
# print(len(plain_text))

b=8
f1="graph.csv"
f2="graph2.csv"
main(k1,k2,f1,f2)
for j in range(30):
	f1, f2= f2, f1
	print("Interation: ",j+1)
	main2(k1, k2, f1, f2)
	