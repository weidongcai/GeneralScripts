function parsave(varargin)

filename = varargin{1};

for i =2:nargin
    savevar.(inputname(i)) = varargin{i};
end

save(filename, '-struct', 'savevar');

end