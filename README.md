# IT-AIoT-Project
AIoT Project : Vision checking based on object detection

Evaluate method:
1. Recognize with Convolution Neural Network
    - video processed by openCV, make MHI(Motion History Image)
    - modelling with CNN
2. Pure openCV image processing
    - extract hand with HSV fiteruing
    - shape detecting(round, retangle,...)
3. Object detection NN - YOLO
    - detect location of hand
