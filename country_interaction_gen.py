import numpy as np
import pandas as pd

number_rows = 522  # Number of rows you want

# Define the columns for the X data (country states for A and B and their relations)
columns_X = [
    # A state parameters
    'A GDP', 'A Unemployment Rate', 'A Inflation Rate', 'A Foreign Debt',
    'A Government Spending', 'A Military Spending', 'A Education Spending',
    'A Health Spending', 'A Environment Spending', 'A Technology Investment',
    'A Internet Penetration', 'A Energy Production', 'A Energy Consumption',
    'A Pollution Level', 'A Population', 'A Urbanization Rate', 'A Political Stability',
    'A Human Development Index', 'A Public Trust', 'A Freedom of Press', 'A Corruption Index',
    'A Military Power', 'A Alliances', 'A Environmental Quality', 'A Natural Resources Availability',
    'A Trade Balance', 'A Public Health', 'A Democracy Index', 'A Technology Adoption Rate',
    'A Cultural Influence', 'A Global Trade Index',

    # B state parameters
    'B GDP', 'B Unemployment Rate', 'B Inflation Rate', 'B Foreign Debt',
    'B Government Spending', 'B Military Spending', 'B Education Spending',
    'B Health Spending', 'B Environment Spending', 'B Technology Investment',
    'B Internet Penetration', 'B Energy Production', 'B Energy Consumption',
    'B Pollution Level', 'B Population', 'B Urbanization Rate', 'B Political Stability',
    'B Human Development Index', 'B Public Trust', 'B Freedom of Press', 'B Corruption Index',
    'B Military Power', 'B Alliances', 'B Environmental Quality', 'B Natural Resources Availability',
    'B Trade Balance', 'B Public Health', 'B Democracy Index', 'B Technology Adoption Rate',
    'B Cultural Influence', 'B Global Trade Index',

    # Relationship Parameters
    'A to B Imports', 'A to B Exports', 'B to A Imports', 'B to A Exports',
    'A Bond Status', 'B Bond Status', 'A Sovereignty Disputes', 'B Sovereignty Disputes',
    'Political Similarity', 'Ethnic Similarity', 'Cultural Compatibility'
]

# Define the columns for the Y data (future actions)
future_action_columns = [
    'Major Political Actions - Future', 'Economic Policy Adjustment - Future', 'Military Activity - Future', 'Diplomatic Policy Change - Future',
    'Social Policy and Welfare Reform - Future', 'Environmental and Energy Policy - Future', 'Technology and Innovation Strategy - Future', 'Public Health and Safety Policy - Future',

    # Actions between A and B
    'A Major Political Actions - Future', 'A Economic Policy Adjustment - Future', 'A Military Activity - Future', 'A Diplomatic Policy Change - Future',
    'A Social Policy and Welfare Reform - Future', 'A Environmental and Energy Policy - Future', 'A Technology and Innovation Strategy - Future', 'A Public Health and Safety Policy - Future',

    'B Major Political Actions - Future', 'B Economic Policy Adjustment - Future', 'B Military Activity - Future', 'B Diplomatic Policy Change - Future',
    'B Social Policy and Welfare Reform - Future', 'B Environmental and Energy Policy - Future', 'B Technology and Innovation Strategy - Future', 'B Public Health and Safety Policy - Future'
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
    'Public Health and Safety Policy': {'Positive Direction': 1, 'Negative Direction': -1},

    # Actions related to A and B
    'A Major Political Actions': {'Positive Direction': 1, 'Negative Direction': -1},
    'A Economic Policy Adjustment': {'Positive Direction': 1, 'Negative Direction': -1},
    'A Military Activity': {'Positive Direction': 1, 'Negative Direction': -1},
    'A Diplomatic Policy Change': {'Positive Direction': 1, 'Negative Direction': -1},
    'A Social Policy and Welfare Reform': {'Positive Direction': 1, 'Negative Direction': -1},
    'A Environmental and Energy Policy': {'Positive Direction': 1, 'Negative Direction': -1},
    'A Technology and Innovation Strategy': {'Positive Direction': 1, 'Negative Direction': -1},
    'A Public Health and Safety Policy': {'Positive Direction': 1, 'Negative Direction': -1},

    'B Major Political Actions': {'Positive Direction': 1, 'Negative Direction': -1},
    'B Economic Policy Adjustment': {'Positive Direction': 1, 'Negative Direction': -1},
    'B Military Activity': {'Positive Direction': 1, 'Negative Direction': -1},
    'B Diplomatic Policy Change': {'Positive Direction': 1, 'Negative Direction': -1},
    'B Social Policy and Welfare Reform': {'Positive Direction': 1, 'Negative Direction': -1},
    'B Environmental and Energy Policy': {'Positive Direction': 1, 'Negative Direction': -1},
    'B Technology and Innovation Strategy': {'Positive Direction': 1, 'Negative Direction': -1},
    'B Public Health and Safety Policy': {'Positive Direction': 1, 'Negative Direction': -1}
}

