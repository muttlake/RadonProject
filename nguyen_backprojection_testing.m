%% Minh Anh Nguyen
%% filtered baclkprojection testing extra credit

I = imread('Lenna.png');
I = rgb2gray(I);

% set some parameters
freq = 1; % [1/degree];
thetas = 0:1/freq:180-1/freq;
% compute sinogram with matlab function
sinogram = radon(I,thetas);
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
    % imagesc( backprojected); title('backprojection without using iradon');
    % drawnow

end


% % find the middle index of the projections
midindex = floor(size(backprojected,1)/2) + 1;


% % prepare filter for frequency domain without normalization
[xCoords,yCoords] = meshgrid(1 - midindex:size(backprojected,1) - midindex);
rampFilter2D      = sqrt(xCoords.^2 + yCoords.^2);

% % 2 D Fourier transformation and sorting
reconstruction2DFT = fftshift(fft2(backprojected));
% % Filter in Freq Domain
reconstruction2DFT = reconstruction2DFT .* rampFilter2D;
 
% % inverse 2 D fourier transformation and sorting
reconstruction2DFT = real( ifft2( ifftshift( reconstruction2DFT )));

b4= mat2gray(reconstruction2DFT );
imshow(b4);
title('filter backproject image using ifft2(ifftshift()) with gray background');

