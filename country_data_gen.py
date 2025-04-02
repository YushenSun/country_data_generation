import numpy as np
import pandas as pd

number_rows = 522  # Number of rows you want

# Define the columns for the X data (country states)
columns_X = [
    'GDP', 'Unemployment Rate', 'Inflation Rate', 'Foreign Debt',
    'Government Spending', 'Military Spending', 'Education Spending',
    'Health Spending', 'Environment Spending', 'Technology Investment',
    'Internet Penetration', 'Energy Production', 'Energy Consumption',
    'Pollution Level', 'Population', 'Urbanization Rate', 'Political Stability',
    'Human Development Index', 'Public Trust', 'Freedom of Press', 'Corruption Index',
    'Military Power', 'Alliances', 'Environmental Quality', 'Natural Resources Availability',
    'Trade Balance', 'Public Health', 'Democracy Index', 'Technology Adoption Rate',
    'Cultural Influence', 'Global Trade Index'
]

# Define the columns for the Y data (future actions)
future_action_columns = [
    'Major Political Actions - Future', 'Economic Policy Adjustment - Future', 'Military Activity - Future', 'Diplomatic Policy Change - Future',
    'Social Policy and Welfare Reform - Future', 'Environmental and Energy Policy - Future', 'Technology and Innovation Strategy - Future', 'Public Health and Safety Policy - Future'
]

# Define the action impact rules (positive and negative direction with weights)
action_impacts = {
    'Major Political Actions': {'Positive Direction': 1, 'Negative Direction': -1},
    'Economic Policy Adjustment': {'Positive Direction': 1, 'Negative Direction': -1},
    'Military Activity': {'Positive Direction': 1, 'Negative Direction': -1},
    'Diplomatic Policy Change': {'Positive Direction': 1, 'Negative Direction': -1},
    'Social Policy and Welfare Reform': {'Positive Direction': 1, 'Negative Direction': -1},
    'Environmental and Energy Policy': {'Positive Direction': 1, 'Negative Direction': -1},
    'Technology and Innovation Strategy': {'Positive Direction': 1, 'Negative Direction': -1},
    'Public Health and Safety Policy': {'Positive Direction': 1, 'Negative Direction': -1}
}

# Define the action columns for the dataframe
action_columns = [
    'Major Political Actions', 'Economic Policy Adjustment', 'Military Activity', 'Diplomatic Policy Change',
    'Social Policy and Welfare Reform', 'Environmental and Energy Policy', 'Technology and Innovation Strategy', 'Public Health and Safety Policy'
]

# Initialize the starting values for each parameter based on realistic data (for example, as of 2025)
initial_values = {
    'GDP': 15000,  # Initial GDP in billion USD
    'Unemployment Rate': 5.0,  # Initial Unemployment Rate %
    'Inflation Rate': 2.5,  # Initial Inflation Rate %
    'Foreign Debt': 500,  # Foreign Debt in billion USD
    'Government Spending': 1200,  # Government Spending in billion USD
    'Military Spending': 200,  # Military Spending in billion USD
    'Education Spending': 100,  # Education Spending in billion USD
    'Health Spending': 150,  # Health Spending in billion USD
    'Environment Spending': 50,  # Environment Spending in billion USD
    'Technology Investment': 300,  # Technology Investment in billion USD
    'Internet Penetration': 75.0,  # Initial Internet Penetration %
    'Energy Production': 1200,  # Energy Production in TWh
    'Energy Consumption': 1150,  # Energy Consumption in TWh
    'Pollution Level': 15,  # Pollution Level
    'Population': 1000000000,  # Population
    'Urbanization Rate': 70.0,  # Urbanization Rate %
    'Political Stability': 7.5,  # Political Stability (scale 0-10)
    'Human Development Index': 0.8,  # HDI (scale 0-1)
    'Public Trust': 65.0,  # Public Trust %
    'Freedom of Press': 70.0,  # Freedom of Press %
    'Corruption Index': 40.0,  # Corruption Index
    'Military Power': 1000,  # Military Power (index)
    'Alliances': 3,  # Number of alliances
    'Environmental Quality': 75.0,  # Environmental Quality %
    'Natural Resources Availability': 120,  # Natural Resources Availability
    'Trade Balance': 10,  # Trade Balance
    'Public Health': 85.0,  # Public Health %
    'Democracy Index': 7.0,  # Democracy Index
    'Technology Adoption Rate': 0.6,  # Technology Adoption Rate
    'Cultural Influence': 50.0,  # Cultural Influence (index)
    'Global Trade Index': 0.7  # Global Trade Index
}

