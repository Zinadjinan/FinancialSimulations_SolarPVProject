import streamlit as st
import pandas as pd

# Function to input variables
def input_variables():
    st.sidebar.subheader("Project Characteristics")
    Installed_capacity = st.sidebar.number_input("Installed capacity (MW):", min_value=0)
    Productivity = st.sidebar.number_input("Productivity (MWh/MW):", min_value=0)
    economic_life = st.sidebar.number_input("Economic life (Years):", min_value=0)
    Energy_Yield_Degradation_Rate_20 = st.sidebar.number_input("Energy Yield Degradation Rate (%) for the first 20 years:", min_value=0.0)
    Energy_Yield_Degradation_Rate_last = st.sidebar.number_input(f"Energy Yield Degradation Rate (%) for the last {economic_life - 20} years:", min_value=0.0)
    Implementation_Duration = st.sidebar.number_input("Implementation Duration (months):", min_value=0)
    Production_Rate_firstyear = st.sidebar.number_input("Production Rate during the first year of operation (MWh/MW):", min_value=0.0)

    st.sidebar.subheader("Economic Assumptions")
    inflation_rate = st.sidebar.number_input("Inflation rate (%):", min_value=0.0)
    Exchange_rate = st.sidebar.number_input("Exchange rate:", min_value=0.0)

    st.sidebar.subheader("Capex Cost Assumptions")
    Cost_perkWp_installed = st.sidebar.number_input("Cost per kWp installed ($/kWc):", min_value=0)
    Grid_Connection_Cost = st.sidebar.number_input("Grid Connection Cost ($):", min_value=0)
    GridConnection_Length = st.sidebar.number_input("Grid Connection Length (meters):", min_value=0)

    st.sidebar.subheader("Opex Cost Assumptions")
    Maintenance_cost_perkWp = st.sidebar.number_input("Maintenance cost per kWp ($/kWp/year):", min_value=0)
    Maintenance_Cost_Increase_Rate = st.sidebar.number_input(f"Maintenance Cost Increase Rate (%) (applied for the last {economic_life - 20} years):", min_value=0.0)
    Labor_Cost = st.sidebar.number_input("Labor Cost ($/agent/year):", min_value=0)
    Number_employees = st.sidebar.number_input("Number of employees:", min_value=0)
    Insurance_Rate = st.sidebar.number_input("Insurance Rate (% of Investment):", min_value=0.0)
    indirectCost_Rate = st.sidebar.number_input("Indirect Cost Rate (%):", min_value=0.0)
    
    st.sidebar.subheader("Profitability Assumptions")
    Required_Equity_Return = st.sidebar.number_input("Required Equity Return (%):", min_value=0.0)
    Selling_Price = st.sidebar.number_input("Selling Price ($/MWh):", min_value=0.0)

    Net_Production = (Installed_capacity * Productivity)
    TotalCost_PowerPlant = (Cost_perkWp_installed * Installed_capacity * 1000 * 1,19 * Exchange_rate)
    TotalCost_GridConnexion = (Grid_Connection_Cost * GridConnection_Length * 1,19 * Exchange_rate)
    Total_Capex = TotalCost_PowerPlant + TotalCost_GridConnexion
    Annual_Capital_Amortization = Total_Capex/economic_life

    Maintenance_cost = Maintenance_cost_perkWp * Installed_capacity *1000 
    Operating_costs = (Maintenance_cost + (Labor_Cost * Number_employees) 
                    + (Insurance_Rate*TotalCost_PowerPlant*(1-0,19))) * (1+indirectCost_Rate)
        
    variables = {
        "Project Characteristics": {
            "Installed_capacity": Installed_capacity,
            "Productivity": Productivity,
            "economic_life": economic_life,
            "Energy_Yield_Degradation_Rate_20": Energy_Yield_Degradation_Rate_20,
            "Energy_Yield_Degradation_Rate_last": Energy_Yield_Degradation_Rate_last,
            "Implementation_Duration": Implementation_Duration,
            "Production_Rate_firstyear": Production_Rate_firstyear,
            "Net_Production" : Net_Production
        },
        "Economic Assumptions": {
            "inflation_rate": inflation_rate,
            "Exchange_rate": Exchange_rate
        },
        "Capex Cost Assumptions": {
            "Cost_perkWp_installed": Cost_perkWp_installed,
            "Grid_Connection_Cost": Grid_Connection_Cost,
            "GridConnection_Length": GridConnection_Length,
            "TotalCost_PowerPlant" : TotalCost_PowerPlant,
            "TotalCost_GridConnexion" : TotalCost_GridConnexion,
            "Total_Capex" : Total_Capex,
            "Annual_Capital_Amortization" : Annual_Capital_Amortization

        },
        "Opex Cost Assumptions": {
            "Maintenance_cost_perkWp": Maintenance_cost_perkWp,
            "Maintenance_Cost_Increase_Rate": Maintenance_Cost_Increase_Rate,
            "Labor_Cost": Labor_Cost,
            "Number_employees": Number_employees,
            "Insurance_Rate": Insurance_Rate,
            "indirectCost_Rate": indirectCost_Rate,
            "Maintenance_cost" : Maintenance_cost,
            "Operating_costs" : Operating_costs
        },        
        "Profitability Assumptions": {
            "Required_Equity_Return": Required_Equity_Return,
            "Selling_Price": Selling_Price,
        }
    }

    return variables



