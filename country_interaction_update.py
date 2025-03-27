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

# Define the action columns for the dataframe (only current actions for A and B)
action_columns = [
    'A Major Political Actions', 'A Economic Policy Adjustment', 'A Military Activity', 'A Diplomatic Policy Change',
    'A Social Policy and Welfare Reform', 'A Environmental and Energy Policy', 'A Technology and Innovation Strategy', 'A Public Health and Safety Policy',
    'B Major Political Actions', 'B Economic Policy Adjustment', 'B Military Activity', 'B Diplomatic Policy Change',
    'B Social Policy and Welfare Reform', 'B Environmental and Energy Policy', 'B Technology and Innovation Strategy', 'B Public Health and Safety Policy'
]

# Initialize an empty DataFrame for actions with columns and the appropriate number of rows
data_actions = pd.DataFrame(columns=action_columns, index=range(number_rows))
data_X_optimized = []  # Initialize an empty list for X data (states)

# First row initialization (start with 0 actions for all)
first_row_actions = [0] * len(action_columns)
data_actions.loc[0] = first_row_actions  # Add first row of actions

# Initialize the starting values for each parameter based on realistic data (for example, as of 2025)
# Initialize the starting values for each parameter based on realistic data (with adjustments to increase action probabilities)
# Initialize the starting values for each parameter based on realistic data (with adjustments to increase action probabilities)
initial_values = {
    'A Public Trust': 80.0,  # Increased Public Trust to increase the probability of actions like support
    'A Political Stability': 8.0,  # Increased Political Stability to increase the likelihood of political actions
    'Political Similarity': 0.8,  # Increased political similarity to improve relations with B and make support more likely
    'A Trade Balance': -10*100,  # Decreased Trade Balance (increase trade deficit to increase probability of sanctions)
    'A GDP': 15000,  # Increased A's GDP to make economic aid more likely
    'A Unemployment Rate': 6.0,  # Slightly reduced Unemployment Rate to keep A's economy healthy
    'A Inflation Rate': 3.0, 
    'A Foreign Debt': 300, 
    'A Government Spending': 800,
    'A Military Spending': 150*10, 
    'A Education Spending': 70, 
    'A Health Spending': 120, 
    'A Environment Spending': 30, 
    'A Technology Investment': 250,
    'A Internet Penetration': 70.0, 
    'A Energy Production': 900, 
    'A Energy Consumption': 850, 
    'A Pollution Level': 20, 
    'A Population': 500000000,
    'A Urbanization Rate': 60.0, 
    'A Human Development Index': 0.75, 
    'A Freedom of Press': 60.0, 
    'A Corruption Index': 50.0,
    'A Military Power': 800*10, 
    'A Alliances': 2, 
    'A Environmental Quality': 70.0, 
    'A Natural Resources Availability': 100,
    'A Public Health': 80.0, 
    'A Democracy Index': 6.0, 
    'A Technology Adoption Rate': 0.5, 
    'A Cultural Influence': 40.0, 
    'A Global Trade Index': 0.6,
    
    'B GDP': 12000, 
    'B Unemployment Rate': 8.5,  # Increased B's Unemployment Rate to make aid more likely
    'B Inflation Rate': 2.0, 
    'B Foreign Debt': 400, 
    'B Government Spending': 1000,
    'B Military Spending': 180, 
    'B Education Spending': 90, 
    'B Health Spending': 140, 
    'B Environment Spending': 40, 
    'B Technology Investment': 280,
    'B Internet Penetration': 80.0, 
    'B Energy Production': 1100, 
    'B Energy Consumption': 1000, 
    'B Pollution Level': 18, 
    'B Population': 750000000,
    'B Urbanization Rate': 75.0, 
    'B Political Stability': 8.0, 
    'B Human Development Index': 0.85, 
    'B Public Trust': 70.0, 
    'B Freedom of Press': 80.0,
    'B Corruption Index': 35.0, 
    'B Military Power': 1200, 
    'B Alliances': 4, 
    'B Environmental Quality': 80.0, 
    'B Natural Resources Availability': 110,
    'B Trade Balance': 20, 
    'B Public Health': 90.0, 
    'B Democracy Index': 8.0, 
    'B Technology Adoption Rate': 0.7, 
    'B Cultural Influence': 60.0, 
    'B Global Trade Index': 0.8,
    
    'A to B Imports': 200, 
    'A to B Exports': 150, 
    'B to A Imports': 180, 
    'B to A Exports': 130,
    'A Bond Status': 1, 
    'B Bond Status': 1, 
    'A Sovereignty Disputes': 0, 
    'B Sovereignty Disputes': 0,
    'Ethnic Similarity': 0.5, 
    'Cultural Compatibility': 0.7
}

