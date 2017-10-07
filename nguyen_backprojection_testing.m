clear all; close all; clc;
I = imread('Lenna.png');
I = rgb2gray(I);
% Define angle resolution (in degree)
ang_res = 4;
theta = 0:ang_res:180-ang_res;
[R,xp] = radon(I,theta);
figure('Color', 'w'),  imagesc(theta,xp,R)
colormap(hot), colorbar
title('Projections of the 3 objects with sharp edges')
xlabel('Parallel Rotation Angle - \theta (degrees)')
ylabel('Parallel Sensor Position - x\prime (pixels)')

figure;
R = radon(I,0:175);
I1 = iradon(R,0:175);
I2 = iradon(R,0:175,'linear','none');
subplot(1,3,1), imshow(I), title('Original of 3 objects with sharp edges')
subplot(1,3,2), imshow(I1), title('Filtered backprojection of 3 objects with sharp edges')
subplot(1,3,3), imshow(I2,[]), title('Unfiltered backprojection of 3 objects with sharp edges')
%% Minh Anh Nguyen
%% filtered baclkprojection testing extra credit
clear all; close all; clc;
I = imread('Lenna.png');
I = rgb2gray(I);

figure, subplot (3,2,1),imshow(I), hold off, title('The original image of image 2')
subplot(2,3,1); imagesc(I);
title('3 shape'); xlabel('X'); ylabel('Y');
% set some parameters
freq = 1; % [1/degree];
thetas = 0:1/freq:180-1/freq; subplot(2,3,2)
% compute sinogram with matlab function
sinogram = radon(I,thetas);
imagesc(sinogram); title('Sinogram')
xlabel('\alpha'); ylabel('# parallel projection'); subplot(2,3,3)
% % simple backprojection (schlegel & bille 9.1.2)
%%http://www.mathworks.com/matlabcentral/fileexchange/34608-ct-reconstruction-package/content/ctRecontruction/myBackprojection.m
% figure out how big our picture is going to be.
ParallelProjections = size(sinogram,1);
AngularProjections  = length(thetas);
% convert thetas to radians
thetas = (pi/180)*thetas;
% set up the backprojected image
 backprojected = zeros(ParallelProjections,ParallelProjections);


% find the middle index of the projections
midindex = floor(ParallelProjections/2) + 1;
% set up the coords of the image
[xCoords,yCoords] = meshgrid(ceil(-ParallelProjections/2):ceil(ParallelProjections/2-1));
% set up filter: now for the spatial domain!!!
filterMode = 'sheppLogan'; % put either 'sheppLogan' or 'ramLak'

if mod(ParallelProjections,2) == 0
    halfFilterSize = floor(1 + ParallelProjections);
else
    halfFilterSize = floor(ParallelProjections);
end

if strcmp(filterMode,'ramLak')
    filter = zeros(1,halfFilterSize);
    filter(1:2:halfFilterSize) = -1./([1:2:halfFilterSize].^2 * pi^2);
    filter = [fliplr(filter) 1/4 filter];
elseif strcmp(filterMode,'sheppLogan')
    filter = -2./(pi^2 * (4 * (-halfFilterSize:halfFilterSize).^2 - 1) );
end

% loop over each projection
for i = 1:AngularProjections

    % figure out which projections to add to which spots
    rotCoords = round(midindex + xCoords*sin(thetas(i)) + yCoords*cos(thetas(i)));

    % check which coords are in bounds
    indices   = find((rotCoords > 0) & (rotCoords <= ParallelProjections));
    newCoords = rotCoords(indices);
    % filter
    filteredProfile = conv(sinogram(:,i),filter,'same');

    % summation
     backprojected(indices) =  backprojected(indices) + filteredProfile(newCoords)./AngularProjections;
   
    % visualization on the fly
    imagesc( backprojected); title('backprojection without using iradon');
    drawnow

end


% % find the middle index of the projections
midindex = floor(size(backprojected,1)/2) + 1;

%
% % prepare filter for frequency domain without normalization
[xCoords,yCoords] = meshgrid(1 - midindex:size(backprojected,1) - midindex);
rampFilter2D      = sqrt(xCoords.^2 + yCoords.^2);
%
% % 2 D Fourier transformation and sorting
 reconstrution2DFT = fftshift(fft2(backprojected));
 % % Filter in Freq Domain
 reconstrution2DFT = reconstrution2DFT .* rampFilter2D;
 
% % inverse 2 D fourier transformation and sorting
 reconstrution2DFT = real( ifft2( ifftshift( reconstrution2DFT )));
%  figure
% imagesc(reconstrution2DFT);
% title('Filtered backprojection with ifft2( ifftshift()) function orginal background')
% xlabel('X'); ylabel('Y');

b4= mat2gray(reconstrution2DFT );
subplot(2,3,4); imshow(b4);title('filter backproject image using ifft2(ifftshift()) with gray background');

