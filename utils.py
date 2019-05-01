import os
import sys
sys.path.insert(0,'..')
import uuid
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import backend as K
from tensorflow.python.framework import graph_util
from tensorflow.python.framework import graph_io
from tensorflow.keras.models import model_from_json

def load_model(json_path, model_path):
    # load json and create model
    json_file = open(json_path, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights(model_path)
    print("Loaded model from disk")
    return loaded_model

def splitModel(model_name):
    MODELS_PATH = '../Models'
    net_model = load_model(os.path.join(MODELS_PATH, model_name+'_model.json'), os.path.join(MODELS_PATH, model_name+'_model.h5'))
    print('\n------------------Model Summary------------------\n')
    print(net_model.summary())

    submodel = keras.Model(inputs=net_model.inputs, outputs=net_model.layers[-2].output, name='submodel-'+str(uuid.uuid4())[:5])
    print('\n------------------SubModel Summary------------------\n')
    print(submodel.summary())

    in_shape = (submodel.output.shape[1].value,)
    last_layer_in = keras.layers.Input(shape=in_shape, name='ll_input-'+str(uuid.uuid4())[:5])
    last_layer_model = keras.Model(inputs=last_layer_in, outputs=net_model.layers[-1](last_layer_in), name='lastlayer-'+str(uuid.uuid4())[:5])
    print('\n------------------Last Layer Summary------------------\n')
    print(last_layer_model.summary())
    print('\n------------------------------------------------------\n')

    return net_model, submodel, last_layer_model

def saveModelAsProtobuf(last_layer_model, model_name):
    sess = K.get_session()
    output_node_names = [node.name[:-2] for node in last_layer_model.outputs]
    constant_graph = graph_util.convert_variables_to_constants(sess, sess.graph.as_graph_def(), output_node_names)
    graph_io.write_graph(constant_graph, './ProtobufNetworks', '{}.pb'.format(model_name), as_text=False)
    print('Saved the model at: ', os.path.join('ProtobufNetworks', '{}.pb'.format(model_name)))

    filename = './ProtobufNetworks/{}.pb'.format(model_name)
    return filename