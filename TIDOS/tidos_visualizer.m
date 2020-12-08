%%
clc; clear all; close all;


%%% Variable 'location' stores the location of the data in your computer 
%%% that you are trying to visualize
%%% E.g: 
%location = 'C:\Users\xxx\Desktop\TIDOS\Data\Lecture\lecture_sensor_1'

location = '';

%%% Variable 'sec' stores the which second(.JSON file) of the recording you want to visualize
%%% E.g: sec = 10;

sec = 1;


%%% Variable 'frame' identifies the specific frame you want to visualize
%%% in the second(JSON file) that you chose. Note that, there are 16 frames
%%% in a second, you can choose any of them by using variable 'frame'
%%% E.g: frame = 12;

frame = 12;

%%
%%% This piece of code prepapre the string that will be used the read the
%%% data

if sec<10
        str = [location,'\data00000',num2str(sec),'.json'];
elseif sec>9 && sec<100
        str = [location,'\data0000',num2str(sec),'.json'];
elseif sec>99 && sec<1000
        str = [location,'\data000',num2str(sec),'.json'];
else
        str = [location,'\data00',num2str(sec),'.json'];
end

%%% This piece of code reads the data from a .JSON file and put the thermal
%%% data in a matrix

json = fileread(str);

struct = jsondecode(json);

values=struct.Frames_B;

data=zeros(24,32,16);

for k=1:16

    for j=1:24

        data(j,:,k)=values(k,32*(j-1)+1:32*j);

    end
    
end

%%%This piece of code visualize the necessary frame
figure_title=['Second= ',num2str(sec),'  Frame= ',num2str(frame)];
figure('Name',figure_title,'NumberTitle','off')
ax1=subplot(1,1,1);
imagesc(data(:,:,frame))
colormap(ax1, jet)
ax1.FontSize=16;
daspect([1 1 1])
c1=colorbar
c1.Ticks=([15 20 28 35 40]);
c1.TickLabels={'15°C','20°C','28°C','35°C','40°C'};
caxis([15 40])
set(gca,'FontSize',18)



