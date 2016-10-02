clear all

subject_list = '/mnt/mandarin2/Public_Data/HCP/data_test_validate/hcp_final_selection/hcp_77subjects.txt';
data_dir = '/mnt/apricot1_share6/TRSBN_test_HCP/TS_for_TRSBN/Power_264_6mm/';
flname_prefix = 'regwc24mv_bp86_srfMRI_REST1_LR_mean_ts_rfMRI_REST1_LR';

subjects = ReadList(subject_list);
num_subj = length(subjects);

TR = 0.645;
fs = 1/TR;
fnyquist = fs/2;

for jsubj = 1:num_subj
    fprintf('---> subject: %s\n', subjects{jsubj});
    subj_fname = sprintf('%s%s_%s.mat', data_dir, flname_prefix, subjects{jsubj});
    subj_roi_ts = load(subj_fname);
    t_data = subj_roi_ts.roi_ts;
    N = size(t_data,1);
    for i = 1:size(t_data,2)
        [power_data(i,:, jsubj), freq_data(i,:, jsubj)] = pwelch(t_data(:,i),[],[],[],fs);
    end
end

power_data_mean = mean(power_data,3);
power_data_std = std(power_data,0,3);
freq_axis = freq_data(1,:,1);
freq_axis = freq_axis(:);

for k = 1:size(power_data_mean,1)
    plot(freq_axis, power_data_mean(k,:));
    hold on;
end
% 
% figure()
% imagesc(freq_data(1,:), 1:264, power_data)

% bin_vals = [0:N-1];
% f_ax_hz = (bin_vals*fs/N);
% N_2 = ceil(N/2);
% 
% %f_data_db = f_data;
% f_data_db = 10*log10(f_data);
% f_data_db_singleside = f_data_db(1:N_2,:)';
% 
% figure();
% imagesc(f_ax_hz(1:N_2), 1:264, f_data_db_singleside);

%plot(f_ax_hz(1:N_2), f_data(1:N_2));