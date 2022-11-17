# ClassiPy

ClassiPy is a simple proof of concept to use a Multi Layer Perceptron neural network form scikit-learn to detect the letter being drawn in the window.

Be aware that the training data is very biased to my own writing, and several times it can get my writing wrong, so your mileage may vary.

## Installation

ClassiPy is a executable. Simply double click "ClassiPy" to run it.

If you want to run the scripts with python, then you need to:

```bash
pip install scikit-learn
pip install pickle
pip install pandas
pip install pygame
```

## Usage

After opening the application, simply draw a letter in the window by clicking and dragging the mouse.

After drawing, press the "Predict" button to let the neural network try to guess the letter drawn.
A result will appear in the far right box as "Predict: C".

To predict again, press "Clear", and repeat the process.

## Debug mode

To activate debug mode, set DEBUG_ACTIVE to True.

## License

[GNU AGPLv3](https://choosealicense.com/licenses/agpl-3.0/)