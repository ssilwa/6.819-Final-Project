# 6.819-Final-Project
Final Project for MIT 6.819

There are two steps to the project.

1) Preprocessing into a graph structure

- graphmaker.py takes an input image and outputs a graph structure where we can partition image -> lines -> words -> letters.

2) CNN for letter recognition
To do:
- train with EMNIST ByClass data |  lowercase, uppercase, digits
- train with EMNIST ByMerge data | digits, letters
data is 28 x 28 in .mat format


3) Models:
	1. Normal EMNIST Byclass- .867 test acc
	2. "Overfit" EMNIST Byclass (run 25 epochs) - .8707 acc
	3. "Deep" EMNIST Byclass (added 1 more conv2d layer) - 0.87019 acc
	4. "Overfit" "Deep" EMNIST Byclass (3. + 20 epochs) - 0.873214 acc


4) Current best model:
	labeled as "Overdeep_model.yaml", "overdeep_model.h5"
