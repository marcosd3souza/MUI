function paramCell = fs_unsup_jelsr_build_param(knnCandi, weightCandi, weight_param_Candi, alphaCandi, betaCandi)
n1 = length(knnCandi);
n2 = length(weightCandi);
n3 = length(weight_param_Candi);
n4 = length(alphaCandi);
n5 = length(betaCandi);

nP = n1 * n2 * n3 * n4 * n5;
paramCell = cell(nP, 1);
idx = 0;
for i1 = 1:n1
    for i2 = 1:n2
        for i3 = 1:n3
            for i4 = 1:n4
                for i5 = 1:n5
                    param = [];
                    param.k = knnCandi(i1);
                    param.weightMode = weightCandi{i2};
		    param.t = weight_param_Candi{i3};
                    param.alpha = alphaCandi(i4);
                    param.beta = betaCandi(i5);
                    
                    idx = idx + 1;
                    paramCell{idx} = param;
                end
            end
        end
    end
end
