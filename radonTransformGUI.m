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

% Last Modified by GUIDE v2.5 06-Oct-2017 00:57:23

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


% --- Executes on button press in buttonRadonTransform.
function buttonRadonTransform_Callback(hObject, eventdata, handles)
% hObject    handle to buttonRadonTransform (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
inputImage = handles.inputImage;
if size(inputImage) > 0
    theta = 0:1:179;
    [R,xp] = radon(inputImage,theta);
    axes(handles.axesRadonTransformImage);
    hold off;
    disp("Size of radon image:")
    disp(size(R))
    imshow(R,[],'Xdata',theta,'Ydata',xp,'InitialMagnification','fit');
    % colorbar;
    colorbar('Ticks',[0,0.5*10^4,1*10^4,1.5*10^4,2*10^4,2.5*10^4],...
         'TickLabels',{'0','5000','10000','15000','20000', '25000'});
    % imshow(R,[],'Xdata',theta,'Ydata',xp);
    xlabel('\theta (degrees)');
    ylabel('x''');
else
end

% --- Executes on button press in buttonInputImage.
function buttonInputImage_Callback(hObject, eventdata, handles)
% hObject    handle to buttonInputImage (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)'
inputImage = [];
inputImage = imread('testImage2.png');
% inputImage = rgb2gray(inputImage);
axes(handles.axesInputImage);
hold off;
disp("Size of input image:")
disp(size(inputImage))
imshow(inputImage)
colorbar('Ticks',[0,64,128,192,256],...
         'TickLabels',{'0','64','128','192','256'});
handles.inputImage = inputImage;
guidata(hObject,handles);


% --- Executes on button press in buttonRadonTransformMovie.
function buttonRadonTransformMovie_Callback(hObject, eventdata, handles)
% hObject    handle to buttonRadonTransformMovie (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
inputImage = handles.inputImage;
[inputRows, inputCols] = size(inputImage);
radonMovieFrame = zeros(180, inputRows);
% radonTransformMovie = VideoWriter('radonTransformMovie.mp4', 'MPEG-4');
% inputImageMovie = VideoWriter('inputImageMovie.mp4', 'MPEG-4');
% open(radonTransformMovie);
% open(inputImageMovie);
radonMovie = {};
inputImageMovie = {};
cmap = gray(256);
for angle = 0:1:179
    rotatedImage = imrotate(inputImage, angle);
    inputImageMovie = [inputImageMovie, im2frame(rotatedImage, cmap)];
    % writeVideo(inputImageMovie, rotatedImage);
    % sumLine = sum(rotatedImage);
%     sumLine = ones(180) .* 125;
%     % radonMovieFrame[angle + 1,:] = sumLine;
%     for x = 1:inputRows
%         radonMovieFrame(angle+1,x) = sumLine(x);
%     end
%     radonMovie = [radonMovie, im2frame(radonMovieFrame, cmap)];
    % writeVideo(radonTransformMovie, radonMovieFrame);
end
% close(inputImageMovie);
% close(radonTransformMovie);
% videoReaderInputImageMovie = VideoReader('inputImageMovie.mp4');
% videoReaderRadonTransformMovie = VideoReader('radonTransformMovie.mp4');

axes(handles.axesInputImage);
hold off;
imshow(inputImageMovie, 'Border', 'tight');

% axes(handles.axesRadonTransformImage);
% hold off;
% imshow(radonMovie.cdata, 'Border', 'tight');
% I should use getframe instead
        
    
    
    
    


