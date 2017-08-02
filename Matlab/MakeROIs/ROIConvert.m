%-convert marsbar ROIs to MNI nii
addpath(genpath('/home/fmri/fmrihome/SPM/spm8/toolbox/marsbar'));

addpath(pwd);
roi_dir = '/mnt/mabloo1/apricot1_share6/longitudinal/2012_integration_segregation/ROIs/ROI_160_10mm';

cd(roi_dir);
rois = dir('*-10mm_*_roi.mat');

num_roi = length(rois);

roi_list = cell(num_roi, 1);

for i = 1:num_roi
  roi_list{i} = fullfile(roi_dir, rois(i).name);
end

mars_rois2img(roi_list, '/mnt/mapricot/musk2/home/tianwenc/MakeROIs/ROI_160_10mm.nii')