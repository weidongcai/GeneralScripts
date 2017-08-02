clear all; close all; clc

roi_folder = pwd;

% Define ROIs by specifying name, coordinates and radius
myroi{1}.name = 'right_mSTS';
myroi{1}.coords = [54 -16 -4];
myroi{1}.radius = 5;

myroi{2}.name = 'right_Parahipp';
myroi{2}.coords = [18 -34 -10];
myroi{2}.radius = 2;

myroi{3}.name = 'right_Amyg';
myroi{3}.coords = [24 -10 -14];
myroi{3}.radius = 2;



no_rois = length(myroi);

addpath /home/fmri/fmrihome/SPM/spm8/toolbox/marsbar
spm('Defaults','fmri')
marsbar('on');
for roi_i = 1:no_rois
    
%     coords = [mni_x mni_y mni_z];
    this_region = myroi{roi_i}.name;
    

    coords = myroi{roi_i}.coords;
    radius = myroi{roi_i}.radius;
    % -------------------------------------------------------------------------
    % Here is the 'roi_make_sphere.m' script
    % -------------------------------------------------------------------------
    
    
    %     function roi_make_sphere(Config_File)
    
    warning('off', 'MATLAB:FINITE:obsoleteFunction')
    %     disp(['Current directory is: ',pwd]);
    
    % -------------------------------------------------------------------------
    % Check existence of the configuration file
    % -------------------------------------------------------------------------
    
    %     if(exist(Config_File,'file')==0)
    %         fprintf('Cannot find the configuration file ... \n');
    %         return;
    %     end
    
    %     Config_File = strtrim(Config_File);
    %     Config_File = Config_File(1:end-2);
    %     eval(Config_File);
    %     clear Config_File;
    
    %   Here is a temp roi_folder
%     roi_folder = fullfile(output_dir, 'temp_dir');
    
    if exist(roi_folder,'dir')
        cd(roi_folder);
    else
        mkdir(roi_folder);
        cd(roi_folder);
    end
    
    %     disp('Making ROIS ...');
    
    %     for i=1:length(myroi)
    %     coords = myroi{i}.coords;
    %     radius = myroi{i}.radius;
    %     name = myroi{i}.name;
    name = ['ROI_' int2str(roi_i) '_' this_region];
    
    roi = maroi_sphere(struct('centre', coords, 'radius', radius));
    roi = label(roi, name);
    
    n = num2str(i);
    r = num2str(radius);
    x = num2str(coords(1));
    y = num2str(coords(2));
    z = num2str(coords(3));
    
    if length(n) == 1
        n = ['0' n];
    end
    
    %     filename = [n '-' r 'mm_' name '_' x '_' y '_' z '_roi.mat'];
    filename = [name '-' r 'mm_' x '_' y '_' z '_roi.mat'];
    fpath    = fullfile(roi_folder,filename);
    save(fpath, 'roi');
    %     end
    
    %     disp('Making ROIs is done.');
    
    %     end
    
    new_img_name = [name '.nii'];
    
    %     mars_rois2img(fpath, new_img_name, roi_space)
    mars_rois2img(fpath, new_img_name);
    
    % This deletes the roi.mat and the labels.mat files
    delete(fpath)
    labels_fname = [name '_labels.mat'];
    delete(labels_fname);
    
    
    clear roi hdr fpath
    
end