# Generate state data and actions row by row
current_values = initial_values.copy()

# Initialize the action impact matrix M (the coefficients that define the action effects on the states)
M = np.zeros((len(action_columns), len(columns_X)))  # Number of actions x Number of states

# Example: Set the matrix M for A Major Political Actions
M[action_columns.index('A Major Political Actions')][columns_X.index('A Public Trust')] = 0.1  # A Major Political Actions increases A Public Trust
M[action_columns.index('A Major Political Actions')][columns_X.index('A Political Stability')] = 0.05  # A Major Political Actions increases A Political Stability
M[action_columns.index('A Major Political Actions')][columns_X.index('A Trade Balance')] = 0.03  # A Major Political Actions increases A Trade Balance

# Generate the first row of actions and states
# For each action, calculate its value based on the current state values (from the previous row)
# Generate state data and actions row by row
for i in range(1, number_rows):
    row_actions = [0] * len(action_columns)  # Initialize the row actions to zero for each action
    row_state = []  # Initialize a list for the state values

    # Initialize the temporary impact values for this row (independent impacts for each action)
    action_impacts = np.zeros(len(columns_X))  # This will store the impact of actions on states for this row

    # For each action, calculate its value based on the current state values (from the previous row)
    for j, action in enumerate(action_columns):
        if action == 'A Major Political Actions':  # Public Declaration of Support or Opposition
            a_public_trust = current_values['A Public Trust']
            a_political_stability = current_values['A Political Stability']
            a_unemployment_rate = current_values['A Unemployment Rate']
            a_bilateral_diplomatic_relations_opposition = current_values['A to B Exports'] - current_values['A to B Imports']

            # Calculate A's support action (Public Declaration of Support)
            a_bilateral_diplomatic_relations_support = current_values['Ethnic Similarity']
            support_probability = 0.3 + 0.05 * (a_public_trust - 60) + 0.1 * (a_political_stability - 6.5) + 0.2 * a_bilateral_diplomatic_relations_support
            random_value = np.random.random()

            if random_value < support_probability:
                row_actions[j] += 3  # Action taken (3 indicates action for support)
                # Accumulate the impact on the state parameters
                action_impacts[columns_X.index('A Public Trust')] += 0.1
                action_impacts[columns_X.index('A Political Stability')] += 0.05
                action_impacts[columns_X.index('A Trade Balance')] += 0.03

            # Calculate A's opposition action (A Opposes B)
            opposition_probability = 0.3 + 0.05 * (a_unemployment_rate - 8) - 0.1 * a_bilateral_diplomatic_relations_opposition
            random_value = np.random.random()

            if random_value < opposition_probability:
                row_actions[j] += -4  # Action taken (negative action for opposition)
                # Accumulate the impact on the state parameters
                action_impacts[columns_X.index('A Public Trust')] -= 0.05
                action_impacts[columns_X.index('A Political Stability')] -= 0.02

        elif action == 'A Economic Policy Adjustment':  # Trade Sanctions (Trigger Condition and Formula)
            # Extract parameters for trade sanctions calculation
            a_trade_balance = current_values['A Trade Balance']
            a_unemployment_rate = current_values['A Unemployment Rate']
            a_bilateral_diplomatic_relations = current_values['A to B Exports'] - current_values['A to B Imports']
            a_gdp = current_values['A GDP']
            b_unemployment_rate = current_values['B Unemployment Rate']
            political_similarity = current_values['Political Similarity']

            # Read Political Similarity from current state
            a_political_similarity = current_values['Political Similarity']  # Added Political Similarity

            # Check if the conditions for trade sanctions are met
            if a_trade_balance < -0.05 * current_values['A GDP'] and a_unemployment_rate > 8 and a_political_similarity < 0.5:
                # Calculate the probability of trade sanction
                sanction_probability = 0.3 + 0.05 * (a_unemployment_rate - 8) - 0.02 * a_bilateral_diplomatic_relations
                random_value = np.random.random()

                if random_value < sanction_probability:
                    row_actions[j] += -4  # Negative action for trade sanctions (e.g., -3 indicates trade sanctions)
                    # Apply the impact on states (e.g., a decrease in public trust, economic stability, etc.)
                    action_impacts[columns_X.index('A Public Trust')] -= 0.1
                    action_impacts[columns_X.index('A Political Stability')] -= 0.05
                    action_impacts[columns_X.index('A Trade Balance')] -= 0.05
                    # Apply the impact on states for B
                    action_impacts[columns_X.index('B Public Trust')] -= 0.05
                    action_impacts[columns_X.index('B Political Stability')] -= 0.02
                    action_impacts[columns_X.index('B Trade Balance')] += 0.05

            # Calculate the probability of providing economic aid
            aid_probability = 0.2 + 0.05 * (a_gdp - 10000) - 0.05 * (b_unemployment_rate - 5) + 0.1 * political_similarity
            random_value = np.random.random()

            if random_value < aid_probability:
                row_actions[j] += 5  # Positive action for economic aid (e.g., 3 indicates aid provided)

                # Apply the impact on states for A (Economic aid)
                action_impacts[columns_X.index('A Public Trust')] += 0.05
                action_impacts[columns_X.index('A Political Stability')] += 0.02
                action_impacts[columns_X.index('A Trade Balance')] -= 0.05  # Could worsen A's trade balance if aid is cash flow out

                # Apply the impact on states for B (Economic aid)
                action_impacts[columns_X.index('B Public Trust')] += 0.1
                action_impacts[columns_X.index('B Political Stability')] += 0.03
                action_impacts[columns_X.index('B Trade Balance')] += 0.05

        elif action == 'A Military Activity':  # Displaying military power (new action)
            # Extract parameters for military display calculation
            a_military_power = current_values['A Military Power']
            b_political_stability = current_values['B Political Stability']
            political_similarity = current_values['Political Similarity']
            b_military_power = current_values['B Military Power']
            a_military_spending = current_values['A Military Spending']
            a_political_stability = current_values['A Political Stability']

            # Calculate the probability of A displaying military power
            military_display_probability = 0.3 + 0.05 * (a_military_power - 700) - 0.1 * (b_political_stability - 7) + 0.2 * (1 - political_similarity)
            random_value = np.random.random()

            if random_value < military_display_probability:
                row_actions[j] += -5  # Action taken (3 indicates action for displaying military power)
                
                # Apply the impact on states for A (Military power)
                action_impacts[columns_X.index('A Military Power')] += 0.05  # Increase A's military power
                action_impacts[columns_X.index('A Government Spending')] += 0.05  # Government spending could rise for military display

                # Apply the impact on states for B (Military impact)
                action_impacts[columns_X.index('B Political Stability')] -= 0.05  # Decrease B's political stability due to military show of force

            # Calculate the probability of A conducting a military exercise near B
            military_exercise_probability = 0.3 + 0.1 * (a_military_power - 800) - 0.2 * (b_military_power - 1000) + 0.3 * political_similarity
            random_value = np.random.random()

            if random_value < military_exercise_probability:
                row_actions[j] += -4  # Positive action for military exercise (e.g., 3 indicates exercise near B)
                # Apply the impact on states
                action_impacts[columns_X.index('A Military Power')] += 0.05  # Increase A's military trust
                action_impacts[columns_X.index('B Political Stability')] -= 0.1  # Decrease B's political stability
                action_impacts[columns_X.index('B Military Power')] -= 0.1  # Decrease B's military power (if threatened)

            # Calculate the probability of A engaging in military conflict with B
            military_conflict_probability = 0.2 + 0.1 * (a_military_power - 1000) - 0.2 * (political_similarity) + 0.1 * (a_military_spending - 200)
            random_value = np.random.random()

            if random_value < military_conflict_probability:
                row_actions[j] += -6  # Negative action indicating military conflict (-6 for military conflict)

                # Apply the impact on states for A
                action_impacts[columns_X.index('A Military Power')] += 0.1  # Military power increases due to conflict preparation
                action_impacts[columns_X.index('A Political Stability')] -= 0.1  # Political stability may decrease due to the conflict

                # Apply the impact on states for B
                action_impacts[columns_X.index('B Political Stability')] -= 0.2  # Decrease B's political stability as a result of conflict
                action_impacts[columns_X.index('B Military Power')] -= 0.15  # Decrease B's military power due to conflict engagement


        elif action == 'A Diplomatic Policy Change':  # Peace Agreement (new action)
            # Extract parameters for peace agreement calculation
            a_political_stability = current_values['A Political Stability']
            b_political_stability = current_values['B Political Stability']
            a_military_power = current_values['A Military Power']
            b_military_power = current_values['B Military Power']
            political_similarity = current_values['Political Similarity']

            # Calculate the probability of signing a peace agreement
            peace_probability = 0.4 + 0.1 * (a_political_stability - 6) - 0.05 * (a_military_power - b_military_power) + 0.2 * political_similarity
            random_value = np.random.random()

            if random_value < peace_probability:
                row_actions[j] += 6  # Positive action for peace agreement (e.g., 4 indicates peace agreement signed)
                
                # Apply the impact on states for A (Positive impact due to peace agreement)
                action_impacts[columns_X.index('A Political Stability')] += 0.1  # Increased political stability
                action_impacts[columns_X.index('A Trade Balance')] += 0.05  # Trade balance might improve
                action_impacts[columns_X.index('A Military Spending')] -= 0.05  # Military spending might decrease as a result of peace

                # Apply the impact on states for B (Positive impact due to peace agreement)
                action_impacts[columns_X.index('B Political Stability')] += 0.1  # Increased political stability for B
                action_impacts[columns_X.index('B Trade Balance')] += 0.05  # Trade balance might improve for B
                action_impacts[columns_X.index('B Military Spending')] -= 0.05  # B's military spending might decrease as a result of peace


            # Extract parameters for international sanctions calculation
            a_unemployment_rate = current_values['A Unemployment Rate']
            a_bilateral_diplomatic_relations = current_values['Political Similarity']  # This represents the diplomatic relation between A and B
            a_trade_balance = current_values['A to B Exports'] - current_values['A to B Imports']  # Economic cooperation index

            # Check if the conditions for participating in international sanctions are met
            if a_bilateral_diplomatic_relations < 0.5 and a_unemployment_rate > 8 and a_trade_balance < 0:
                # Calculate the probability of participating in sanctions
                sanction_probability = 0.3 + 0.05 * (a_unemployment_rate - 8) - 0.1 * a_trade_balance - 0.2 * (1 - a_bilateral_diplomatic_relations)
                random_value = np.random.random()

                if random_value < sanction_probability:
                    row_actions[j] += -6  # Negative action indicating participation in sanctions (e.g., -6 indicates sanctions)

                    # Apply the impact on states for A (International sanctions)
                    action_impacts[columns_X.index('A Public Trust')] -= 0.1  # Public trust in A could decrease due to sanctions
                    action_impacts[columns_X.index('A Political Stability')] -= 0.05  # Political stability in A might decrease due to sanctions
                    action_impacts[columns_X.index('A Trade Balance')] -= 0.05  # Trade balance could worsen as a result of sanctions

                    # Apply the impact on states for B (Sanctions impact)
                    action_impacts[columns_X.index('B Public Trust')] -= 0.15  # Public trust in B might decrease due to sanctions
                    action_impacts[columns_X.index('B Political Stability')] -= 0.1  # B's political stability could decrease
                    action_impacts[columns_X.index('B Military Power')] -= 0.1  # B's military power could decrease as a result of sanctions

        elif action == 'A Environmental and Energy Policy':  # A takes environmental policy action with B
            # Extract parameters for the environmental policy action calculation
            a_environment_spending = current_values['A Environment Spending']
            b_environment_spending = current_values['B Environment Spending']
            political_similarity = current_values['Political Similarity']

            # Calculate the probability of A taking environmental policy action with B
            policy_probability = 0.3 + 0.05 * (a_environment_spending - 30) + 0.1 * (b_environment_spending - 40) + 0.15 * (political_similarity - 0.5)
            random_value = np.random.random()

            if random_value < policy_probability:
                row_actions[j] += 4  # Positive action for environmental policy cooperation

                # Apply the impact on states for A (Environmental policy)
                action_impacts[columns_X.index('A Environment Spending')] += 0.05  # Increase A's environmental spending
                action_impacts[columns_X.index('A Environmental Quality')] += 0.1  # Improve A's environmental quality

                # Apply the impact on states for B (Environmental cooperation)
                action_impacts[columns_X.index('B Environment Spending')] += 0.05  # Increase B's environmental spending
                action_impacts[columns_X.index('B Environmental Quality')] += 0.1  # Improve B's environmental quality
            
            # Extract parameters for the energy consumption and collaboration action calculation
            a_energy_consumption = current_values['A Energy Consumption']
            b_energy_production = current_values['B Energy Production']
            political_similarity = current_values['Political Similarity']

            # Calculate the probability of A increasing energy consumption and collaborating with B
            energy_cooperation_probability = 0.3 + 0.05 * (a_energy_consumption - 850) + 0.1 * (b_energy_production - 1000) + 0.2 * (political_similarity - 0.5)
            random_value = np.random.random()

            if random_value < energy_cooperation_probability:
                row_actions[j] += 2  # Positive action for increasing energy consumption and collaborating with B

                # Apply the impact on states for A (Energy consumption)
                action_impacts[columns_X.index('A Energy Consumption')] += 0.05  # Increase A's energy consumption
                action_impacts[columns_X.index('A Energy Production')] += 0.02  # A might increase its energy production to support the consumption increase

                # Apply the impact on states for B (Energy cooperation)
                action_impacts[columns_X.index('B Energy Consumption')] += 0.03  # B's energy consumption might rise due to cooperation
                action_impacts[columns_X.index('B Energy Production')] += 0.05  # B may increase energy production as part of cooperation

            # Extract parameters for the environmental restriction action calculation
            a_energy_consumption = current_values['A Energy Consumption']
            a_to_b_exports = current_values['A to B Exports']
            a_environment_spending = current_values['A Environment Spending']

            # Calculate the probability of A implementing environmental measures and restricting energy exports to B
            environmental_restriction_probability = 0.3 + 0.05 * (a_energy_consumption - 850) - 0.1 * (a_to_b_exports - 150) + 0.2 * (a_environment_spending - 30)
            random_value = np.random.random()

            if random_value < environmental_restriction_probability:
                row_actions[j] += -4  # Negative action for restricting energy exports to B (e.g., -4 indicates restriction)

                # Apply the impact on states for A (Energy policy)
                action_impacts[columns_X.index('A Energy Consumption')] -= 0.05  # A may reduce energy consumption as part of the restriction
                action_impacts[columns_X.index('A Environmental Quality')] += 0.1  # A's environmental quality could improve with the policy

                # Apply the impact on states for B (Energy exports restriction)
                action_impacts[columns_X.index('B Energy Consumption')] -= 0.05  # B's energy consumption might decrease due to the restriction
                action_impacts[columns_X.index('B Trade Balance')] -= 0.03  # B's trade balance could worsen due to restricted energy imports

        elif action == 'A Technology and Innovation Strategy':  # A Shares Technology with B
            # Extract parameters for technology sharing calculation
            a_technology_investment = current_values['A Technology Investment']
            a_innovation_index = current_values['A Innovation Index']
            political_similarity = current_values['Political Similarity']  # Political cooperation between A and B
            
            # Calculate the probability of sharing technology with B
            tech_sharing_probability = 0.3 + 0.05 * (a_technology_investment - 250) + 0.1 * (a_innovation_index - 50) + 0.2 * political_similarity
            random_value = np.random.random()

            if random_value < tech_sharing_probability:
                row_actions[j] += 4  # Positive action (3 indicates technology sharing with B)
                
                # Apply the impact on states for A (Technology Sharing)
                action_impacts[columns_X.index('A Technology Investment')] += 0.05  # Technology investment might increase due to shared knowledge
                action_impacts[columns_X.index('A Innovation Index')] += 0.05  # Innovation index might rise as a result of sharing

                # Apply the impact on states for B (Technology Sharing)
                action_impacts[columns_X.index('B Technology Adoption Rate')] += 0.05  # B's technology adoption might increase
                action_impacts[columns_X.index('B Technology Investment')] += 0.03  # B's technology investment might rise due to shared knowledge

            # Extract parameters for technology competition calculation
            a_technology_investment = current_values['A Technology Investment']
            a_innovation_index = current_values['A Innovation Index']
            b_technology_investment = current_values['B Technology Investment']  # B's technology investment
            
            # Calculate the probability of A competing with B in the technology field
            tech_competition_probability = 0.4 + 0.05 * (a_technology_investment - 250) + 0.1 * (a_innovation_index - 50) - 0.15 * (b_technology_investment - 280)
            random_value = np.random.random()

            if random_value < tech_competition_probability:
                row_actions[j] += -4  # Negative action (indicates competition, -4 represents A's active competition with B in technology)
                
                # Apply the impact on states for A (Competition)
                action_impacts[columns_X.index('A Technology Investment')] += 0.05  # A's technology investment might increase as a result of competition
                action_impacts[columns_X.index('A Innovation Index')] += 0.05  # Innovation index might rise as a result of competition
                action_impacts[columns_X.index('A Military Spending')] += 0.03  # Competition may drive more military spending as a countermeasure

                # Apply the impact on states for B (Competition)
                action_impacts[columns_X.index('B Technology Investment')] -= 0.05  # B's technology investment might decline due to increased competition
                action_impacts[columns_X.index('B Innovation Index')] -= 0.05  # B's innovation index might be impacted

            # Extract parameters for technology export restriction calculation
            a_technology_investment = current_values['A Technology Investment']
            b_technology_investment = current_values['B Technology Investment']
            a_political_stability = current_values['A Political Stability']

            # Calculate the probability of A restricting technology exports to B
            tech_export_restriction_probability = 0.3 + 0.1 * (a_technology_investment - 300) - 0.1 * (b_technology_investment - 280) - 0.2 * (a_political_stability - 6.5)
            random_value = np.random.random()

            if random_value < tech_export_restriction_probability:
                row_actions[j] += -5  # Negative action (-5 indicates action for restricting exports)

                # Apply the impact on states for A (Restricting exports)
                action_impacts[columns_X.index('A Technology Investment')] -= 0.1  # A's technology investment might be impacted by restrictions
                action_impacts[columns_X.index('A Government Spending')] += 0.05  # Possible increase in government spending to maintain control

                # Apply the impact on states for B (Restrictions)
                action_impacts[columns_X.index('B Technology Investment')] -= 0.1  # B's technology investment might decrease due to lack of access to A's technology
                action_impacts[columns_X.index('B Innovation Index')] -= 0.05  # B's innovation index could be impacted by technology restrictions

        else:
            row_actions[j] += 0  # Default to 0 if the action isn't defined yet

    # Apply the action impacts to the state values (i.e., update the state values with the impact of the actions)
    for col in columns_X:
        # Apply random fluctuation to the state value
        change = np.random.uniform(-2, 2)
        new_value = current_values[col] * (1 + change / 100) if 'Rate' in col or 'Index' in col else current_values[col] + change

        # Apply the accumulated action impact to the state value
        action_effect = action_impacts[columns_X.index(col)]
        new_value += action_effect  # Add the impact of actions on the state parameter

        current_values[col] = new_value  # Update the current value
        row_state.append(round(new_value, 2))  # Append the updated state value to the row state

    # Assign the row actions directly to the DataFrame
    data_actions.loc[i] = row_actions
    data_X_optimized.append(row_state)  # Append the row state data

# Convert the list of rows into a DataFrame
df_X_optimized = pd.DataFrame(data_X_optimized, columns=columns_X)

# Combine all the data
df_optimized = pd.concat([df_X_optimized, data_actions], axis=1)

# Save the data to a CSV file for further analysis
df_optimized.to_csv('country_inter_gen.csv', index=False)

# Display the first few rows of the dataframe for verification
print("Displaying Optimized Country Actions and Predictions:")
print(df_optimized.head())
