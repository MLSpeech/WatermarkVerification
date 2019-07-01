# from nn_verification.utils import load_model
import numpy as np
import os
import tqdm
import argparse
import utils
from copy import deepcopy
from maraboupy import Marabou
from maraboupy import MarabouUtils
import MarabouNetworkTFWeightsAsVar
sat = 'SAT'
unsat = 'UNSAT'

class WatermarkVerification:

    def __init__(self, epsilon_max, epsilon_interval):
        self.epsilon_max = epsilon_max
        self.epsilon_interval = epsilon_interval

    def findEpsilonInterval(self, network, prediction):
        sat_epsilon = self.epsilon_max
        unsat_epsilon = 0.0
        sat_vals = None
        epsilon = sat_epsilon
        while abs(sat_epsilon - unsat_epsilon) > self.epsilon_interval:
            status, vals, out = self.evaluateEpsilon(epsilon, deepcopy(network), prediction)
            if status == sat:
                sat_epsilon = epsilon
                sat_vals = (status, vals, out)
            else:
                unsat_epsilon = epsilon
            epsilon = (sat_epsilon + unsat_epsilon)/2
        return unsat_epsilon, sat_epsilon , sat_vals


    def evaluateEpsilon(self, epsilon, network, prediction):
        outputVars = network.outputVars[0]
        vals = dict()
        for out in range(len(outputVars)):
            if out != prediction:
                vals[out] = self.evaluateSingleOutput(epsilon, deepcopy(network), prediction, out)
                if vals[out][0]:
                    return sat, vals, out
        return unsat, vals, -1


    def evaluateSingleOutput(self, epsilon, network, prediction, output):
        outputVars = network.outputVars[0]
        for k in network.matMulLayers.keys():
            n, m = network.matMulLayers[k]['vals'].shape
            print(n,m)
            for i in range(n):
                for j in range(m):
                    network.setUpperBound(network.matMulLayers[k]['epsilons'][i][j], epsilon)
                    network.setLowerBound(network.matMulLayers[k]['epsilons'][i][j], -epsilon)
            
        MarabouUtils.addInequality(network, [outputVars[prediction], outputVars[output]], [1, -1], 0)
        return network.solve(verbose=False)


    def run(self, model_name):
       
        filename = './ProtobufNetworks/last.layer.{}.pb'.format(model_name)

        out_file = open("WatermarkVerification1.csv", "w")
        out_file.write('unsat-epsilon,sat-epsilon,original-prediction,sat-prediction\n')
        out_file.flush()
        lastlayer_inputs = np.load('./data/{}.lastlayer.input.npy'.format(model_name))
        predictions = np.load('./data/{}.prediction.npy'.format(model_name))
        num_of_inputs_to_run = lastlayer_inputs.shape[0]
        # num_of_inputs_to_run = 20
        epsilons_vals = np.array([])
        for i in tqdm.tqdm(range(num_of_inputs_to_run)):
            print('******************************************8')
            prediction = np.argmax(predictions[i])
            inputVals = np.reshape(lastlayer_inputs[i], (1, lastlayer_inputs[i].shape[0]))
            network = MarabouNetworkTFWeightsAsVar.read_tf_weights_as_var(filename=filename, inputVals=inputVals)
            
            unsat_epsilon, sat_epsilon, sat_vals = self.findEpsilonInterval(network, prediction)
            out_file.write('{},{},{},{}\n'.format(unsat_epsilon, sat_epsilon, prediction, sat_vals[2]))
            out_file.flush()

            all_vals = sat_vals[1][max(sat_vals[1].keys())][0]
            newVars = np.array([[all_vals[network.epsilons[j][i]] for i in range(network.epsilons.shape[1])] for j in range(network.epsilons.shape[0])])
            self.outputVars = newVars if epsilons_vals==0 else np.append(epsilons_vals, newVars, axis=0)

        
        out_file.close()
        np.save('./data/wm.ver.1.{}.vals'.format(model_name), epsilons_vals)

    

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--model', help='the name of the model')
    parser.add_argument('--epsilon_max', default=1, help='max epsilon value')
    parser.add_argument('--epsilon_interval', default=0.01, help='epsilon smallest change')
    args = parser.parse_args()
    epsilon_max = float(args.epsilon_max)
    epsilon_interval = float(args.epsilon_interval)  
    model_name = args.model
    MODELS_PATH = './Models'
    problem = WatermarkVerification(epsilon_max, epsilon_interval)
    problem.run(model_name)