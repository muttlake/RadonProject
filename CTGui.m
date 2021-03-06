function varargout = CTGui(varargin)
% CTGUI MATLAB code for CTGui.fig
%      CTGUI, by itself, creates a new CTGUI or raises the existing
%      singleton*.
%
%      H = CTGUI returns the handle to a new CTGUI or the handle to
%      the existing singleton*.
%
%      CTGUI('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in CTGUI.M with the given input arguments.
%
%      CTGUI('Property','Value',...) creates a new CTGUI or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before CTGui_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to CTGui_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help CTGui

% Last Modified by GUIDE v2.5 06-Nov-2017 03:06:41

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @CTGui_OpeningFcn, ...
                   'gui_OutputFcn',  @CTGui_OutputFcn, ...
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


% --- Executes just before CTGui is made visible.
function CTGui_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to CTGui (see VARARGIN)

% Choose default command line output for CTGui
handles.output = hObject;
handles.aI = 1;

im = phantom('Modified Shepp-Logan',256);
axes(handles.axes1);
imshow(im);
handles.im = im;
guidata(hObject,handles);

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes CTGui wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = CTGui_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on button press in pushbutton1.
function pushbutton1_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% here we load image
global im im2
[path, user_cance] = imgetfile();
if user_cance
    magbox(sprintf('Error'), 'Error', 'Error')
    return 
end
im = imread(path);
im = im2double(im);
szdim3 = size(im, 3);
if szdim3 > 1
    im = rgb2gray(im);
end
im2 = im; % for backup process
axes(handles.axes1);
imshow(im);
handles.im = im;
handles.im2 = im2;
guidata(hObject,handles);




% --- Executes on slider movement.
function slider1_Callback(hObject, eventdata, handles)
% hObject    handle to slider1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'Value') returns position of slider
%        get(hObject,'Min') and get(hObject,'Max') to determine range of slider
global angleIncrement;
a = get(handles.slider1, 'Value'); % a is from 0 to 1
x = 178;
angleIncrement = round(floor(x*a)) + 1;
textOut = strcat("= ", num2str(angleIncrement), '�');
set(handles.angleIncrementText, 'String', textOut);
handles.aI = angleIncrement;
guidata(hObject,handles);



% --- Executes during object creation, after setting all properties.
function slider1_CreateFcn(hObject, eventdata, handles)
% hObject    handle to slider1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background.
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end



% --- Executes on button press in pushbutton3.
function pushbutton3_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
im = phantom('Modified Shepp-Logan',256);
axes(handles.axes1);
imshow(im);
handles.im = im;
guidata(hObject,handles);


% --- Executes on button press in radonButton.
function radonButton_Callback(hObject, eventdata, handles)
% hObject    handle to radonButton (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
angleIncrement = handles.aI;
im = handles.im;
textOut = strcat(num2str(angleIncrement), "� Angle Increment");
set(handles.radonAngleIncrementText, 'String', textOut);
theta = 0:angleIncrement:179;
[R,xp] = radon(im,theta);
axes(handles.axes2);
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

    
