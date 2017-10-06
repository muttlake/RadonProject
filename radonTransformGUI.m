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

% Last Modified by GUIDE v2.5 05-Oct-2017 21:29:21

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
    theta = 0:180;
    [R,xp] = radon(inputImage,theta);
    axes(handles.axesRadonTransformImage);
    imshow(R);
    title('Radon Transform {\theta} (X\prime)');
    xlabel('\theta (degrees)');
    ylabel('X\prime');
    set(gca,'XTick',0:20:180);
    colormap(gray);
    colorbar;
else
end

% --- Executes on button press in buttonInputImage.
function buttonInputImage_Callback(hObject, eventdata, handles)
% hObject    handle to buttonInputImage (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)'
inputImage = [];
inputImage = imread('Lenna.png');
inputImage = rgb2gray(inputImage);
inputImage = imresize(inputImage, [256, 256]);
axes(handles.axesInputImage);
imshow(inputImage)
handles.inputImage = inputImage;
guidata(hObject,handles);