
# BAFFLE - Bionic Apparatus For Fluorescent Light Estimation

Repository for: "A 3D printable device for macroscopic quantification of fluorescently-tagged bacteria in space and time".


## Overview

Here you can find the hardware design files, code and materials for assemblying a low cost and open source opto-mechanical device with the aim of acquiring multi-channel time-lapse images of bacterial colonies growing in agar plates.  

This device uses a system of addressable LEDs and fluorescence filters to estimate the spatio-temporal distribution of different fluorescently-tagged sub-populations from time-lapse images obtained using a standard DSLR camera with a macro lens.
## Getting Started

You can see the full project in the pre-print manuscript at Biorxiv[a link].

### Prerequisites

To assemble this device you need access to a laser cutter and a 3D printer. You also need PC and a digital camera. The complete list of materials, electronics and parts can be found at [link a excel file].

### Installing

*Create a Conda Environment:

conda create --name baffle

conda activate baffle

conda pip install

*Install Libraries:

pip install dash

pip install dash-bootstrap-components

pip install dash-daq

pip install Phidget22

pip install pandas

pip install pyserial


*Enable USB Port in Linux:

sudo chmod a+rw /dev/ttyUSB*

### Running the equipment

The project includes some python codes to control the hardware via a dedicated GUI that runs in a web browser.

- /BAFFLE/code/app.py 


## Authors

- [@Systems Biology Lab, CCG-UNAM](https://github.com/ccg-esb-lab)


## License

[MIT](https://choosealicense.com/licenses/mit/)

This project is licensed under the MIT License - see the LICENSE.txt file for details. Hardware is lincesed under the CERN license.


## Aknowledgements

We thank the help and input from past and present members of the Systems and Synthetic Laboratory at CCG-UNAM.
