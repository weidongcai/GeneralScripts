%-convert marsbar ROIs to MNI nii
addpath(genpath('/home/fmri/fmrihome/SPM/spm8/toolbox/marsbar'));
addpath(genpath('/home/wdcai/Library/Matlab/'));

addpath(pwd);
roiFolder = '/mnt/mandarin1/Public_Data/OpenfMRI/ROIs/Power_264_6mm/';
roiListFname = sprintf('%s/roisList_6mm_fullpath.txt', roiFolder);
roiList = ReadList(roiListFname);

subcortical_module = 10;
moduleFolder = '/mnt/mandarin1/Public_Data/OpenfMRI/ROIs/Power_ROIs_264/ROI_modules/';
roiModuleFname = sprintf('%sPower_264_ROI_modules.txt', moduleFolder);
fid = fopen(roiModuleFname);
foutput = textscan(fid, '%d%d');
fclose(fid)
roiModule = foutput{2};
subcortical_idx = find(roiModule == subcortical_module);
subcortical_roiList = roiList(subcortical_idx);

outputFolder = '/mnt/mandarin2/Public_Data/HCP/ROIs/Subcortical_from_Parcellation_HCP_rsfMRI_LR_77subjs/';
outputFname = sprintf('%sSubcortical_HCP_6mm.nii', outputFolder);

mars_rois2img(subcortical_roiList, outputFname)