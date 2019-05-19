Russian OCR (an exercise project)
============

## Installation and dependencies

Dependencies are managed with `pipenv`. 

The first you need is a text file of Russian text. This model was trained with this Russian News Corpus, which you can get from [here](https://github.com/maxoodf/russian_news_corpus). You can also download the generated training data from [here]()

The code to compare against Tesseract is located  in `test` directory. To run it, you need to install Tesseract 4 properly. See [this](https://pypi.org/project/tesserocr/) for more information.

## Running

The model can be trained at Google Colaboratory.

Once you have installed the pipenv dependencies, you can activate the virtualenv with:

    pipenv shell


To make a prediction on your own machine, run `predict.py`
like following:

```
python predict.py --model <path/to/model> predict_this.png
```

NOTE: The input must be a grayscale image with the height of 32 pixels. While `compare_tesseract.py` and **the training** cannot handle JPEG files, they should work fine with `predict.py`.

To generate training data yourself

To run automated comparison against Tesseract, go to `test` directory, and run the following:

```
python compare_tesseract.py -m <path/to/model> <input_directory>
```

The content of the directory can be generated with

Each image in the input_directory must be a PNG file, and must have a corresponding .gt.txt file, which contains the ground truth. For example, if there exists an image with the name `1.png`, there must also be a file `1.gt.txt`. 

## License

Apache 2.0
