#!/bin/bash
#SBATCH --killable
#SBATCH -c2
#SBATCH --time=2-0

export PYTHONPATH=$PYTHONPATH:"$(dirname "$(pwd)")"/Marabou

#--model test --input_path ./test_data/test_images.npy
python3 WatermarkVerification2.py --model mnist.w.wm --epsilon_max 100