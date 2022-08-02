%% PLOTS FIGURE 3: COLONY COUNTING

dataDir='./../data/Figure_colonies/DATA/';
T1 = readtable([dataDir,'IMG_0024.csv']);
T2 = readtable([dataDir,'IMG_0036.csv']);
T3 = readtable([dataDir,'IMG_0048.csv']);
T4 = readtable([dataDir,'IMG_0212.csv']);
T5 = readtable([dataDir,'IMG_0220.csv']);
T6 = readtable([dataDir,'IMG_0228.csv']);

f1=100*length(find(T1.Type>1))/length(T1.Type);
f2=100*length(find(T2.Type>1))/length(T2.Type);
f3=100*length(find(T3.Type>1))/length(T3.Type);
f4=100*length(find(T4.Type>1))/length(T4.Type);
f5=100*length(find(T5.Type>1))/length(T5.Type);
f6=100*length(find(T6.Type>1))/length(T6.Type);

w1=log(length(find(T1.Type>1)))/log(length(find(T1.Type<2)));
w2=log(length(find(T2.Type>1)))/log(length(find(T2.Type<2)));
w3=log(length(find(T3.Type>1)))/log(length(find(T3.Type<2)));
w4=log(length(find(T4.Type>1)))/log(length(find(T4.Type<2)));
w5=log(length(find(T5.Type>1)))/log(length(find(T5.Type<2)));
w6=log(length(find(T6.Type>1)))/log(length(find(T6.Type<2)));

figure(1); clf('reset');  set(gcf,'DefaultLineLineWidth',2); set(gcf, 'color', 'white'); 
set(gcf, 'Position',  [100, 100, 200, 400]);
plot([0,2],[1,1],':','Color',[.75 .75 .75]); hold on;

boxplot([w1; w2; w3; w4; w5; w6], 'sym','r*', 'colors',[0 0 0]); hold on;
set(gca,'FontSize',18)
xticks([1]);
xticklabels('Gby/Wcl')
ylabel('Relative fitness');
axis([.75 1.25 0.6 1.4]);

%% PLOTS FIGURE 5: COLONY EXPANSION
figure(); clf('reset');  set(gcf,'DefaultLineLineWidth',2); set(gcf, 'color', 'white'); 

T_DARK = readtable('../data/Figure_expansion/DATA/Results_DARK.csv');
T_GFP = readtable('../data/Figure_expansion/DATA/Results_GFP.csv');
T_RFP = readtable('../data/Figure_expansion/DATA/Results_RFP.csv');
   
dist=1:length(T_RFP.Mean);
normInt_RFP=T_RFP.Mean./max(T_RFP.Mean);
normInt_GFP=T_GFP.Mean./max(T_GFP.Mean);
normInt_DARK=T_DARK.Mean./max(T_DARK.Mean);

plot(dist, normInt_RFP,'-m','MarkerFaceColor','m','LineWidth',3); hold on;
plot(dist, normInt_GFP,'-g','MarkerFaceColor','g','LineWidth',3); hold on;
plot(dist, normInt_DARK,'-k','MarkerFaceColor','k','LineWidth',3); hold on;

set(gca,'FontSize',16);
ylim([0.5, 1.1])
xlabel('Distance from center (pixels)','FontSize',20);
ylabel('Normalized intensity','FontSize',20);

%% PLOTS FIGURE 6: TIMELAPSE OF COLONY EXPANSION

figure(); clf('reset');  set(gcf,'DefaultLineLineWidth',2); set(gcf, 'color', 'white'); 

DATA_radius = readtable('../data/Figure_timelapse/DATA/Dendritiformis_radius.csv');

plot(DATA_radius.t, DATA_radius.r,'-k','LineWidth',3); hold on;
set(gca,'FontSize',16);
xlabel('Time (frames)','FontSize',20);
ylabel('Colony radius','FontSize',20);



