% P = phantom(128); 

lenna = imread('Lenna.png');

lenna = rgb2gray(lenna);

figure;

imshow(lenna);

theta = 0:179;

[R,xp] = radon(lenna,theta);

figure;

imshow(R,[],'Xdata',theta,'Ydata',xp,'InitialMagnification','fit');

imageInverseRadon = iradon(R,0:179);

figure;

imshow(imageInverseRadon, []);