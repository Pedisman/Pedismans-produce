import numpy as np
import sklearn
import sklearn.datasets
import theano
import theano.tensor as T
import time

# Use float32 as the default float data type
theano.config.floatX = 'float32'

# Generate a dataset
np.random.seed(0)
digits = sklearn.datasets.load_digits()
train_X = digits.images

train_X = train_X.reshape(len(train_X), 64) #shape the input vector to be single row

train_y = digits.target
train_X = train_X.astype(np.float32)
train_y = train_y.astype(np.int32)
train_y_onehot = np.eye(10)[train_y]

print(train_X[0])

def maxPixel(input):
	max = 0
	for image in input:
		for pixel in image:
			if (pixel > max):
				max = pixel
	return max

def scalePixels(input, scaleFactor):
	for i, image in enumerate(input):
		for j, pixel in enumerate(image):
			input[i][j] = pixel/scaleFactor
	return input
	
max = maxPixel(train_X)
print(max)

train_X = scalePixels(train_X, max)

max = maxPixel(train_X)
print(max)
		
print(train_X[0])
print(train_y[0])
print(train_y_onehot[0])

# Size definitions
num_examples = len(train_X) # training set size
nn_input_dim = 64 # input layer dimensionality
nn_output_dim = 10 # output layer dimensionality
nn_hdim = 250 # hidden layer dimensionality

# Gradient descent parameters (I picked these by hand)
epsilon = np.float32(0.01) # learning rate for gradient descent
reg_lambda = np.float32(0.01) # regularization strength 

# GPU NOTE: Conversion to float32 to store them on the GPU!
X = theano.shared(train_X.astype('float32')) # initialized on the GPU
y = theano.shared(train_y_onehot.astype('float32'))

# GPU NOTE: Conversion to float32 to store them on the GPU!
W1 = theano.shared(np.random.randn(nn_input_dim, nn_hdim).astype('float32'), name='W1')
b1 = theano.shared(np.zeros(nn_hdim).astype('float32'), name='b1')
W2 = theano.shared(np.random.randn(nn_hdim, nn_output_dim).astype('float32'), name='W2')
b2 = theano.shared(np.zeros(nn_output_dim).astype('float32'), name='b2')

# Forward propagation
z1 = X.dot(W1) + b1
a1 = T.tanh(z1)
z2 = a1.dot(W2) + b2
y_hat = T.nnet.softmax(z2)

# The regularization term (optional)
loss_reg = 1./num_examples * reg_lambda/2 * (T.sum(T.sqr(W1)) + T.sum(T.sqr(W2))) 
# the loss function we want to optimize
loss = T.nnet.categorical_crossentropy(y_hat, y).mean() + loss_reg
# Returns a class prediction
prediction = T.argmax(y_hat, axis=1)

# Gradients
dW2 = T.grad(loss, W2)
db2 = T.grad(loss, b2)
dW1 = T.grad(loss, W1)
db1 = T.grad(loss, b1)

# Note that we removed the input values because we will always use the same shared variable
# GPU NOTE: Removed the input values to avoid copying data to the GPU.
forward_prop = theano.function([], y_hat)
calculate_loss = theano.function([], loss)
predict = theano.function([], prediction)

# GPU NOTE: Removed the input values to avoid copying data to the GPU.
gradient_step = theano.function(
    [],
    # profile=True,
    updates=((W2, W2 - epsilon * dW2),
             (W1, W1 - epsilon * dW1),
             (b2, b2 - epsilon * db2),
             (b1, b1 - epsilon * db1)))

def build_model(num_passes=20000, print_loss=False, print_freq = 1000):
    # Re-Initialize the parameters to random values. We need to learn these.
	np.random.seed(0)
	# GPU NOTE: Conversion to float32 to store them on the GPU!
	W1.set_value((np.random.randn(nn_input_dim, nn_hdim) / np.sqrt(nn_input_dim)).astype('float32'))
	b1.set_value(np.zeros(nn_hdim).astype('float32'))
	W2.set_value((np.random.randn(nn_hdim, nn_output_dim) / np.sqrt(nn_hdim)).astype('float32'))
	b2.set_value(np.zeros(nn_output_dim).astype('float32'))
	
	# Gradient descent. For each batch...
	for i in xrange(0, num_passes):
		# This will update our parameters W2, b2, W1 and b1!
		gradient_step()
		
        # Optionally print the loss.
        # This is expensive because it uses the whole dataset, so we don't want to do it too often.
		if print_loss and i % print_freq == 0:
			print "Loss after iteration %i: %f" %(i, calculate_loss())

x = theano.tensor.fvector('x')

ultimateFunction = theano.function([x], T.nnet.softmax(T.tanh(x.dot(W1) + b1).dot(W2) + b2))	
			
# Profiling
'''
theano.config.profile = True
theano.config.profile_memory = True
gradient_step()
theano.printing.debugprint(gradient_step) 
print gradient_step.profile.summary()
'''

'''
x = theano.tensor.fvector('x')
run_forward = theano.function(inputs=[x], outputs=y_hat)
'''
    
#%timeit gradient_step()
###GPU: 297.894996502

function_timed = build_model

start= time.clock()
function_timed(print_loss = True, print_freq=500)
end= time.clock()
print(end-start)

'''
print(run_forward([  0,   0,   5,  13,   9,   1,   0,  0,  0,   0,  13,  15,  10,  15,   5,
   0,   0,   3,  15,   2,   0,  11,   8,   0,   0,   4,  12,   0,   0,   8,
   8,   0,   0,   5,   8,   0,   0,   9,   8,   0,   0,   4,  11,   0,   1,
  12,   7,   0,   0,   2,  14,   5,  10,  12,   0,   0,   0,   0,   6,  13,
  10,   0,   0,   0]), train_Y[0])
'''
print(ultimateFunction(train_X[23]), train_y[23])
print(ultimateFunction(train_X[100]), train_y[100])
print(ultimateFunction(train_X[160]), train_y[160])
print(ultimateFunction(train_X[300]), train_y[300])
print(ultimateFunction(train_X[1000]), train_y[1000])

'''
print(predict(train_X[2]), train_Y[2])
print(predict(train_X[3]), train_Y[3])
print(predict(train_X[4]), train_Y[4])
print(predict(train_X[5]), train_Y[5])
print(predict(train_X[6]), train_Y[6])
print(predict(train_X[7]), train_Y[7])
print(predict(train_X[8]), train_Y[8])
'''