# Define the action columns for the dataframe
action_columns = [
    'Major Political Actions', 'Economic Policy Adjustment', 'Military Activity', 'Diplomatic Policy Change',
    'Social Policy and Welfare Reform', 'Environmental and Energy Policy', 'Technology and Innovation Strategy', 'Public Health and Safety Policy',

    # Actions related to A and B
    'A Major Political Actions', 'A Economic Policy Adjustment', 'A Military Activity', 'A Diplomatic Policy Change',
    'A Social Policy and Welfare Reform', 'A Environmental and Energy Policy', 'A Technology and Innovation Strategy', 'A Public Health and Safety Policy',

    'B Major Political Actions', 'B Economic Policy Adjustment', 'B Military Activity', 'B Diplomatic Policy Change',
    'B Social Policy and Welfare Reform', 'B Environmental and Energy Policy', 'B Technology and Innovation Strategy', 'B Public Health and Safety Policy'
]

# Initialize the starting values for each parameter based on realistic data (for example, as of 2025)
initial_values = {
    # A state parameters
    'A GDP': 10000, 'A Unemployment Rate': 6.0, 'A Inflation Rate': 3.0, 'A Foreign Debt': 300, 'A Government Spending': 800,
    'A Military Spending': 150, 'A Education Spending': 70, 'A Health Spending': 120, 'A Environment Spending': 30, 'A Technology Investment': 250,
    'A Internet Penetration': 70.0, 'A Energy Production': 900, 'A Energy Consumption': 850, 'A Pollution Level': 20, 'A Population': 500000000,
    'A Urbanization Rate': 60.0, 'A Political Stability': 6.5, 'A Human Development Index': 0.75, 'A Public Trust': 60.0, 'A Freedom of Press': 60.0,
    'A Corruption Index': 50.0, 'A Military Power': 800, 'A Alliances': 2, 'A Environmental Quality': 70.0, 'A Natural Resources Availability': 100,
    'A Trade Balance': 15, 'A Public Health': 80.0, 'A Democracy Index': 6.0, 'A Technology Adoption Rate': 0.5, 'A Cultural Influence': 40.0, 'A Global Trade Index': 0.6,

    # B state parameters
    'B GDP': 12000, 'B Unemployment Rate': 5.5, 'B Inflation Rate': 2.0, 'B Foreign Debt': 400, 'B Government Spending': 1000,
    'B Military Spending': 180, 'B Education Spending': 90, 'B Health Spending': 140, 'B Environment Spending': 40, 'B Technology Investment': 280,
    'B Internet Penetration': 80.0, 'B Energy Production': 1100, 'B Energy Consumption': 1000, 'B Pollution Level': 18, 'B Population': 750000000,
    'B Urbanization Rate': 75.0, 'B Political Stability': 8.0, 'B Human Development Index': 0.85, 'B Public Trust': 70.0, 'B Freedom of Press': 80.0,
    'B Corruption Index': 35.0, 'B Military Power': 1200, 'B Alliances': 4, 'B Environmental Quality': 80.0, 'B Natural Resources Availability': 110,
    'B Trade Balance': 20, 'B Public Health': 90.0, 'B Democracy Index': 8.0, 'B Technology Adoption Rate': 0.7, 'B Cultural Influence': 60.0, 'B Global Trade Index': 0.8,

    # Relationship parameters
    'A to B Imports': 200, 'A to B Exports': 150, 'B to A Imports': 180, 'B to A Exports': 130,
    'A Bond Status': 1, 'B Bond Status': 1, 'A Sovereignty Disputes': 0, 'B Sovereignty Disputes': 0,
    'Political Similarity': 0.6, 'Ethnic Similarity': 0.5, 'Cultural Compatibility': 0.7
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
    period_1 = 52.177142857  # Annual cycle (weekly data, approximately 1 year per cycle)
    period_2 = 208.70857142857  # Longer cycle (~4 years for example)
    
    # Random phase shifts for each periodic term
    phase_1 = np.random.uniform(0, 2 * np.pi)
    phase_2 = np.random.uniform(0, 2 * np.pi)
    
    for col in columns_X:
        # Base value with linear growth over time
        linear_growth = current_values[col] * (1 + growth_trend)  # Apply growth rate

        # Add periodic sinusoidal fluctuation
        # Scale the periodic fluctuation with respect to the initial value of the parameter
        periodic_1 = np.sin(2 * np.pi * (i / period_1) + phase_1) * (initial_values[col] * np.random.uniform(0.02, 0.03))
        periodic_2 = np.sin(2 * np.pi * (i / period_2) + phase_2) * (initial_values[col] * np.random.uniform(0.02, 0.03))

        # Add a small random fluctuation proportional to the initial value
        random_fluctuation = np.random.uniform(-0.005, 0.005) * initial_values[col]

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
df_optimized.to_csv('country_inter_gen.csv', index=False)

# Display the first few rows of the dataframe for verification
print("Displaying Optimized Country Actions and Predictions:")
print(df_optimized.head())