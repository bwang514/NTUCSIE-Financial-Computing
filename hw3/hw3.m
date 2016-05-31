
initialStockPrice = input('Enter Stock price at time 0 : ');
strikePrice = input('Enter strike price: ');
T = input('Enter maturity in years: ');
V = input('Enter annual volatility: ');
r = input('Enter continuously compounded annual interest rate: ');
n = input('number of periods:');
k = input('number of simulation paths:');
dt = T/n;
ExeTime = (k+1)*ones(n,1); 
R = exp((r-V^2/2)*dt+V*sqrt(dt)*randn(n,k));
stockPrice = cumprod([initialStockPrice*ones(1,k); R]);
Cashflow = zeros(size(stockPrice)); 
Cashflow(end,:) = max(strikePrice-stockPrice(end,:),0);

for i = size(stockPrice)-1:-1:2
    InMoney = find(stockPrice(i,:) < strikePrice); 
    X = stockPrice(i,InMoney)'; X1 = X/initialStockPrice;
    Y = Cashflow(i+1,InMoney)'*exp(-r*dt); 
    R = [ ones(size(X1)) (1-X1) 1/2*(2-4*X1-X1.^2)];
    a = R\Y; 
    C = R*a; 
    exeNow = max(strikePrice-X,0) > C; 
    notExeNow = setdiff((1:k),InMoney(exeNow));
    Cashflow(i,InMoney(exeNow)) = max(strikePrice-X(exeNow),0);
    ExeTime(InMoney(exeNow)) = i;
    Cashflow(i,notExeNow) = exp(-r*dt)*Cashflow(i+1,notExeNow);
end
Price = mean(Cashflow(2,:))*exp(-r*dt)
Standard_Error = std(Cashflow(2,:))/sqrt(length(Cashflow(2,:)))
