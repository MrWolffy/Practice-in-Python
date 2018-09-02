function [J grad] = nnCostFunction(nn_params, input_layer_size, hidden_layer_size, ...
                                   num_labels, X, y, lambda)

Theta1 = reshape(nn_params(1:hidden_layer_size * (input_layer_size + 1)), ...
                 hidden_layer_size, (input_layer_size + 1));

Theta2 = reshape(nn_params((1 + (hidden_layer_size * (input_layer_size + 1))):(hidden_layer_size * (input_layer_size + hidden_layer_size + 2))), ...
                 hidden_layer_size, (hidden_layer_size + 1));
             
Theta3 = reshape(nn_params((1 + (hidden_layer_size * (input_layer_size + hidden_layer_size + 2))):end), ...
                 num_labels, (hidden_layer_size + 1));

m = size(X, 1);
J = 0;
Theta1_grad = zeros(size(Theta1));
Theta2_grad = zeros(size(Theta2));
Theta3_grad = zeros(size(Theta3));


X = [ones(m, 1) X];
s2 = 1 ./ (1 + exp(-X * Theta1'));
s2 = [ones(m, 1) s2];
s3 = 1 ./ (1 + exp(-s2 * Theta2'));
s3 = [ones(m, 1) s3];
s4 = 1 ./ (1 + exp(-s3 * Theta3'));
for i = 1:m
    J = J + sum(-y(i) .* log(s4(i)) - (1 - y(i)) .* log(1 - s4(i)));
end
J = J / m;
reg = (sum(sum(Theta1(1:hidden_layer_size, 2:(input_layer_size + 1)) .^ 2)) ...
    + sum(sum(Theta2(1:hidden_layer_size, 2:(hidden_layer_size + 1)) .^ 2)) ...  
    + sum(sum(Theta3(1:num_labels, 2:(hidden_layer_size + 1)) .^ 2)));
J = J + lambda * reg / (2 * m);


a1 = X;
z2 = a1 * Theta1';
a2 = [ones(m, 1) 1 ./ (1 + exp(-z2))];
z3 = a2 * Theta2';
a3 = [ones(m, 1) 1 ./ (1 + exp(-z3))];
z4 = a3 * Theta3';
a4 = 1 ./ (1 + exp(-z4));
delta4 = a4 - y;
delta3 = delta4 * Theta3(:, 2:end) .* sigmoidGradient(z3);
delta2 = delta3 * Theta2(:, 2:end) .* sigmoidGradient(z2);
Delta3 = delta4' * a3;
Delta2 = delta3' * a2;
Delta1 = delta2' * a1;
Theta1_grad = Delta1 / m + [zeros(hidden_layer_size, 1) Theta1(:, 2:end)] * lambda / m;
Theta2_grad = Delta2 / m + [zeros(hidden_layer_size, 1) Theta2(:, 2:end)] * lambda / m;
Theta3_grad = Delta3 / m + [zeros(num_labels, 1) Theta3(:, 2:end)] * lambda / m;

grad = [Theta1_grad(:) ; Theta2_grad(:); Theta3_grad(:)];


end
