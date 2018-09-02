function p = predict(Theta1, Theta2, Theta3, X)

m = size(X, 1);
p = zeros(size(X, 1), 1);

h1 = sigmoid([ones(m, 1) X] * Theta1');
h2 = sigmoid([ones(m, 1) h1] * Theta2');
h3 = sigmoid([ones(m, 1) h2] * Theta3');
p = (h3 > 0.5);

end
