function [residual_mtx] = NuisanceRegress2(signal_mtx, nuisance_mtx)

%%%%
% matrix are nxp, n: samples, p: features
%%%%

for ii = 1:size(signal_mtx, 2)
    b(:,ii) = regress(signal_mtx(:,ii), nuisance_mtx);
end
residual_mtx = signal_mtx - nuisance_mtx*b;