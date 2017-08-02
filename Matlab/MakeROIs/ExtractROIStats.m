%-Extract mean values from ROIs
clear all; close all; clc;

ROIDir = '/mnt/apricot1_share6/MovementCorrection/PowerData/ROIs';
ROIs = dir(fullfile(ROIDir, '*_roi.mat'));
NumROIs = length(ROIs);
InputData = '/mnt/musk1/2006/06-11-12.1/fmri/resting_state_1/smoothed_spm8/swarI.nii';

ROIData = [];
for j = 1:NumROIs
  roi_obj = maroi(fullfile(ROIDir, ROIs(j).name));
  roi_data_obj = get_marsy(roi_obj, InputData, 'mean');
  roi_stats = summary_data(roi_data_obj);
  ROIData = [ROIData; roi_stats(9:end)'];
end

save('/mnt/apricot1_share6/MovementCorrection/SCSNLData/ROIMeanTS.mat', 'ROIData');
