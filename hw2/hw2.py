import sys
import math

def Amax(j, i, stock, u, d):
	return (stock * ( ( ( 1 - u**(j-i+1) ) / ( 1 - u ) ) + u**(j-i) * d * ( ( 1 - d**i ) / ( 1 - d ) ) ) / (j+1) )
def Amin(j, i, stock, u, d):
	return ( stock * ( ( ( 1 - d**(i+1) ) / ( 1 - d )) + ( d**i * u * ( ( 1 - u**(j-i) ) / ( 1 - u ) ) ) ) / (j+1) )
def Am(states, m, A_min, A_max):
	return ((float(states) - float(m)) / (float(states) ) * A_min + (float(m) / (float(states))) * A_max)

def asianCall(stock, strike, barrier, maturity, volatility, rate, periods, states, R, u, d, p):
	A = [[0 for x in range(int(states)+1)] for y in range(int(periods)+1)]
	C = [[0 for x in range(int(states)+1)] for y in range(int(periods)+1)]
	D = [0 for x in range(int(states)+1)]
	for i in range(0, periods+1):
		A_min = Amin(periods, i, stock, u, d)
		A_max = Amax(periods, i, stock, u, d)
		for m in range(0, states):
			A[i][m] = Am(states, m, A_min, A_max)
			if ((A[i][m] >= strike) and (A[i][m] < barrier)):
				C[i][m] = A[i][m] - strike
			else:
				C[i][m] = 0.0				
	for j in range(periods - 1, -1, -1):
		for i in range(0, j+1):
			stock_temp = stock * pow(u, j - i) * pow(d, i)
 			A_min = Amin(j, i, stock, u, d)
			A_max = Amax(j, i, stock, u, d)
			for m in range(0, states+1):
				a = Am(states, m, A_min, A_max)
				Au = ( (j + 1) * a + stock_temp * u) / (j + 2.0)
				if(Au >= barrier):
					Cu = 0
				else:
					for l in range(0, states):
						if((A[i][l] <= Au) and (Au <= A[i][l+1])):
							break
					if(A[i][l] == A[i][l+1]):
						x = 1
					else:
						x = (Au - A[i][l+1]) / (A[i][l] - A[i][l+1])
					Cu = x * C[i][l] + (1 - x) * C[i][l+1]
				Ad = ( (j + 1) * a + stock_temp * d) / (j + 2.0)
				if(Ad >= barrier):
						Cd = 0
				else:
					for l in range(0, states):
						if((A[i+1][l] <= Ad) and (Ad <= A[i+1][l+1])):
							break
					if(A[i+1][l] == A[i+1][l+1]):
						x = 1
					else:
						x = (Ad - A[i+1][l+1]) / (A[i+1][l] - A[i+1][l+1])
					Cd = x * C[i+1][l] + (1 - x) * C[i+1][l+1]

				D[m] = max( a - strike  , ((p * Cu + (1 - p) * Cd) / R) ) #e^-r?
			for m in range(0, states+1):
				C[i][m] = D[m]
				A[i][m] = Am(states, m, A_min, A_max)
	
	
	print "Price = %4.4f" % C[0][0]

if __name__ == '__main__':
	print "Please input stock"
	stock = float(input())
	print "Please input strike"
	strike = float(input())
	print "Please input barrier"
	barrier = float(input())
	print "Please input maturity"
	maturity = float(input())
	print "Please input volatility"
	volatility = float(raw_input().strip('%')) / 100.0
	print "Please input rate"
	rate = float(raw_input().strip('%')) / 100.0
	print "Please input periods"
	periods = int(input())
	print "Please input states"
	states = int(input()) + 1
	print "Please wait for calculation"
	R = math.exp(rate / (periods/maturity) )
	u = math.exp(volatility * ((maturity/periods)**(0.5)))
	d = 1.0/u
	p = (R - d) / (u - d)
	asianCall(stock, strike, barrier, maturity, volatility, rate, periods, states, R, u, d, p)