# Function to input financial options
def input_financial_assumptions(Total_Capex):
    st.sidebar.subheader("Financing Assumptions")
    Equity_rates = []
    Loan_rates = []
    Interest_Rates = []
    Loans_Term = []
    Repayment_Installments = []
    Grace_Periods = []
    Principals = []
    Discount_Rates = [] 
    Required_Equity_Returns = []
    
    while True:
        try:
            Equity_rate = st.sidebar.number_input("Equity rate (%):", min_value=0.0)
            Loan_rate = st.sidebar.number_input("Loan rate (%):", min_value=0.0)
            Interest_Rate = st.sidebar.number_input("Interest Rate (%):", min_value=0.0)
            Loan_Term = st.sidebar.number_input("Loan Term (years):", min_value=0)
            Repayment_Installment = st.sidebar.number_input("Repayment Installments per Year:", min_value=0)
            Grace_Period = st.sidebar.number_input("Grace Period (years):", min_value=0)
            Required_Equity_Return = st.sidebar.number_input("Required_Equity_Return : ", min_value=0)

            if Loan_Term <= Grace_Period:
                st.sidebar.error("Loan Term should be greater than Grace Period.")
                continue

            Principal = Total_Capex * Loan_rate / (Loan_Term - Grace_Period)
            Discount_Rate = (Equity_rate * Required_Equity_Return) + (Loan_rate * Interest_Rate)
            
            # Append the values to the respective lists
            Equity_rates.append(Equity_rate)
            Loan_rates.append(Loan_rate)
            Interest_Rates.append(Interest_Rate)
            Loans_Term.append(Loan_Term)
            Repayment_Installments.append(Repayment_Installment)
            Grace_Periods.append(Grace_Period)
            Principals.append(Principal)
        except ValueError:
            break

    # Create a DataFrame from the input values
    Fin_Options_df = pd.DataFrame({
        "Equity_rate": Equity_rates,
        "Loan_rate": Loan_rates,
        "Interest_Rate": Interest_Rates,
        "Loan_Term": Loans_Term,
        "Repayment_Installments": Repayment_Installments,
        "Grace_Period": Grace_Periods,
        "Principal": Principals
    })

    return Fin_Options_df

# Function to input capital expenditure data
def input_capex_data():
    st.subheader("Input Capital Expenditure Data")
    years = []
    capex_values = []

    while True:
        try:
            year = st.number_input("Enter the year (or any non-integer to exit):", min_value=0)
            capex = st.number_input("Enter the Capital Expenditure for that year ($):", min_value=0.0)

            years.append(year)
            capex_values.append(capex)
        except ValueError:
            break

    capex_data = pd.DataFrame({
        "Year": years,
        "Capital_Expenditure": capex_values
    })

    return capex_data

# Function to perform calculations
def Display_variables(variables):
    # Display selected variables
    st.subheader("Selected Variables")
    selected_variables = st.multiselect("Select variables to display:", variables.keys())

    for section in selected_variables:
        st.subheader(section)
        for variable, value in variables[section].items():
            st.write(f"{variable}: {value}")

# Main function to run the Streamlit app
def main():
    st.title("Solar PV Project Calculator")
    st.sidebar.title("Input Assumptions")

    variables = input_variables()
    capex_data = input_capex_data()
    Display_variables(variables, capex_data)

if __name__ == "__main__":
    main()


