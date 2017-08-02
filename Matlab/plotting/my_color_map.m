function [newColorMap] = my_color_map(posColor, negColor)

% posScale = [zeros(1, 124), linspace(0.2, 0.8, 132)];
% negScale = [linspace(0.8, 0.2, 132), zeros(1, 124)];
% transScale = [zeros(1, 85), linspace(0.2, 0.8, 43), linspace(0.8,0.2,43), zeros(1,85)];
% zeroScale = [zeros(1, 256)];
% neutralScale = [0.5*ones(1,256)];

posScale = [zeros(1, 126), ones(1,4), linspace(0.2, 0.8, 126)];
negScale = [linspace(0.8, 0.2, 126), ones(1,4), zeros(1, 126)];
transScale = [zeros(1,63), linspace(0.4,0.8,63), ones(1,4), linspace(0.4,0,63), zeros(1,63)];

if strcmp(posColor, 'red') && strcmp(negColor, 'blue')
    newColorMap = [posScale; transScale; negScale]';
elseif strcmp(posColor, 'red') && strcmp(negColor, 'green')
    newColorMap = [posScale; negScale; transScale]';
elseif strcmp(posColor, 'green') && strcmp(negColor, 'bllue')
    newColorMap = [transScale; posScale; negScale]';
end

end