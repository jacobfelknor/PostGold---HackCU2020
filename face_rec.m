clear all;
close all;

% Establishing the directory
dinfo = dir('/Users/drsain/Documents/Matlab/colFace');
dinfo([dinfo.isdir]) = []; 

% h is the height of each image in pixels
% w is the width of each image in pixels
% n is the number of images in the database
%[h,w] = size(imread('/Users/drsain/Documents/Matlab/colFace/00206_940128_fa_a.ppm'));
h = 256;
w = 384;
n1 = size(dinfo);
n = n1(1,1);

% This section inputs all of the data in the database. This is done by 
% transforming the original hxw matrix into a column vector of length h*w. 
% All of these column vectors are combined into the matrix yalefaces which 
% stores all of the data from all of the image in the database.
% Also in this section the mean image is created. The mean image is the
% average pixel value for all images.
yalefaces = [];
mean = zeros(h*w,1);
for i = 2:n
    % Designates the file's location
    filename = fullfile('/Users/drsain/Documents/Matlab/colFace/',dinfo(i).name);
    % Reads the data from the location
    face = imread(filename);
    face = rgb2gray(face);
    % Transforms the data from a matrix into a column vector.
    face = reshape(face,[h*w 1]);
    face = double(face);
    mean = mean + face;
    % This stores all of the column vectors in one matrix.
    yalefaces(:,i-1) = face(:);
end
% This calculates the average image.
mean = mean/(n-1);
imagesc(reshape(mean(:,1),w,h))
colormap gray

% a is a matrix where each column is the difference between the equivalent
% image and the average image.
a = zeros(h*w,n-1);
for i = 1: n-1
    a(:,i) = yalefaces(:,i) - mean(:,1);
end


% This section finds the eigenvectors of the covariant matrix.
% In other words this section computes the singular values and vectors of
% the SVD of a.
s = a'*a;
% obtain eigenvalue & eigenvector
[V,D] = eig(s);
%D = abs(D.^1/2);
D = diag(D);
D = D(end:-1:1);
V = fliplr(V);
%for i = 6:n-1
%    V(:,i) = zeros(n-1,1);
%end


% This projects the differences on to the singular vectors. This gives a
% basis for the space that contains all of the images.
eigenfaces = a * V;

% This finds the projects of the differences on the eigenface basis.
% Essentially this finds how much each image varies in the directions of
% each of the eigenfaces.
projectimg = [];
for i = 1:n-1
    temp = eigenfaces'*a(:,i);
    projectimg = [projectimg temp];
end
% This just shows that all of the information is recoverable from the basis
% of eigenfaces and the singular vectors.
%P = [];
%for i = 1:n-1
%    P(:,i) = a*V(:,i)/D(i,i);
%end
%figure,subplot(2,2,1)
%imagesc(reshape(yalefaces(:,1),w,h))
%subplot(2,2,2)
%imagesc(reshape(eigenfaces(:,1),w,h))
%subplot(2,2,3)
%b = eigenfaces*V';
%imagesc(reshape(b(:,1)+mean(:,1),w,h))
%subplot(2,2,4)
%b = P*projectimg*(D^-1);
%imagesc(reshape(b(:,1)+mean(:,1),w,h))
%colormap gray


for i = 1:10
    figure
    for j = 1:20
        subplot(4,5,j)
        imagesc(reshape(eigenfaces(:,((i-1)*10)+j),w,h))
    end
    colormap gray
end
        



% This initializes the test directory.
testdir = dir('/Users/drsain/Documents/Matlab/testFaces');
testdir([testdir.isdir]) = []; 

% These matrices store the test images and the closest matches.
people = [];
tests = [];
distances = zeros(10,2);
for t = 2:14
    % This inputs all of the test data.
    filename = fullfile('/Users/drsain/Documents/Matlab/testFaces/',testdir(t).name);
    test = imread(filename);
    test = rgb2gray(test);
    test = reshape(test, [h*w 1]);
    test = double(test);
    tests = [tests test];
    
    % This finds the difference from the average image.
    difference = test - mean;
    % This projects the difference on to the basis of eigenfaces.
    projtestimg = eigenfaces'*difference;
    
    % This finds the magnitude of the difference between the projection of
    % the test image compared to the projections of all images in the
    % database using the 2-norm.
    euclide_dist = zeros(1,n-1);
    for i = 1:n-1
        temp = (norm(projtestimg - projectimg(:,i)))^2;
        euclide_dist(1,i) = temp;
    end
    
    % This selects the index with the minimum 2-norm difference.
    [bestFit index] = min(euclide_dist);
    distances(t-1,1) = min(euclide_dist);
    distances(t-1,2) = max(euclide_dist);
    
    people(1,t-1) = index;
    
    % This matches the index of the image with the corresponding person and
    % stores the data.
    %person = ceil(index/10)
    %people(1,t) = index;
    %if person == t
    %    correct = correct + 1;
    %end
end
%correct

% This plots all of the test images as compared to their closest matches.
figure,subplot(5,6,1)
imagesc(reshape(tests(:,1), [w,h]));
subplot(5,6,2) 
imagesc(reshape(yalefaces(:,people(1,1)),w,h))
colormap gray
for i = 2:13
    subplot(5,6,2*i-1)
    imagesc(reshape(tests(:,i), [w,h]));
    subplot(5,6,2*i)
    imagesc(reshape(yalefaces(:,people(1,i)),w,h))
end
