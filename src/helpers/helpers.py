"""
Helper functions.
"""


def sequence_in(x, y, offset=0):
	"""
	Returns the start indices of sequences in list x that match list y.
	"""
	return [i+offset for i in range(0, len(x)-len(y)) if x[i:i+len(y)] == y]