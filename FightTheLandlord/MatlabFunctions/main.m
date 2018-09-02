clear ; close all; clc


%% 初始化全局变量
input_layer_size  = 540;
hidden_layer_size = 30;
num_labels = 1;


%% 初始化数据
data = csvread("../data.csv");
y = data(:, 1);
X = data(:, 2:end-1);
m = size(X, 1);
fprintf("初始化数据完成\n")


%% 初始化参数
Theta1 = randInitializeWeights(input_layer_size, hidden_layer_size);
Theta2 = randInitializeWeights(hidden_layer_size, hidden_layer_size);
Theta3 = randInitializeWeights(hidden_layer_size, num_labels);
nn_params = [Theta1(:) ; Theta2(:); Theta3(:)];
fprintf("初始化参数完成\n")


%% 训练模型
options = optimset('MaxIter', 500);
lambda = 0;
costFunction = @(p) nnCostFunction(p, input_layer_size, hidden_layer_size, ...
    num_labels, X, y, lambda);

[nn_params, cost] = fmincg(costFunction, nn_params, options);

Theta1 = reshape(nn_params(1:hidden_layer_size * (input_layer_size + 1)), ...
                 hidden_layer_size, (input_layer_size + 1));
Theta2 = reshape(nn_params((1 + (hidden_layer_size * (input_layer_size + 1))):(hidden_layer_size * (input_layer_size + hidden_layer_size + 2))), ...
                 hidden_layer_size, (hidden_layer_size + 1));
Theta3 = reshape(nn_params((1 + (hidden_layer_size * (input_layer_size + hidden_layer_size + 2))):end), ...
                 num_labels, (hidden_layer_size + 1));
fprintf("训练模型完成\n")


%% 预测
pred = predict(Theta1, Theta2, Theta3, X);
fprintf('预测准确率: %f\n', mean(double(pred == y)) * 100);


%% 存储结果
f = fopen("../theta1.txt", "w");
for i = 1:30
    for j = 1:541
        fprintf(f, "%f ", Theta1(i, j));
    end
    fprintf(f, "\n");
end
f = fopen("../theta2.txt", "w");
for i = 1:30
    for j = 1:31
        fprintf(f, "%f ", Theta2(i, j));
    end
    fprintf(f, "\n");
end
f = fopen("../theta3.txt", "w");
for i = 1:31
    fprintf(f, "%f\n", Theta3(1, i));
end
