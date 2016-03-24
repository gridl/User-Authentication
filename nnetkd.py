import numpy as np
import random

class network(object):
	"""docstring for neural network"""

	def __init__(self, sizes):
		# sizes is an iterable indicating the number of neurons in each layer
		self.num_layers = len(sizes)
		self.sizes = sizes
		self.biases = [np.random.randn(y, ) for y in sizes[1:]]
		self.weights = [np.random.randn(y, x) for x, y in zip(sizes[:-1], sizes[1:])]

	def sigmoid(self, z):
		#activation function
		return 1.0/(1.0+np.exp(-z))

	def feed_forward(self, inp):
		#returns the final feed
		for bias, weight in zip(self.biases, self.weights):
			inp = self.sigmoid(np.dot(weight, inp)+bias)
		return inp

	def SGD(self, training_data, iterations, learning_rate):
		n = len(training_data)
		for j in range(iterations):
			random.shuffle(training_data)
			for unit_batch in training_data:
				self.update_unit_batch(unit_batch, learning_rate)

	def update_unit_batch(self, unit_batch, learning_rate):
		temp_b = [np.zeros(b.shape) for b in self.biases]
		temp_w = [np.zeros(w.shape) for w in self.weights]
		x, y = unit_batch
		delta_b, delta_w = self.backprop(x, y)
		temp_b = [tb+db for tb, db in zip(temp_b, delta_b)]
		temp_w = [tw+dw for tw, dw in zip(temp_w, delta_w)]
		self.weights = [w-(learning_rate)*tw 
						for w, tw in zip(self.weights, temp_w)]
		self.biases = [b-(learning_rate/1)*tb 
						for b, tb in zip(self.biases, temp_b)]

	def backprop(self, x, y):
		temp_b = [np.zeros(b.shape) for b in self.biases]
		temp_w = [np.zeros(w.shape) for w in self.weights]
		#forwarding input
		inp = x
		inp_list = [x] # list to store all the inputs, layer by layer
		output_layer = [] # list to store all the z vectors, layer by layer
		for b, w in zip(self.biases, self.weights):
			output = np.dot(w, inp)+b
			output_layer.append(output)
			inp = self.sigmoid(output)
			inp_list.append(inp)
		delta = self.cost_derivative(inp_list[-1], y) * self.sigmoid_prime(output_layer[-1])
		temp_b[-1] = delta
		temp_w[-1] = np.dot((np.array([delta])).transpose(), [inp_list[-2]])
		output = output_layer[-2]
		sp = self.sigmoid_prime(output)
		delta = np.dot(self.weights[-1].transpose(), delta) * sp
		temp_b[-2] = delta
		temp_w[-2] = np.dot((np.array([delta])).transpose(), [inp_list[-3]])
		return (temp_b, temp_w)

	def sigmoid_prime(self, z):
		return self.sigmoid(z)*(1-self.sigmoid(z))

	def cost_derivative(self, output_activations, y):
		return(np.array(output_activations)-np.array(y))

	def evaluate(self, test_data):
		test_results = [(np.argmax(self.feed_forward(x)), y) for (x, y) in test_data]
		return sum(int(x == y) for (x, y) in test_results)

training_data = list(zip(np.array([[12,21,3], [11, 20, 3]]), np.array([[0,1], [0,1]])))
net = network([3, 5, 2])
test_data = list(zip(np.array([[13,22,3]]), np.array([1])))
net.SGD(training_data, 10, 3.0) #train the neural network
print(net.evaluate(test_data))



