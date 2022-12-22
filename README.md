# DistortionCorrection
Please reference https://easychair.org/publications/preprint/n6PL for any citation.
We propose a practical novel method to correct non-linear distortions in videos and single images, which we train a convolutional neural network (CNN) to recognize multiple distortions by estimating image structure. We first employed a VGG16 model to extract features to retain substantial pixels from input images. We designed a CNN, trained by annotated dataset to predict a window frame that visually defined the distortion. A drawing model uses network outputs to generate a grid fitting the window frame. The grid deforms to the corrected sample to render the final image. We use headless rendering mode to enhance correction speed and efficiency. Finally, the experimental results demonstrate that our algorithm outperforms other methods on both time assumption and accuracy.(see https://github. com/danielcyrus/DistortionCorrection)
