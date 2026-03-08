import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

st.title('Mortgage payment Calculator')

st.write('### input data')
col1, col2 = st.columns(2)
home_value = col1.number_input('Home Value',min_value=0, value=100000)
down_payment = col1.number_input('Down Payment',min_value=0, value=20000)
interest_rate = col2.number_input('Interest Rate',min_value=0.0, value=3.5)
loan_term = col2.number_input('Loan Term',min_value=1, value=30)

loan_amount = home_value - down_payment
monthly_interest_rate = (interest_rate / 100) / 12
number_of_payments = loan_term * 12
monthly_payment = (
    loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments)/
    ((1 + monthly_interest_rate) ** number_of_payments - 1)
)

total_payment = monthly_payment * number_of_payments
total_interest = total_payment - loan_amount

st.write('### Output')
col1, col2, col3 = st.columns(3)
col1.metric(label = 'Monthly Payment',value = f'{monthly_payment:.2f}')
col2.metric(label = 'Total Payment',value = f'{total_payment:.2f}')
col3.metric(label = 'Total Interest',value = f'{total_interest:.2f}')

# Create a data-frame with the payment schedule.
schedule = []
remaining_balance = loan_amount

for i in range(1, number_of_payments + 1):
    interest_payment = remaining_balance * monthly_interest_rate
    principal_payment = monthly_payment - interest_payment
    remaining_balance -= principal_payment
    year = math.ceil(i / 12)  # Calculate the year into the loan
    schedule.append(
        [
            i,
            monthly_payment,
            principal_payment,
            interest_payment,
            remaining_balance,
            year,
        ]
    )

df = pd.DataFrame(
    schedule,
    columns=["Month", "Payment", "Principal", "Interest", "Remaining Balance", "Year"],
)

# Graphing with Matplotlib
fig, ax = plt.subplots()
ax.plot(df['Month'], df['Remaining Balance'], label='Remaining Balance')
ax.set_xlabel('Month')
ax.set_ylabel('Balance')
ax.set_title('Mortgage Balance Over Time')
ax.legend()
st.pyplot(fig)
