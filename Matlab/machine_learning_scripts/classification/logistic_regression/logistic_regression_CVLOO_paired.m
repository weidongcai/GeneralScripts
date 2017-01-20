function [acc] = logistic_regression_CVLOO_paired(X_grp1, X_grp2, y_grp1, y_grp2)

addpath(genpath('/home/tianwenc/CommonlyUsedScripts'));

if size(X_grp1,1) == size(X_grp2, 1)
    n_grp = size(X_grp1, 1);
else
    fprintf('Error: two pairs of data have different sampel size!'\n);
    return;
end

data_mtx = [X_grp1; X_grp2];
normal_data_mtx = NormalizeData(data_mtx);

X_grp1_norm = normal_data_mtx(1:n_grp, :);
X_grp2_norm = normal_data_mtx(n_grp+1:end,:);

y_pred_all = [];
y_test_all = [];

fullidx = 1:n_grp;

for i = 1:n_grp
    idx_test = i;
    idx_train = find(fullidx ~= i);
    X_test = [X_grp1_norm(idx_test,:); X_grp2_norm(idx_test,:)];
    y_test = [y_grp1(idx_test,:); y_grp2(idx_test,:)];
    X_train = [X_grp1_norm(idx_train,:); X_grp2_norm(idx_train,:)];
    y_train = [y_grp1(idx_train,:); y_grp2(idx_train,:)];
   
    % apply logistic regression
    [B, dev, stats] = mnrfit(X_train, y_train);
    [pihat, dlow, dhi] = mnrval(B, X_test, stats);
        
    for j = 1:size(pihat,1)
        jpihat = pihat(j,:);
        if jpihat(1) > jpihat(2)
            y_pred = 1;
        else
            y_pred = 2;
        end
        
        y_pred_all = [y_pred_all; y_pred];
        y_test_all = [y_test_all; y_test(j)];
    end
end

acc = sum(y_pred_all == y_test_all)/length(y_pred_all);
fprintf('accurasy: %4.3f\n', acc);