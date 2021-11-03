from keyGeneration import *

# Function for decryption of data
def decryption():

	# The initial state vector array
	S = [i for i in range(0, 2**n)]

	key_list = [key[i:i + n] for i in range(0, len(key), n)]

	# Convert to key_stream to decimal
	for i in range(len(key_list)):
		key_list[i] = int(key_list[i], 2)

	# Convert to plain_text to decimal
	global pt

	pt = [plain_text[i:i + n] for i in range(0, len(plain_text), n)]

	for i in range(len(pt)):
		pt[i] = int(pt[i], 2)

	# making key_stream equal
	# to length of state vector
	diff = int(len(S)-len(key_list))

	if diff != 0:
		for i in range(0, diff):
			key_list.append(key_list[i])

	print(" ")

	# KSA algorithm
	def KSA():
		j = 0
		N = len(S)
		
		# Iterate over the range [0, N]
		for i in range(0, N):
			j = (j + S[i]+key_list[i]) % N
			
			# Update S[i] and S[j]
			S[i], S[j] = S[j], S[i]
			print(i, " ", end ="")
			print(S)

		initial_permutation_array = S
		print(" ")
		print("The initial permutation array is : ",
			initial_permutation_array)

	print("KSA iterations : ")
	print(" ")
	KSA()
	print(" ")

	# Perform PRGA algorithm
	def do_PGRA():

		N = len(S)
		i = j = 0
		global key_stream
		key_stream = []

		# Iterate over the range
		for k in range(0, len(pt)):
			i = (i + 1) % N
			j = (j + S[i]) % N
			
			# Update S[i] and S[j]
			S[i], S[j] = S[j], S[i]
			print(k, " ", end ="")
			print(S)
			t = (S[i]+S[j]) % N
			key_stream.append(S[t])

	print("Key stream : ", key_stream)
	print(" ")

	print("PGRA iterations : ")
	print(" ")
	do_PGRA()

	# Perform XOR between generated
	# key stream and cipher text
	def do_XOR():
		global original_text
		original_text = []
		for i in range(len(cipher_text)):
			p = key_stream[i] ^ cipher_text[i]
			original_text.append(p)

	do_XOR()

	# convert the decrypted text to
	# the bits form
	decrypted_to_bits = ""
	for i in original_text:
		decrypted_to_bits += '0'*(n-len(bin(i)[2:]))+bin(i)[2:]

	print(" ")
	print("Decrypted text : ",
		decrypted_to_bits)

# Driver Code
decryption()

