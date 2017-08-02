function plot_matrix(mtx, newColorMap, clim, flg_grid, flg_margin_off)

colormap(newColorMap);

imagesc(mtx, clim);

set(gca, 'XTick', [], 'YTick', [], 'XTickLabel', '', 'YTickLabel', '');

if flg_margin_off
    set(gca, 'position', [0 0 1 1]);
end
if flg_grid
    hold on;
    for i = 1:size(mtx,1)
        plot([-0.5, size(mtx,1)+0.5], [i-0.5, i-0.5], 'k-', 'LineWidth', 2);
        plot([i-0.5, i-0.5], [-0.5, size(mtx,1)+0.5], 'k-', 'LineWidth', 2);
    end
end