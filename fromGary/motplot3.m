%	to open motion file and do some plotting of
%	stats for brain activation
%	
%	rev 0 	5/12/95		original
%	rev 1 	12/10/06	can do 6 axes
%	rev 3 			can correlate with a block trial

rad = 68.0;			% geometric mean of spm brain mask
				% for calc motion from rots
%  open the file

fname = input('gimme file = ', 's');
fid = fopen(fname, 'r');
num = input('num components (3 or 6) [6] = ');
if(isempty(num))
  num = 6;
end
if(num == 3)
  [dat n] = fscanf(fid, '%g %g %g\n');
  m=n/3;
else
  [dat n] = fscanf(fid, '%g %g %g %g %g %g\n');
  m=n/6;
end
fclose(fid);
u = zeros(num, m);
t = (1:m)';
for k=1:num
  x = dat(k:num:n);
  p = polyfit(t, x, 1);
  xfit = polyval(p, t);
  rms(k) = std(x - xfit);
  u(k,1:m) = x';
  v(k,1:m) = (x - xfit)';
end

spm = input('spm(1) or not(0) [0] = ');
if(isempty(spm)) spm = 0; end;
if(spm)
  u(4:6,:) = u(4:6,:)*180/pi;	% spm rot are in radians
  rms(4:6) = rms(4:6)*180/pi;
end

% get scale factors

foo = input('gimme [npix fov slcthick (mm)] (64 220 4) = ');
if(isempty(foo))
  foo = [64 220 4];
end
npix = foo(1); fov = foo(2); slthick = foo(3);
pix = fov/npix;
rms(1:2) = rms(1:2)*pix;
rms(3) = rms(3)*slthick;
rms(4:6) = rms(4:6)*pi/180*rad;

%  plot x, y, z

if(num == 6)  subplot(2,1,1); end
plot(t,u(1:3,:));
ymin = floor(min(min(u(1:3,:))));
ymax = ceil(max(max(u(1:3,:))));
axis([1 m ymin ymax]);
xlabel('frame');
ylabel('translation, mm');
grid
title(sprintf('%s   x=blu, y=grn, z=red   rms=%6.3f %6.3f %6.3f mm', fname, rms(1:3)));

%  plot thet, phi, eta

if (num==6)
  subplot(2,1,2); 
  plot(t,u(4:6,:));
  ymin = floor(min(min(u(4:6,:))));
  ymax = ceil(max(max(u(4:6,:))));
  axis([1 m ymin ymax]);
  xlabel('frame');
  ylabel('phi, deg.');
  grid
  title(sprintf('Rx=blu, Ry=grn, Rz=red   rms=%6.3f %6.3f %6.3f mm', rms(4:6)));
end

%  calc motion correlation

T = input('task period: frames [15] = ');
if(isempty(T))
  T = 15;
end
Ton = round(T/2);
d = zeros(m,1);
for k=1:T:m
  d(k:k+Ton-1) = ones(Ton,1);
end

for j=1:num
  cc = corrcoef(d, v(j,:));		% R^2 is the fraction of task-cor variance 
  rmstask(j) = rms(j)*abs(cc(1,2));  	% the rms that is task correlated
end

% drift and maxima

drift = max(u') - min(u');

fprintf('drift   = %6.3f %6.3f %6.3f %6.3f %6.3f %6.3f mm\n', drift);
fprintf('rms     = %6.3f %6.3f %6.3f %6.3f %6.3f %6.3f mm\n', rms);
fprintf('rmstask = %6.3f %6.3f %6.3f %6.3f %6.3f %6.3f mm\n', rmstask);

driftmax = max(drift);
rmsmax = max(rms);
rmstaskmax = max(rmstask);
fprintf('max drift, rms, rmstask = %6.3f %6.3f %6.3f mm\n', driftmax, rmsmax, rmstaskmax);




