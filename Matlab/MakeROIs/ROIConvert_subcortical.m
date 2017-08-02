%-convert marsbar ROIs to MNI nii
addpath(genpath('/home/fmri/fmrihome/SPM/spm8/toolbox/marsbar'));
addpath(genpath('/home/wdcai/Library/Matlab/'));

addpath(pwd);
roiFolder = '/mnt/mandarin2/Public_Data/HCP/ROIs/Subcortical_from_Parcellation_HCP_rsfMRI_LR_77subjs_4mm/';
roiListFname = sprintf('%s/roiList_mat_fullpath_noHippo.txt', roiFolder);
roiList = ReadList(roiListFname);

%roi_dir = '/mnt/mandarin2/Public_Data/HCP/ROIs/Subcortical_from_Parcellation_HCP_rsfMRI_LR_77subjects/';

%cd(roi_dir);
%rois = dir('*-10mm_*_roi.mat');

%num_roi = length(rois);

% roi_list = cell(num_roi, 1);
% 
% for i = 1:num_roi
%   roi_list{i} = fullfile(roi_dir, rois(i).name);
% end

%roiIntensityFname = sprintf('%sROIs_Regions_noHippo.txt', roiFolder);

outputFname = sprintf('%sSubcortical_noHippo_4mm_numLabel.nii', roiFolder);

%mars_rois2img_wLabels(roiList, outputFname, roiIntensityFname)
mars_rois2img(roiList, outputFname)