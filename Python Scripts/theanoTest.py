import theano
import theano.tensor as T
import theano.tensor.nnet as nnet
import numpy as np

'''
#define symbolic expressions
x = T.dscalar()

fx = T.exp(T.sin(x**2))

print(type(fx)) #out: theano.tensor.var.TensorVariable

f = theano.function(inputs = [x], outputs = [fx])

print (f(10))

#Theano autodifferentiation

fp = T.grad(fx, wrt=x) #wrt means with respect to so we are differentiating with respect to x
fprime = theano.function([x], fp)

print(fprime(15))
'''

###XOR network implementation
x = T.dvector()
y = T.dscalar()

def layer(x, w):
	b = np.array([1], dtype=theano.config.floatX)
	new_x = T.concatenate([x, b])
	m = T.dot(w.T, new_x) #theta1: 3x3 * x: 3x1 = 3x1 ;;; theta2: 1x4 * 4x1
	h = nnet.sigmoid(m)
	return h
	
def grad_desc(cost, theta):
	alpha = 0.1 #learning rate
	return theta - (alpha * T.grad(cost, wrt=theta))
	
theta1 = theano.shared(np.array(np.random.rand(3,3), dtype=theano.config.floatX))
theta2 = theano.shared(np.array(np.random.rand(4,1), dtype=theano.config.floatX))

hid1 = layer(x, theta1) #hidden layer
out1 = T.sum(layer(hid1, theta2)) #output layer
fc = (out1 - y)**2 #cost expression

#updates allows shared variables to be updated via an expression
#The update format takes a tuple of 2 values with the format (shared_variable, update_value)
cost = theano.function(inputs=[x, y], 
							outputs=fc, 
							updates=[(theta1, grad_desc(fc, theta1)), 
							(theta2, grad_desc(fc, theta2))])
run_forward = theano.function(inputs=[x], outputs=out1)

# Create some test data
inputs = np.array([[0,1],[1,0],[1,1],[0,0]]).reshape(4,2) #training data X
exp_y = np.array([1, 1, 0, 0]) #training data Y (exp_y means expected output)

#function train
def train_model(inputs, exp_y, tolerance, max_iterations = 10000):
	cur_cost = 1 #initialise at arbitrary value
	i = 0
	while(i < max_iterations and cur_cost > tolerance):
		for k in range(len(inputs)):
			cur_cost = cost(inputs[k], exp_y[k]) #call out theano-compiled cost function on, it will auto update weights
			if (i % 500 == 0): #only print the cost every 500 epochs/iterations (to save space)
				print('Cost: %s' %(cur_cost,))
		i += 1		
		
train_model(inputs, exp_y, 0.001, max_iterations = 100000)		
		
#Testing trained data
print(run_forward([0,1]))
print(run_forward([1,1]))
print(run_forward([1,0]))
print(run_forward([0,0]))