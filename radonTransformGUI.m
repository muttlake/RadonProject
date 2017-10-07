function varargout = radonTransformGUI(varargin)
% RADONTRANSFORMGUI MATLAB code for radonTransformGUI.fig
%      RADONTRANSFORMGUI, by itself, creates a new RADONTRANSFORMGUI or raises the existing
%      singleton*.
%
%      H = RADONTRANSFORMGUI returns the handle to a new RADONTRANSFORMGUI or the handle to
%      the existing singleton*.
%
%      RADONTRANSFORMGUI('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in RADONTRANSFORMGUI.M with the given input arguments.
%
%      RADONTRANSFORMGUI('Property','Value',...) creates a new RADONTRANSFORMGUI or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before radonTransformGUI_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to radonTransformGUI_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help radonTransformGUI

% Last Modified by GUIDE v2.5 06-Oct-2017 19:55:45

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @radonTransformGUI_OpeningFcn, ...
                   'gui_OutputFcn',  @radonTransformGUI_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


function fieldEnterAngleIncrement_Callback(hObject, eventdata, handles)
% hObject    handle to fieldEnterAngleIncrement (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of fieldEnterAngleIncrement as text
%        str2double(get(hObject,'String')) returns contents of fieldEnterAngleIncrement as a double


% --- Executes during object creation, after setting all properties.
function fieldEnterAngleIncrement_CreateFcn(hObject, eventdata, handles)
% hObject    handle to fieldEnterAngleIncrement (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in buttonAngleIncrement.
function buttonAngleIncrement_Callback(hObject, eventdata, handles)
% hObject    handle to buttonAngleIncrement (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
angleIncrement = 1;
angleIncrement = str2num(get(handles.fieldEnterAngleIncrement,'String'));
if angleIncrement < 1 || angleIncrement > 179
    angleIncrement = 1;
    disp("Changing to default angleIncrement = 1");
end
handles.angleIncrement = angleIncrement;
guidata(hObject,handles);
% --- buttonAngleIncrement


% --- Executes just before radonTransformGUI is made visible.
function radonTransformGUI_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to radonTransformGUI (see VARARGIN)

% Choose default command line output for radonTransformGUI
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes radonTransformGUI wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = radonTransformGUI_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;

% --- Executes on button press in buttonInputImage.
function buttonInputImage_Callback(hObject, eventdata, handles)
% hObject    handle to buttonInputImage (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)'
inputImage = [];
inputImage = imread('Lenna.png');
inputImage = rgb2gray(inputImage);
disp("Size of input image:")
disp(size(inputImage));
axes(handles.axesInputImage);
hold off;
imshow(inputImage)
colorbar('Ticks',[0,64,128,192,256],...
         'TickLabels',{'0','64','128','192','256'});
handles.inputImage = inputImage;
guidata(hObject,handles);

% --- End buttonInputImage


% --- Executes on button press in buttonMatlabRadonTransform.
function buttonMatlabRadonTransform_Callback(hObject, eventdata, handles)
% hObject    handle to buttonMatlabRadonTransform (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
inputImage = handles.inputImage;
angleIncrement = handles.angleIncrement;
if size(inputImage) > 0
    theta = 0:angleIncrement:179;
    [R,xp] = radon(inputImage,theta);
    axes(handles.axesMatlabRadonTransform);
    hold off;
    % disp("Size of radon image:")
    % disp(size(R))
    imshow(R,[],'Xdata',theta,'Ydata',xp,'InitialMagnification','fit');
    % colorbar;
    colorbar;
    % imshow(R,[],'Xdata',theta,'Ydata',xp);
    xlabel('\theta (degrees)');
    ylabel('x''');
    handles.matlabRadonTransformR = R;
    handles.theta = theta;
    guidata(hObject,handles);
else
end
% --- End buttonMatlabRadonTransform

% --- Executes on button press in buttonMatlabIRadonTransform.
function buttonMatlabIRadonTransform_Callback(hObject, eventdata, handles)
% hObject    handle to buttonMatlabIRadonTransform (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
matlabRadonTransformR = handles.matlabRadonTransformR;
theta = handles.theta;
matlabInverseRadonImage = iradon(matlabRadonTransformR,theta);
axes(handles.axesMatlabIRadonTransform);
hold off;
imshow(matlabInverseRadonImage, []);



% --- End buttonMatlabIRadonTransform

% --- Executes on button press in buttonNguyenBackprojection.
function buttonNguyenBackprojection_Callback(hObject, eventdata, handles)
% hObject    handle to buttonNguyenBackprojection (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
%% Minh Anh Nguyen
% set some parameters
inputImage = handles.inputImage;
angleIncrement = handles.angleIncrement;
thetas = 0:angleIncrement:179;
% compute sinogram with matlab function
sinogram = radon(inputImage,thetas);
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
%% rotating and clipping image Timothy Shepard
disp("Size of b4 matrix: ");
disp(size(b4));
b4 = imrotate(b4, 90);
%%
axes(handles.axesNguyenRadonBackprojection);
hold off;
imshow(b4);
title('filter backproject image using ifft2(ifftshift()) with gray background');
