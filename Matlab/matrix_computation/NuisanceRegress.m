function [residual_mtx] = NuisanceRegress(signal_mtx, nuisance_mtx)

%%%%
% matrix are nxp, n: samples, p: features
%%%%

residual_mtx = (eye(size(nuisance_mtx,1)) - nuisance_mtx*pinv(nuisance_mtx'*nuisance_mtx)*nuisance_mtx')*signal_mtx;