def calculate_annual_net_production(Net_Production, Production_Rate_firstyear,
                                    Energy_Yield_Degradation_Rate_20, Energy_Yield_Degradation_Rate_last, index):
    if index == 0:
        Annual_Net_Production = 0
    elif index == 1:
        Annual_Net_Production = Net_Production * Production_Rate_firstyear
    elif 2 < index < 20:
        Annual_Net_Production = Net_Production * (1 - Energy_Yield_Degradation_Rate_20 / 100)
    else:
        Annual_Net_Production = Net_Production * (1 - Energy_Yield_Degradation_Rate_20 / 100 - Energy_Yield_Degradation_Rate_last / 100)
    return Annual_Net_Production

def calculate_current_charges(Production_Rate_firstyear, current_charges, index):
    if index == 0:
        current_charges = 0
    elif index == 1:
        current_charges = current_charges * Production_Rate_firstyear
    else:
        current_charges = current_charges

    return current_charges

def calculate_annual_capital_amortization(Production_Rate_firstyear, Annual_Capital_Amortization, index):
    if index == 0:
        Annual_Capital_Amortization = 0
    elif index == 1:
        Annual_Capital_Amortization = Annual_Capital_Amortization * Production_Rate_firstyear
    else:
        Annual_Capital_Amortization = Annual_Capital_Amortization
    return Annual_Capital_Amortization

def generate_dataframe(economic_life, Selling_Price, Net_Production, Production_Rate_firstyear,
                       Energy_Yield_Degradation_Rate_20, Energy_Yield_Degradation_Rate_last, df_credit_tab, capex_data):
    data = {
        'Annual_Net_Production': [calculate_annual_net_production(Net_Production, Production_Rate_firstyear,
                                                                  Energy_Yield_Degradation_Rate_20,
                                                                  Energy_Yield_Degradation_Rate_last, i)
                                  for i in range(economic_life + 2)],
        'Selling_Price': [Selling_Price] * (economic_life + 2),
        'current_charges': [calculate_current_charges(Production_Rate_firstyear, 0, i) for i in range(economic_life + 2)],
        'amortization': [calculate_annual_capital_amortization(Production_Rate_firstyear, 0, i) for i in range(economic_life + 2)]
    }

    df = pd.DataFrame(data)

    # Calculate and add "Electricity_Sales" column
    df['Electricity_Sales'] = df['Selling_Price'] * df['Annual_Net_Production']
    df['operating_costs'] = df['current_charges'] + df['amortization']
    df['Gross_Operating_Income'] = df['Electricity_Sales'] - df['operating_costs']
    df['professional_taxes'] = df['Electricity_Sales'] * 0.01
    df['Various_taxes'] = df['Electricity_Sales'] * 0.05
    
    df['Interest'] = df_credit_tab['Interest']
    df['total_charge'] = df['operating_costs'] + df['Interest'] + df['professional_taxes'] + df['Various_taxes']
    df['net_profit_before_tax'] = df['Gross_Operating_Income'] - df['Interest'] - df['professional_taxes'] - df['Various_taxes']
    df['Capex'] = capex_data['Capital_Expenditure']
    df['Inflow'] = df['net_profit_before_tax'] + df['amortization']
    df['Cashflow'] = df['Inflow'] + df['Capex']
    df['Cumulated_Cshflow'] = df['Cshflow'].cumsum()

    return df


import pandas as pd

def amortization_schedule(principal, annual_interest_rate, duration_years):
    # Calculate the number of months and monthly interest rate
    num_months = duration_years * 12
    monthly_interest_rate = annual_interest_rate / 12
    
    # Calculate the monthly payment (amortization)
    monthly_payment = (principal * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** -num_months)
    
    # Initialize lists to store data
    months = []
    remaining_balances = []
    principal_payments = []
    interest_payments = []
    
    # Initialize the remaining balance
    remaining_balance = principal
    
    # Generate the amortization schedule
    for month in range(1, num_months + 1):
        interest_payment = remaining_balance * monthly_interest_rate
        principal_payment = monthly_payment - interest_payment
        remaining_balance -= principal_payment
        
        # Append data to lists
        months.append(month)
        principal_payments.append(principal_payment)
        interest_payments.append(interest_payment)
        remaining_balances.append(remaining_balance)
    
    # Create a DataFrame from the lists
    amortization_df = pd.DataFrame({
        "Month": months,
        "Principal Payment": principal_payments,
        "Interest Payment": interest_payments,
        "Remaining Balance": remaining_balances
    })
    
    return amortization_df

# Example usage:
principal_amount = 10000  # Principal amount of the loan
annual_interest_rate = 0.05  # Annual interest rate (5%)
loan_duration_years = 5  # Loan duration in years

amortization_table = amortization_schedule(principal_amount, annual_interest_rate, loan_duration_years)
print(amortization_table)
