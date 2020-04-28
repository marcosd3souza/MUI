function paramCell = fs_unsup_idetect_build_param(it, distance, sigma, lambda)

%Para.sigma:  kernel width
%Para.lambda:  regularization parameter(critical)

if ~exist('it', 'var')
	it = 20;
end
if ~exist('distance', 'var') || isempty(distance)
	distance = {'euclidean','block'};
end

if ~exist('sigma', 'var') || isempty(sigma)
	sigma = 10.^[-5:0];
end

if ~exist('lambda', 'var') || isempty(lambda)
	lambda = 10.^[1:3];
end

n0 = it;
n1 = length(distance);
n2 = length(sigma);
n3 = length(lambda);

nP = n0 * n1 * n2 * n3;
paramCell = cell(nP, 1);
idx = 0;
for i0 = 1:n0
for i1 = 1:n1
    for i2 = 1:n2
        for i3 = 1:n3
            param = [];
            
            param.it = 20;
            param.distance = distance(i1){};
            param.sigma = sigma(i2);
            param.lambda = lambda(i3);
            idx = idx + 1;
            paramCell{idx} = param;
        end
    end
end
end
