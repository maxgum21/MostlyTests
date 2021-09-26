import numpy as np

np.random.seed(0)


class Layer:
    def __init__(self, n_inputs, n_neurons):
        self.weights = 0.1 * np.random.randn(n_inputs, n_neurons)
        self.biases = np.zeros((1, n_neurons))

    def forward(self, inputs):
        self.output = np.dot(inputs, self.weights) + self.biases


class ReLU:
    def forward(self, inputs):
        self.output = np.maximum(0, inputs)


class SoftMax:
    def forward(self, inputs):
        exp = np.exp(inputs - np.max(inputs, keepdims=True, axis=1))
        self.output = exp / np.sum(exp, axis=1, keepdims=True)


X = [[1, 2, 3, 2.5],
     [2.0, 5.0, -1.0, 2.0],
     [-1.5, 2.7, 3.3, -0.8]]

l1 = Layer(4, 5)
a_relu = ReLU()
l2 = Layer(5, 3)
a_smax = SoftMax()

l1.forward(X)
a_relu.forward(l1.output)
l2.forward(a_relu.output)
a_smax.forward(l2.output)
print(a_smax.output)