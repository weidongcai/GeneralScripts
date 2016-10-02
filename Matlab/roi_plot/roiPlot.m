roi_file = '/mnt/mabloo1/apricot1_share6/network_interaction/network_nonstationary/group_78subjects/ROI_264/roi/roi_264_6mm.nii';
roi_v = spm_vol(roi_file);
roi_d = spm_read_vols(spm_vol(roi_v));

for icomm = 1:num_comm
    comm_v = roi_v;
    comm_v.fname = fullfile(result_dir, ['stable_bootstrap_stability_ROI_264_static_community_', num2str(icomm), '.nii']);
    comm_v.private.dat.fname = fullfile(result_dir, ['stable_bootstrap_stability_ROI_264_static_community_', num2str(icomm), '.nii']);
    comm_d = zeros(size(roi_d));
    comm_node_idx = stable_node_idx(stability_clust_mtx == icomm);
    for i_node = 1:length(comm_node_idx)
        comm_d(roi_d == comm_node_idx(i_node)) = icomm;
    end
    spm_write_vol(comm_v, comm_d);
end
