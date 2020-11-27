import scipy.stats as st
import tensorflow as tf
import numpy as np

'''smoother.py'''
def layer(op):
    def layer_decorated(self, *args, **kwargs):
        name = kwargs.setdefault('name', self.get_unique_name(op.__name__))
        layer_input = self.terminals[0]
        layer_output = op(self, layer_input, *args, **kwargs)
        self.layers[name] = layer_output
        self.feed(layer_output)
        return self
    return layer_decorated


class Smoother(object):
    def __init__(self, inputs, filter_size, sigma, heat_map_size=0):
        self.inputs = inputs  #{‘data’:self.tensor_heatMat_up}
        self.terminals = []   # []
        self.layers = dict(inputs) #{‘data’:self.tensor_heatMat_up}
        self.filter_size = filter_size   #25
        self.sigma = sigma      #3
        self.heat_map_size = heat_map_size   #0
        self.setup()    #

    def setup(self):
        self.feed('data').conv(name='smoothing')

    def get_unique_name(self, prefix):
        ident = sum(t.startswith(prefix) for t, _ in self.layers.items()) + 1
        return '%s_%d' % (prefix, ident)

    def feed(self, *args):
        assert len(args) != 0
        self.terminals = []
        for fed_layer in args:
            if isinstance(fed_layer, str):
                fed_layer = self.layers[fed_layer]
            self.terminals.append(fed_layer)
        return self

    def gauss_kernel(self, kernlen=21, nsig=3, channels=1):
        interval = (2*nsig+1.)/(kernlen)
        x = np.linspace(-nsig-interval/2., nsig+interval/2., kernlen+1)
        kern1d = np.diff(st.norm.cdf(x))
        kernel_raw = np.sqrt(np.outer(kern1d, kern1d))
        kernel = kernel_raw/kernel_raw.sum()
        out_filter = np.array(kernel, dtype = np.float32)
        out_filter = out_filter.reshape((kernlen, kernlen, 1, 1))
        out_filter = np.repeat(out_filter, channels, axis = 2)
        return out_filter

    def make_gauss_var(self, name, size, sigma, c_i):
        # with tf.device("/cpu:0"):
        kernel = self.gauss_kernel(size, sigma, c_i)
        var = tf.Variable(tf.convert_to_tensor(kernel), name=name)
        return var

    def get_output(self):
        '''Returns the smoother output.'''
        return self.terminals[-1]

    @layer
    def conv(self,
             input, #self.tensor_heatMat_up
             name,  # smoothing
             padding='SAME'):
        # Get the number of channels in the input
        if self.heat_map_size != 0:
            c_i = self.heat_map_size
        else:
            #input = Tensor("upsample_heatmat:0", shape=(?, ?, ?, 19), dtype=float32)
            c_i = input.get_shape().as_list()[3]   #c_i = 19
        # Convolution for a given input and kernel
        #深度可分离卷积
        convolve = lambda i, k: tf.nn.depthwise_conv2d(i, k, [1, 1, 1, 1], padding=padding)
        with tf.compat.v1.variable_scope(name) as scope:
            kernel = self.make_gauss_var('gauss_weight', self.filter_size, self.sigma, c_i)
            output = convolve(input, kernel)
        return output  #Tensor("smoothing/depthwise:0", shape=(?, ?, ?, 19), dtype=float32)
