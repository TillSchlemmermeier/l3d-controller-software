'''
see
http://effbot.org/pyfaq/how-do-i-share-global-variables-across-modules.htm
'''
import numpy as np

global_parameter = np.zeros(255)
global_label = np.array([['parameter', 'number'] in range(100)])
