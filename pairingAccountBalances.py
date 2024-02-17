import os
import csv
import time


# Start time of proccess
start = time.time()

# your input files should be named this 
inputFileName = "transactions.csv"
balancesFileName = "accountBalances20182022.txt"


outputFileName = "outputTransactions.csv"

# outer list to save rows in
transactions = []
amounts_column = []
comments_column =[]

inputFile = open(inputFileName)
inputReader = csv.reader(inputFile)
for row in inputReader:
    # inner list to save values in memory
    transactions.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]])
    # Values in these columns are set aside to maintain the same output structure as PAS
    amounts_column.append(row[10])
    comments_column.append(row[11])

balancesFile = open(balancesFileName)
balancesReader = csv.reader(balancesFile, delimiter=",")
balancesData = list(balancesReader)
# new list to save the data in memory
NewTransactions = []
# comparing snno and sponsor codes together to pull out 2018 values
for transactionsRow in transactions:
    for balancesRow in balancesData:
        if (transactionsRow[4]==balancesRow[0]) and (transactionsRow[2]==balancesRow[1]):
            transactionsRow.append(balancesRow[2])
    NewTransactions.append(transactionsRow)
    print(f"2018 value for row {len(NewTransactions)} has been added")

# Saves the current row the transfer process is on 
row_count = 0 

# Block of code for removing duplicate values 
print("\nNow checking for duplicate values...\n")
for transactions in NewTransactions:
    row_count += 1
    if (len(transactions) > 11):
        number_of_duplicates = len(transactions) - 11
        print(f"Row {row_count} has duplicate {number_of_duplicates} values. \nAdding up the duplicates...")
        number_as_float_sum = float(transactions[10])
        for value in range(number_of_duplicates):
            number_as_float_sum = number_as_float_sum + float(transactions[11])
            transactions.pop(11)
        transactions[10] = number_as_float_sum
        transactions.append(amounts_column[0])
        amounts_column.pop(0)
        transactions.append(comments_column[0])
        comments_column.pop(0)
    else:
        # 
        transactions.append(amounts_column[0])
        amounts_column.pop(0)
        transactions.append(comments_column[0])
        comments_column.pop(0)
print("\nAll duplicate values have been deleted")

outputFile = open(outputFileName, 'w', newline='')
outputRowWriter = csv.writer(outputFile)
# Writing the headers for the output file 
outputRowWriter.writerow(["Action", "Scheme", "Sponsor", "Person", "SSNIT", "Entry Date" , "Value Date", "Modified By", "Modified Date", "Time", "2018 Balances", "Amount", "Comments"])
for row in NewTransactions:
    outputRowWriter.writerow(row)
outputFile.close()

end = time.time()

print("\nExecution time in seconds: ",(end-start))