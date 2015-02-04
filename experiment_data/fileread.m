fid = fopen('points.dat');
c=textscan(fid, '%f %f %f %s');
gscatter(c{1}, c{2}, c{4}); % plot only x and y
