%-make sphere ROIs

clear all; close all; clc;

addpath(genpath('/home/fmri/fmrihome/SPM/spm8/toolbox/marsbar'));
roi_folder = pwd;

ROICoord = load('ROI_Coords.txt');

for i = 1:size(ROICoord, 1)
  
  coords = ROICoord(i, :);
  radius = 6;
  name = ['ROI_', num2str(i)];

  roi = maroi_sphere(struct('centre', coords, 'radius', radius));
  roi = label(roi, name);

  n = num2str(i);
  r = num2str(radius);
  x = num2str(coords(1));
  y = num2str(coords(2));
  z = num2str(coords(3));
  
  if length(n) == 1
    n = ['00' n];
  else
    if length(n) == 2
      n = ['0', n];
    end
  end
  
  filename = [n '-' r 'mm_' name '_' x '_' y '_' z '_roi.mat'];
  fpath    = fullfile(roi_folder, filename); 
  save(fpath, 'roi');
end

disp('Making ROIs is done.');