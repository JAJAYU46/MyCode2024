




clc;
clear;
clear mycam;

load('Detector.mat'); % Load a pre-trained ACF detector.
%droneObj=ryze;
%takeoff(droneObj);

StreamingFlag = 1; %0: for web cam, 1: for video

%【Streaming】
if StreamingFlag==0
    mycam = webcam; % Initialize webcam
else
    %By Video
    vidReader = VideoReader('DroneVideo1.mp4');
    vidPlayer = vision.DeployableVideoPlayer; % Create video player for visualization
end

%【Start Object Detecting】
%第一次初始化
if StreamingFlag==0
    I = snapshot(mycam);
else
    I = readFrame(vidReader); %video reader
end

[bboxes, scores] = detect(detector, I, 'Threshold', 1);
previous_bboxes=bboxes;
previous_scores=scores; 
[imageHeight, imageWidth] = size(I);
centreX = imageWidth / 2;
centreY = imageHeight / 2;
dobra=0;
try 
    while dobra ==0
    %while hasFrame(vidReader)
    
        % GET DATA
        if StreamingFlag==0
            I = snapshot(mycam);% I: Capture a frame from webcam
        else
            I = readFrame(vidReader); %video reader
        end
        %fprintf('OK0\n');

        %Detect the Drone center
        %[bboxes, scores] = detect(detector, I, 'Threshold', 1);
        %fprintf('OK0.5\n');

        [I, previous_bboxes, previous_scores,NowDroneCenter] = getDroneCenterFunc(I, previous_bboxes, previous_scores, detector); %bboxes, scores);
        fprintf('OK8\n');


        %step(vidPlayer, I); % Display frame
        %dobra=calibration2(NowDroneCenter,  droneObj, centreX, centreY);
        
        imshow(I); % Display the frame
        drawnow; % Force MATLAB to update the display
    
    end
catch ME
    % If an error occurs, display it
    disp(['Error occurred: ', ME.message]);
end % End of try block

%close the open resources
   disp('Cleaning up...');
   clear mycam;
   %release(vidPlayer);
   disp('Cleanup complete.');

