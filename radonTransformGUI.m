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
inputImage = imread('testImage2.png');
% inputImage = rgb2gray(inputImage);
axes(handles.axesInputImage);
hold off;
% disp("Size of input image:")
% disp(size(inputImage))
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


% --- Executes on button press in buttonNguyenRadonTransform.
function buttonNguyenRadonTransform_Callback(hObject, eventdata, handles)
% hObject    handle to buttonNguyenRadonTransform (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
inputImage = handles.inputImage;
angleIncrement = handles.angleIncrement;
if size(inputImage) > 0
    theta = 0:angleIncrement:179;
    [R,xp] = radon(inputImage,theta);
    axes(handles.axesNguyenRadonTransform);
    hold off;
    % disp("Size of radon image:")
    % disp(size(R))
    imshow(R,[],'Xdata',theta,'Ydata',xp,'InitialMagnification','fit');
    colorbar;
    xlabel('\theta (degrees)');
    ylabel('x''');
else
end
% --- End buttonNguyenRadonTransform


% --- Executes on button press in buttonNguyenBackprojection.
function buttonNguyenBackprojection_Callback(hObject, eventdata, handles)
% hObject    handle to buttonNguyenBackprojection (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
