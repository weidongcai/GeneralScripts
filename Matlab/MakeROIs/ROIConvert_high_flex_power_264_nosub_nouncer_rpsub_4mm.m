%-convert marsbar ROIs to MNI nii
addpath(genpath('/home/fmri/fmrihome/SPM/spm8/toolbox/marsbar'));
addpath(genpath('/home/wdcai/Library/Matlab/'));

addpath(pwd);
hcpRoiFolder = '/mnt/mandarin1/Public_Data/OpenfMRI/ROIs/Power_264_6mm/';
hcpRoiListFname = sprintf('%s/roisList_6mm_fullpath.txt', hcpRoiFolder);
hcpRoiList = ReadList(hcpRoiListFname);

subcortical_module = 10;
uncertain_module = -1;
hcpModuleFolder = '/mnt/mandarin1/Public_Data/OpenfMRI/ROIs/Power_ROIs_264/ROI_modules/';
hcpRoiModuleFname = sprintf('%sPower_264_ROI_modules.txt', hcpModuleFolder);
fid = fopen(hcpRoiModuleFname);
foutput = textscan(fid, '%d%d');
fclose(fid)
hcpRoiModule = foutput{2};
nosub_nouncer_idx = find((hcpRoiModule ~= subcortical_module) & (hcpRoiModule~= uncertain_module));
nosub_nouncer_roiList = hcpRoiList(nosub_nouncer_idx);


subRoiFolder = '/mnt/mandarin2/Public_Data/HCP/ROIs/Subcortical_from_Parcellation_HCP_rsfMRI_LR_77subjs_4mm/';
subNonHippoRoiListFname = sprintf('%sroiList_mat_fullpath_noHippo.txt', subRoiFolder);
sub_nonhippo_roiList = ReadList(subNonHippoRoiListFname);

nosub_nouncer_rpsub_roiList = horzcat(nosub_nouncer_roiList, sub_nonhippo_roiList);

highFlexIdxFolder = '/mnt/apricot1_share6/TRSBN_test_HCP/TRSBN_stats/Dynamic/sign_und/network_switching/';
highFlexIdxFname = sprintf('%sROI_idx_high_flex_power_264_nosub_nouncer_rpsub_4mm.txt', highFlexIdxFolder);
highFlexIdx = load(highFlexIdxFname);

nosub_nouncer_rpsub_highflex_roiList = nosub_nouncer_rpsub_roiList(highFlexIdx);

outputFolder = '/mnt/mandarin2/Public_Data/HCP/ROIs/Subcortical_from_Parcellation_HCP_rsfMRI_LR_77subjs_4mm/';
outputFname = sprintf('%spower_264_nosub_nouncer_rpsub_highflex_4mm.nii', outputFolder);

mars_rois2img(nosub_nouncer_rpsub_highflex_roiList, outputFname)