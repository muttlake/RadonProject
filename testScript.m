% This is a project
% Bro


v = [32, 44, 55];

lenna = imread('Lenna.png');

size(lenna)

lenna = rgb2gray(lenna);

size(lenna)

figure;

imshow(lenna);

inputImage = [];

size(inputImage)

colorMap = gray(256);

testImage = zeros(256, 256);

[rows, cols] = size(testImage);

numberOfFrames = 256
vidHeight = 256
vidWidth = 258

allTheFrames = cell(numberOfFrames,1);
allTheFrames(:) = {zeros(vidHeight, vidWidth, 3, 'uint8')};
allTheColorMaps = cell(numberOfFrames,1);
allTheColorMaps(:) = {zeros(256, 3)};
newMovie = struct('cdata', allTheFrames, 'colormap', allTheColorMaps)

for frame = 1:numberOfFrames
    row = frame
    for col = 1:cols
        testImage(row, col) = 255;
    end
    imwrite(testImage, 'testImage.png');
    thisFrame = imread('testImage.png');
    newMovie(frame) = im2frame(thisFrame);
end

