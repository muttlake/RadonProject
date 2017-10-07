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

% numberOfFrames = 256
% vidHeight = 256
% vidWidth = 258
% 
% allTheFrames = cell(numberOfFrames,1);
% allTheFrames(:) = {zeros(vidHeight, vidWidth, 3, 'uint8')};
% allTheColorMaps = cell(numberOfFrames,1);
% allTheColorMaps(:) = {zeros(256, 3)};
% newMovie = struct('cdata', allTheFrames, 'colormap', allTheColorMaps)
% 
% for frame = 1:numberOfFrames
%     row = frame
%     for col = 1:cols
%         testImage(row, col) = 255;
%     end
%     imwrite(testImage, 'testImage.png');
%     thisFrame = imread('testImage.png');
%     newMovie(frame) = im2frame(thisFrame);
% end


for k = 1:16
	plot(fft(eye(k+16)))
	axis([-1 1 -1 1])
	M(k) = getframe;
end

figure
movie(M,5)

figure
u = uicontrol('Style','slider','Position',[10 50 20 340],...
    'Min',1,'Max',16,'Value',1);
for k = 1:16
    plot(fft(eye(k+16)))
    axis([-1 1 -1 1])
    u.Value = k;
    M(k) = getframe(gcf);
end

figure
axes('Position',[0 0 1 1])
movie(M,5)











