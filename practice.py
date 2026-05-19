
#Exercise 1
def amounts_analyser(amounts):
    total= sum(amounts)
    average = total / len(amounts)
    maximum = max(amounts)
    return total, average, maximum

amounts=[27.00,435.75,190.00,380.00,195.00]

total, average, maximum = amounts_analyser(amounts)

print(f"Total: INR{total}")
print(f"Average: INR{average:.2f}")
print(f"Maximum: INR{maximum}")

#Exercise 2

import pandas as pd

#Exercise 2 is filter 500 transactions

df=pd.read_csv("data/sample_transactions.csv")
high_spends = df[df["amount"] > 500]
print("\n--- Transactions over INR 500 ---")
print(high_spends[["date","amount","merchant","category"]])

#Exercise 3

# Error 1 - NameError
#print(undefined_variable)

#error 2 -valueerror
#int("Hi")

#error 3- indexerror

m_list=[1,2,4]
print(m_list[5])