# Initialize data lists
data_actions = []
data_future_actions = []

# Generate the first row of actions based on random values within realistic ranges
first_row_actions = []
first_row_future_actions = []

for action in action_impacts:
    action_type = np.random.choice(['Positive Direction', 'Negative Direction'])
    impact = action_impacts[action]
    
    # Randomize the actions with small float values rather than just 1 or -1
    if np.random.rand() < 0.3:  # 30% chance of no action (value = 0)
        action_value = 0
    else:
        action_value = impact[action_type] * np.random.uniform(0.5, 1.5)  # Randomize with magnitude 0.5 to 1.5 times
    
    first_row_actions.append(round(action_value, 2))
    first_row_future_actions.append(round(action_value, 2))

data_actions.append(first_row_actions)
data_future_actions.append(first_row_future_actions)

# Now, for subsequent rows, the current actions will be equal to the previous row's future actions
for i in range(1, number_rows):
    row_actions = []
    row_future_actions = []
    
    # For current actions, take the future actions of the previous row
    for j, action in enumerate(action_columns):
        future_action_value = data_future_actions[i - 1][j]  # Match index
        row_actions.append(future_action_value)

    # Generate future actions based on current state (for simulation)
    for j, action in enumerate(future_action_columns):
        action_type = np.random.choice(['Positive Direction', 'Negative Direction'])
        impact = action_impacts[action.split(' - ')[0]]
        
        # Randomize the future action with small float values
        future_value = impact[action_type] * np.random.uniform(0.5, 1.5)  # Randomize with magnitude 0.5 to 1.5 times
        row_future_actions.append(round(future_value, 2))
    
    # Add the row data to both actions and future actions
    data_actions.append(row_actions)
    data_future_actions.append(row_future_actions)

# Combine X (current data) and Y (future predictions)
df_actions = pd.DataFrame(data_actions, columns=action_columns)
df_future_actions = pd.DataFrame(data_future_actions, columns=future_action_columns)

# Generate X data with realistic fluctuations, including linear growth and periodic variations
data_X_optimized = []
current_values = initial_values.copy()

# Generate the data with fluctuations
for i in range(number_rows):
    row = []
    
    # Add linear growth trend to each parameter (this models the country's overall development)
    growth_trend = 0.0002  # Assumed average annual growth rate of 1% for most parameters
    
    # Periodic terms (sinusoidal variations)
    period_1 = 52.1775  # Annual cycle (weekly data, approximately 1 year per cycle)
    period_2 = 208.71  # Longer cycle (~4 years for example)
    
    # Random phase shifts for each periodic term
    phase_1 = np.random.uniform(0, 2 * np.pi)
    phase_2 = np.random.uniform(0, 2 * np.pi)
    
    for col in columns_X:
        # Base value with linear growth over time
        linear_growth = current_values[col] * (1 + growth_trend)  # Apply growth rate

        # Add periodic sinusoidal fluctuation
        # Scale the periodic fluctuation with respect to the initial value of the parameter
        periodic_1 = np.sin(2 * np.pi * (i / period_1) + phase_1) * (initial_values[col] * np.random.uniform(0.02, 0.05))
        periodic_2 = np.sin(2 * np.pi * (i / period_2) + phase_2) * (initial_values[col] * np.random.uniform(0.02, 0.05))

        # Add a small random fluctuation proportional to the initial value
        random_fluctuation = np.random.uniform(-0.01, 0.01) * initial_values[col]

        # Combine the trend, periodic fluctuations, and random fluctuation
        new_value = linear_growth + periodic_1 + periodic_2 + random_fluctuation
        current_values[col] = new_value  # Update the current value
        
        # Append the new value to the row
        row.append(round(new_value, 2))
    
    data_X_optimized.append(row)


# Create DataFrame for the X data
df_X_optimized = pd.DataFrame(data_X_optimized, columns=columns_X)

# Combine all the data
df_optimized = pd.concat([df_X_optimized, df_actions, df_future_actions], axis=1)

# Save the data to a CSV file for further analysis
df_optimized.to_csv('country_data_optimized.csv', index=False)

# Display the first few rows of the dataframe for verification
print("Displaying Optimized Country Actions and Predictions:")
print(df_optimized.head())
