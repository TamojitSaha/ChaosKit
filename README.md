<h1 align="center"> ChaosKit </h1> <br>

## About
[![Build Platforms](https://img.shields.io/badge/build_platform-Python2.7-3776AB.svg)](https://www.python.org/download/releases/2.7/)
[![Dependency](https://img.shields.io/badge/dependency-OpenCV-red.svg)](https://pypi.python.org/pypi/opencv-python)
<br>
The Chaos Kit comprises of all the necessary python scripts for embedding information inside an image in a way that it goes unnoticed even with the Virtual Steganography Tool ([VSL](http://vsl.sourceforge.net/)).<br>
[Here](https://doi.org/10.1109/ICRCICN.2017.8234536) is the link to the IEEE publication based on the this work.

## Concept Flow
<p align="center"><img src="./CFD.png" heigth="473" width="488"> &nbsp </p>

## Usage
  - Download all the file as zip from [here](https://github.com/TamojitSaha/ChaosKit/archive/0.0.1.zip)
  - After install Python and running ```pip install opencv-python``` open ["<i>steganography.py</i>"](./steganography.py). <b>Dont run it now!</b>
  - Make a text file named "<i>msg.txt</i>" in the same directory and put your own message.  For [this particular image](./image.tiff?raw=true), the message file should be less than <b>8kb</b>. 
  - The default password is ```-1, 2.01, 3 ```. Refer to <i><b>line 127</b></i> and <i><b>line 230</b></i> of ["<i>steganography.py</i>"](./steganography.py) to embed and decipher respectively. 
  <br>You can change the password if you want but it is recommended that do not put infinite huge numbers for e.g. ```25,45.001,3547 ```. 
  <br>Example password: ``` -3.12457863, 5.14785236997, 0.00012364478```
  - All paswwords parameters are double-precision floating point resulting a <b>192 bits</b> key length.
  - Now you can run the file and look for <b><i>image_encoded.tiff</i></b> file in the same directory.
  
## Authors
[![ID](https://img.shields.io/badge/id-Tamojit-54C7EC.svg?style=for-the-badge)](https://www.linkedin.com/in/tamojit-saha/)<br>
[![ID](https://img.shields.io/badge/id-Sandeepan-54C7EC.svg?style=for-the-badge)](https://www.linkedin.com/in/sandeepan-sengupta/)<br>
[![ID](https://img.shields.io/badge/id-Tanmoy-54C7EC.svg?style=for-the-badge)]( https://www.researchgate.net/profile/Tanmoy_Dasgupta)

## Feedback
You can always open a [issue](https://github.com/TamojitSaha/ChaosKit/issues/new) if you find any bug.
