#!/bin/bash
#SBATCH --time=7-0

export PYTHONPATH=$PYTHONPATH:"$(dirname "$(pwd)")"/Marabou

python3 WatermarkVerification3.py --model mnist.w.wm --epsilon_max 10 --num_of_inputs 4
# python3 WatermarkVerification2.py --model test --epsilon_max 100