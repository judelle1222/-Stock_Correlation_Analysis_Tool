import yfinance as yf
import matplotlib.pyplot as plt

# Ask user for stocks
stock1 = input("Pick your first stock (e.g., AAPL, MSFT): ").upper().strip()
stock2 = input("Pick your second stock (e.g., HD, GE): ").upper().strip()

# Function to download data and calculate daily average price
def download_data(stock1, stock2):
    data = yf.download([stock1, stock2], period = "365d")

# If no data was downloaded (invalid ticker/no trading days) -> returns empty list
    if len(data) == 0:
        return [],[]

    stocks = []
    dates = []

    # Loops/iterates through each trading day row 
    i = 0
    while i < len(data):

        # Gets high, low, closing price for stock 1 on day i
        if i < len(data):
            h1 = data["High"][stock1][i]  
            l1 = data["Low"][stock1][i]     
            c1 = data["Close"][stock1][i]
        
        # Gets high, low, closing price for stock 2 on day i
        if i < len(data):
            h2 = data["High"][stock2][i] 
            l2 = data["Low"][stock2][i]     
            c2 = data["Close"][stock2][i] 


        # Skip non-existent values
        if (h1 == h1) and (l1 == l1) and (c1 == c1) and (h2 == h2) and (l2 == l2) and (c2 == c2):
            # Finds daily average price for both stocks
            total1 = (h1 + l1 + c1)
            avg1 = total1 / 3

            total2 = (h2 + l2 + c2)
            avg2 = total2 / 3

            # Stores both averages together for same day
            stocks.append([avg1, avg2])
            #Gets the label (date) of the ith row
            dates.append(data.index[i])

        i = i + 1

    return stocks, dates

# Function to calculate Pearson correlation and line of best fit
def pearson_and_bestfit(stocks):
    n_total = len(stocks)
    if n_total < 2:
        return 0.0, 0.0, 0.0
    # Calculate sums
    SX = 0
    SY = 0
    SXY = 0
    SXX = 0
    SYY = 0

    i = 0
    while i < n_total:
        X = stocks[i][0]
        Y = stocks[i][1]

        SX = SX + X
        SY = SY + Y
        SXY = SXY + (X * Y)
        SXX = SXX + (X * X)
        SYY = SYY + (Y * Y)

        i = i + 1

    # Pearson Correlation
    numerator = (n_total * SXY) - (SX * SY)
    denom = ((n_total * SXX - SX*SX) * (n_total * SYY - SY*SY)) ** 0.5
    if denom == 0:
        return 0.0, 0.0, 0.0
    r = numerator / denom

    meanx = SX / n_total
    meany = SY / n_total

    # Line of best fit (y = a + b*x)
    sum_diff_x_sq = 0
    sum_diff_y_sq = 0

    for i in range(len(stocks)):
        s = stocks[i]
        sum_diff_x_sq = sum_diff_x_sq + ((s[0] - meanx) ** 2)
        sum_diff_y_sq = sum_diff_y_sq + ((s[1] - meany) ** 2)

    stdx = (sum_diff_x_sq / (n_total - 1)) ** 0.5
    stdy = (sum_diff_y_sq / (n_total - 1)) ** 0.5
    
    if stdx != 0:
        b = r * (stdy / stdx)
    else:
        b = 0
        
    a = meany - b * meanx

    return r, a, b

# Main Program
stocks, dates = download_data(stock1, stock2)

if len(stocks) < 2:
    print("Data error: not enough data.")
    exit()

stock1_list = []
stock2_list = []
days = []

i = 0
while i < len(stocks):
    stock1_list.append(stocks[i][0])
    stock2_list.append(stocks[i][1])
    days.append(i + 1)
    i = i + 1

r, a, b = pearson_and_bestfit(stocks)

# Determine correlation meaning
if r > 0.7:
    correlationText = "Strong positive correlation: the stocks tend to move in the same direction."
elif r > 0.3:
    correlationText = "Moderate positive correlation: the stocks somewhat move together."
elif r > 0:
    correlationText = "Weak positive correlation: the stocks slightly move together."
elif r < -0.7:
    correlationText = "Strong negative correlation: the stocks tend to move in opposite directions."
elif r < -0.3:
    correlationText = "Moderate negative correlation: the stocks somewhat move oppositely."
elif r < 0:
    correlationText = "Weak negative correlation: the stocks slightly move oppositely."
else:
    correlationText = "No correlation: the stocks move independently."

# Opens file with results of Pearson and line of best fit for both stocks
with open ("stock_results.txt" , "w") as f:
    f.write("Thanks for trying out our program! Here are your results: \n")
    f.write("\n Results for " + stock1 + " vs " + stock2 + ":\n")
    f.write("Pearson r: " + str(r) + "\n")
    f.write("Best fit: y = " + str(a) + " + " + str(b) + "x\n")
    f.write("Interpretation: " + correlationText + "\n")

# Time plot of stock1 & stock2
plt.figure() # Shows both grahps in one screen
y1 = stock1_list
y2 = stock2_list
plt.plot(days, y1, label = stock1)
plt.plot(days, y2, label = stock2)

# Labels, titles, legend
plt.xlabel("Days")
plt.ylabel("Avg Price ($)")
plt.title(stock1 + " & " + stock2 + " - Last 365 Days")
plt.legend()


# Scatter plot with line of best fit
plt.figure()
plt.scatter(stock1_list, stock2_list, s = 10, label = "Daily points")
x_start = min(stock1_list)
x_end = max(stock1_list)
y_start = a + b * x_start
y_end = a + b * x_end

line_x = [x_start, x_end]
line_y = [y_start, y_end]
plt.plot(line_x, line_y, linestyle = "--", label = "Best Fit")

# Labels, titles, legend
plt.xlabel(stock1 + " avg price")
plt.ylabel(stock2 + " avg price")
plt.title(stock1 + " vs " + stock2)
plt.legend()
plt.show()

'''
----Test 1:

--Inputs: AAPL, MSFT 

--Expected Output:
|
Thanks for trying out our program! Here are your results: 

 Results for AAPL vs MSFT:
Pearson r: 0.3719506672469587
Best fit: y = 264.02323142907596 + 0.8025955647116693x
Interpretation: Moderate positive correlation: the stocks somewhat move together.



----Test 2: 

--Inputs: MSFT, GOOGL

--Expected Output: 
|
Thanks for trying out our program! Here are your results: 

 Results for MSFT vs GOOGL:
Pearson r: 0.6617981003005222
Best fit: y = -78.84171988395977 + 0.6087107677610736x
Interpretation: Moderate positive correlation: the stocks somewhat move together.



----Test 3: 

--Inputs: AMZN, WMT

--Expected Output:
|
Thanks for trying out our program! Here are your results: 

 Results for AMZN vs WMT:
Pearson r: 0.7725941941218296
Best fit: y = 2.6305699220946934 + 0.425842528002539x
Interpretation: Strong positive correlation: the stocks tend to move in the same direction.



'''

