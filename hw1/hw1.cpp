#include <iostream>
#include <cmath>
#include <cstdio>

using namespace std;

int main(){
	int numberOfCashFlows,i;
	cin >> numberOfCashFlows;
	double averageRate = 0,w,spotRates[numberOfCashFlows],CashFlows[numberOfCashFlows],MD_mol = 0,MD_den = 0,macaulayDuration,modifiedDuration,convexityTmp = 0,convexity;
	for(i = 0;i < numberOfCashFlows;i++)
		cin >> spotRates[i];
	for(i = 0;i < numberOfCashFlows;i++)
		cin >> CashFlows[i];
	cin >> w;
	for(i = 0;i < numberOfCashFlows;i++){
		MD_den += CashFlows[i] / pow((1 + spotRates[i]),(i + w));
		MD_mol += ((i + w) * CashFlows[i]) / pow((1 + spotRates[i]),(i + w));
	}

	macaulayDuration = MD_mol / MD_den;
	modifiedDuration = macaulayDuration / (1 + spotRates[numberOfCashFlows - 1]);
	for(i = 0; i < numberOfCashFlows;i++)
		convexityTmp += ((i + w) * (i + w + 1) * CashFlows[i]) / pow((1 + spotRates[i]),(i + w + 2));
	convexity = convexityTmp / MD_den;
	printf("Modified Duration = %.4lf\n", modifiedDuration);
	printf("Convexity = %.4lf\n",convexity);


}