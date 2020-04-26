import random
import nltk


# Ensure that seed_length >= statelen
def parse_tokens_simple(tokens, statelen):
	"""Parses a list of tokens as a map for a markov chain that uses the 
	previous statelen tokens as state"""

	# We need at least statelen+1 tokens to construct a state transition
	if not statelen < len(tokens):
		print("Token list needs to be longer:", tokens)
		return None

	# Create map to store state transitions
	markov_map = dict()
	for i in range(statelen, len(tokens)):
		# Build a tuple to represent the previous state
		tup = list()
		for j in range(statelen, 0, -1):
			tup.append(tokens[i-j])
		tup = tuple(tup)

		# Append this transition to the tuple's entry in the map
		if tup in markov_map:
			markov_map[tup].append(tokens[i])
		else:
			markov_map[tup] = [tokens[i]]
	return markov_map

def seed_tokens(tokens, seed_length):
	"""Generate a random list of 'seed' tokens: adjacent tokens that can be
	used to seed the chain"""

	# Check that the tokens and the seed_length have acceptable sizes
	if not seed_length < len(tokens):
		print("Text too short or seed_length too large")
		return None
	if not seed_length > 0:
		print("Seed_length too small")
		return None

	seed = random.randint(0, len(tokens)-seed_length)
	return tokens[seed:seed+seed_length]

def create_list(seed_list, markov_map, state_len, list_size):
	"""Use seed_list to create a list of length list_size based on the markov
	model with state length state_len represented by markov_map"""

	# Expand lst to list_size
	lst = seed_list
	for i in range(list_size-len(seed_list)):
		state = tuple(lst[-state_len:])
		if state not in markov_map:
			break
		lst.append(random.choice(markov_map[state]))
	return lst


if __name__ == "__main__":
	f = open("jane_eyre.txt")
	text = f.read()
	f.close()
	tokens = nltk.word_tokenize(text)
	# tokens = nltk.word_tokenize("The cat in the hat \n ate a fat rat on the mat.")

	l = 4
	simple_map = parse_tokens_simple(tokens, l)
	# print(simple_map)
	seed = seed_tokens(tokens, l)
	# print(seed)
	gen = create_list(seed, simple_map, l, 100)
	print(' '.join(gen), ".")