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
    'A Cultural Influence', 'A Global Trade Index', 'A Innovation Index', 'A Social Welfare Spending', 'A Social Security Reform','A Social Welfare',

    # B state parameters
    'B GDP', 'B Unemployment Rate', 'B Inflation Rate', 'B Foreign Debt',
    'B Government Spending', 'B Military Spending', 'B Education Spending',
    'B Health Spending', 'B Environment Spending', 'B Technology Investment',
    'B Internet Penetration', 'B Energy Production', 'B Energy Consumption',
    'B Pollution Level', 'B Population', 'B Urbanization Rate', 'B Political Stability',
    'B Human Development Index', 'B Public Trust', 'B Freedom of Press', 'B Corruption Index',
    'B Military Power', 'B Alliances', 'B Environmental Quality', 'B Natural Resources Availability',
    'B Trade Balance', 'B Public Health', 'B Democracy Index', 'B Technology Adoption Rate',
    'B Cultural Influence', 'B Global Trade Index', 'B Innovation Index', 'B Social Welfare Spending', 'B Social Security Reform', 'B Social Welfare',

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

# Define a function to handle political actions
def major_political_actions(initiator, target, current_values, action_columns, row_actions, action_impacts):
    # Define the action column name dynamically based on initiator
    action_column = f'{initiator} Major Political Actions'

    # Check if the action column exists in action_columns
    if action_column not in action_columns:
        raise ValueError(f"Column '{action_column}' not found in action_columns!")

    # Define state parameter keys for initiator and target
    initiator_public_trust = f'{initiator} Public Trust'
    initiator_political_stability = f'{initiator} Political Stability'
    initiator_unemployment_rate = f'{initiator} Unemployment Rate'
    initiator_to_target_exports = f'{initiator} to {target} Exports'
    initiator_to_target_imports = f'{initiator} to {target} Imports'
    target_public_trust = f'{target} Public Trust'
    target_political_stability = f'{target} Political Stability'
    
    # Calculate support action (Public Declaration of Support)
    initiator_public_trust_value = current_values[initiator_public_trust]
    initiator_political_stability_value = current_values[initiator_political_stability]
    initiator_unemployment_rate_value = current_values[initiator_unemployment_rate]
    initiator_bilateral_diplomatic_relations_opposition = current_values[initiator_to_target_exports] - current_values[initiator_to_target_imports]
    initiator_bilateral_diplomatic_relations_support = current_values['Ethnic Similarity']
    
    support_probability = 0.3 + 0.05 * (initiator_public_trust_value - 60) + 0.1 * (initiator_political_stability_value - 6.5) + 0.2 * initiator_bilateral_diplomatic_relations_support
    random_value = np.random.random()

    if random_value < support_probability:
        # Find the correct index of the action column dynamically
        action_index = action_columns.index(action_column)
        row_actions[action_index] = 3  # Positive action for support
        # Accumulate the impact on the state parameters
        action_impacts[columns_X.index(initiator_public_trust)] += 0.1
        action_impacts[columns_X.index(initiator_political_stability)] += 0.05
        action_impacts[columns_X.index(f'{initiator} Trade Balance')] += 0.03

    # Calculate opposition action (A Opposes B)
    opposition_probability = 0.3 + 0.05 * (initiator_unemployment_rate_value - 8) - 0.1 * initiator_bilateral_diplomatic_relations_opposition
    random_value = np.random.random()

    if random_value < opposition_probability:
        # Negative action for opposition
        action_index = action_columns.index(action_column)
        row_actions[action_index] = -4
        # Accumulate the impact on the state parameters
        action_impacts[columns_X.index(initiator_public_trust)] -= 0.05
        action_impacts[columns_X.index(initiator_political_stability)] -= 0.02

    return row_actions, action_impacts

def economic_policy_adjustment(initiator, target, current_values, action_columns, row_actions, action_impacts):
    # Define the action column name dynamically based on initiator
    action_column = f'{initiator} Economic Policy Adjustment'

    # Check if the action column exists in action_columns
    if action_column not in action_columns:
        raise ValueError(f"Column '{action_column}' not found in action_columns!")

    # Define state parameter keys for initiator and target
    initiator_trade_balance = f'{initiator} Trade Balance'
    initiator_unemployment_rate = f'{initiator} Unemployment Rate'
    initiator_to_target_exports = f'{initiator} to {target} Exports'
    initiator_to_target_imports = f'{initiator} to {target} Imports'
    initiator_gdp = f'{initiator} GDP'
    target_unemployment_rate = f'{target} Unemployment Rate'
    political_similarity = 'Political Similarity'

    # Extract relevant state values for economic sanctions and aid
    initiator_trade_balance_value = current_values[initiator_trade_balance]
    initiator_unemployment_rate_value = current_values[initiator_unemployment_rate]
    initiator_bilateral_diplomatic_relations = current_values[initiator_to_target_exports] - current_values[initiator_to_target_imports]
    initiator_gdp_value = current_values[initiator_gdp]
    target_unemployment_rate_value = current_values[target_unemployment_rate]
    initiator_political_similarity = current_values[political_similarity]

    # Trade sanctions condition
    if initiator_trade_balance_value < -0.05 * initiator_gdp_value and initiator_unemployment_rate_value > 8 and initiator_political_similarity < 0.5:
        sanction_probability = 0.3 + 0.05 * (initiator_unemployment_rate_value - 8) - 0.02 * initiator_bilateral_diplomatic_relations
        random_value = np.random.random()

        if random_value < sanction_probability:
            # Find the correct index of the action column dynamically
            action_index = action_columns.index(action_column)
            row_actions[action_index] = -4  # Negative action for trade sanctions
            # Apply the impact on states (e.g., a decrease in public trust, economic stability, etc.)
            action_impacts[columns_X.index(f'{initiator} Public Trust')] -= 0.1
            action_impacts[columns_X.index(f'{initiator} Political Stability')] -= 0.05
            action_impacts[columns_X.index(initiator_trade_balance)] -= 0.05
            # Apply the impact on states for B
            action_impacts[columns_X.index(f'{target} Public Trust')] -= 0.05
            action_impacts[columns_X.index(f'{target} Political Stability')] -= 0.02
            action_impacts[columns_X.index(f'{target} Trade Balance')] += 0.05

    # Economic aid condition
    aid_probability = 0.2 + 0.05 * (initiator_gdp_value - 10000) - 0.05 * (target_unemployment_rate_value - 5) + 0.1 * initiator_political_similarity
    random_value = np.random.random()

    if random_value < aid_probability:
        action_index = action_columns.index(action_column)
        row_actions[action_index] = 5  # Positive action for economic aid
        # Apply the impact on states for initiator (A)
        action_impacts[columns_X.index(f'{initiator} Public Trust')] += 0.05
        action_impacts[columns_X.index(f'{initiator} Political Stability')] += 0.02
        action_impacts[columns_X.index(initiator_trade_balance)] -= 0.05  # Could worsen initiator's trade balance if aid is cash flow out

        # Apply the impact on states for target (B)
        action_impacts[columns_X.index(f'{target} Public Trust')] += 0.1
        action_impacts[columns_X.index(f'{target} Political Stability')] += 0.03
        action_impacts[columns_X.index(f'{target} Trade Balance')] += 0.05

    return row_actions, action_impacts

def military_activity(initiator, target, current_values, action_columns, row_actions, action_impacts):
    # Define the action column name dynamically based on initiator
    action_column = f'{initiator} Military Activity'

    # Check if the action column exists in action_columns
    if action_column not in action_columns:
        raise ValueError(f"Column '{action_column}' not found in action_columns!")

    # Define state parameter keys for initiator and target
    initiator_military_power = f'{initiator} Military Power'
    target_political_stability = f'{target} Political Stability'
    political_similarity = 'Political Similarity'
    target_military_power = f'{target} Military Power'
    initiator_military_spending = f'{initiator} Military Spending'
    initiator_political_stability = f'{initiator} Political Stability'

    # Extract relevant state values for military actions
    initiator_military_power_value = current_values[initiator_military_power]
    target_political_stability_value = current_values[target_political_stability]
    political_similarity_value = current_values[political_similarity]
    target_military_power_value = current_values[target_military_power]
    initiator_military_spending_value = current_values[initiator_military_spending]
    initiator_political_stability_value = current_values[initiator_political_stability]

    # Military display (probability of displaying military power)
    military_display_probability = 0.3 + 0.05 * (initiator_military_power_value - 700) - 0.1 * (target_political_stability_value - 7) + 0.2 * (1 - political_similarity_value)
    random_value = np.random.random()

    if random_value < military_display_probability:
        # Find the correct index of the action column dynamically
        action_index = action_columns.index(action_column)
        row_actions[action_index] = -5  # Action taken (negative value indicates displaying military power)
        
        # Apply the impact on states for A
        action_impacts[columns_X.index(initiator_military_power)] += 0.05  # Increase A's military power
        action_impacts[columns_X.index(f'{initiator} Government Spending')] += 0.05  # Increase A's government spending due to military display

        # Apply the impact on states for B
        action_impacts[columns_X.index(target_political_stability)] -= 0.05  # Decrease B's political stability due to military show of force

    # Military exercise (probability of conducting a military exercise near B)
    military_exercise_probability = 0.3 + 0.1 * (initiator_military_power_value - 800) - 0.2 * (target_military_power_value - 1000) + 0.3 * political_similarity_value
    random_value = np.random.random()

    if random_value < military_exercise_probability:
        action_index = action_columns.index(action_column)
        row_actions[action_index] = -4  # Action taken for military exercise near B (negative value indicates exercise)

        # Apply the impact on states for A
        action_impacts[columns_X.index(initiator_military_power)] += 0.05  # Increase A's military trust
        action_impacts[columns_X.index(target_political_stability)] -= 0.1  # Decrease B's political stability
        action_impacts[columns_X.index(target_military_power)] -= 0.1  # Decrease B's military power due to military exercise

    # Military conflict (probability of engaging in a military conflict with B)
    military_conflict_probability = 0.2 + 0.1 * (initiator_military_power_value - 1000) - 0.2 * (political_similarity_value) + 0.1 * (initiator_military_spending_value - 200)
    random_value = np.random.random()

    if random_value < military_conflict_probability:
        action_index = action_columns.index(action_column)
        row_actions[action_index] = -6  # Action taken for military conflict (negative value indicates conflict)

        # Apply the impact on states for A
        action_impacts[columns_X.index(initiator_military_power)] += 0.1  # Increase A's military power due to conflict preparation
        action_impacts[columns_X.index(initiator_political_stability)] -= 0.1  # Decrease A's political stability due to the conflict

        # Apply the impact on states for B
        action_impacts[columns_X.index(target_political_stability)] -= 0.2  # Decrease B's political stability as a result of conflict
        action_impacts[columns_X.index(target_military_power)] -= 0.15  # Decrease B's military power due to conflict engagement

    return row_actions, action_impacts

def diplomatic_policy_change(initiator, target, current_values, action_columns, row_actions, action_impacts):
    # Define the action column name dynamically based on initiator
    action_column = f'{initiator} Diplomatic Policy Change'

    # Check if the action column exists in action_columns
    if action_column not in action_columns:
        raise ValueError(f"Column '{action_column}' not found in action_columns!")

    # Extract relevant state parameters for the initiator and target
    initiator_political_stability = f'{initiator} Political Stability'
    target_political_stability = f'{target} Political Stability'
    initiator_military_power = f'{initiator} Military Power'
    target_military_power = f'{target} Military Power'
    political_similarity = 'Political Similarity'

    # Extract relevant state values
    initiator_political_stability_value = current_values[initiator_political_stability]
    target_political_stability_value = current_values[target_political_stability]
    initiator_military_power_value = current_values[initiator_military_power]
    target_military_power_value = current_values[target_military_power]
    political_similarity_value = current_values[political_similarity]

    # Calculate the probability of signing a peace agreement
    peace_probability = 0.4 + 0.1 * (initiator_political_stability_value - 6) - 0.05 * (initiator_military_power_value - target_military_power_value) + 0.2 * political_similarity_value
    random_value = np.random.random()

    if random_value < peace_probability:
        # Find the correct index of the action column dynamically
        action_index = action_columns.index(action_column)
        row_actions[action_index] = 6  # Positive action for peace agreement
        
        # Apply the impact on states for A (Positive impact due to peace agreement)
        action_impacts[columns_X.index(initiator_political_stability)] += 0.1  # Increased political stability
        action_impacts[columns_X.index(f'{initiator} Trade Balance')] += 0.05  # Trade balance might improve
        action_impacts[columns_X.index(f'{initiator} Military Spending')] -= 0.05  # Military spending might decrease as a result of peace

        # Apply the impact on states for B (Positive impact due to peace agreement)
        action_impacts[columns_X.index(target_political_stability)] += 0.1  # Increased political stability for B
        action_impacts[columns_X.index(f'{target} Trade Balance')] += 0.05  # Trade balance might improve for B
        action_impacts[columns_X.index(f'{target} Military Spending')] -= 0.05  # B's military spending might decrease as a result of peace

    # Calculate the probability of participating in international sanctions
    a_unemployment_rate = current_values[f'{initiator} Unemployment Rate']
    a_bilateral_diplomatic_relations = current_values[political_similarity]  # This represents the diplomatic relation between A and B
    a_trade_balance = current_values[f'{initiator} to {target} Exports'] - current_values[f'{initiator} to {target} Imports']  # Economic cooperation index

    sanction_probability = 0.3 + 0.05 * (a_unemployment_rate - 8) - 0.1 * a_trade_balance - 0.2 * (1 - a_bilateral_diplomatic_relations)
    random_value = np.random.random()

    if random_value < sanction_probability:
        action_index = action_columns.index(action_column)
        row_actions[action_index] = -6  # Negative action indicating participation in sanctions

        # Apply the impact on states for A (International sanctions)
        action_impacts[columns_X.index(f'{initiator} Public Trust')] -= 0.1  # Public trust in A could decrease due to sanctions
        action_impacts[columns_X.index(f'{initiator} Political Stability')] -= 0.05  # Political stability in A might decrease due to sanctions
        action_impacts[columns_X.index(f'{initiator} Trade Balance')] -= 0.05  # Trade balance could worsen as a result of sanctions

        # Apply the impact on states for B (Sanctions impact)
        action_impacts[columns_X.index(f'{target} Public Trust')] -= 0.15  # Public trust in B might decrease due to sanctions
        action_impacts[columns_X.index(f'{target} Political Stability')] -= 0.1  # B's political stability could decrease
        action_impacts[columns_X.index(f'{target} Military Power')] -= 0.1  # B's military power could decrease as a result of sanctions

    return row_actions, action_impacts

def social_policy_and_welfare_reform(initiator, target, current_values, action_columns, row_actions, action_impacts):
    # Define the action column name dynamically based on initiator
    action_column = f'{initiator} Social Policy and Welfare Reform'

    # Check if the action column exists in action_columns
    if action_column not in action_columns:
        raise ValueError(f"Column '{action_column}' not found in action_columns!")

    # Extract relevant state parameters for the initiator and target
    initiator_social_welfare_spending = f'{initiator} Social Welfare Spending'
    initiator_social_security_reform = f'{initiator} Social Security Reform'
    target_social_welfare = f'{target} Social Welfare'
    political_similarity = 'Political Similarity'

    # Extract relevant state values
    initiator_social_welfare_spending_value = current_values[initiator_social_welfare_spending]
    initiator_social_security_reform_value = current_values[initiator_social_security_reform]
    target_social_welfare_value = current_values[target_social_welfare]
    political_similarity_value = current_values[political_similarity]

    # Calculate the probability of implementing social welfare reform
    social_policy_probability = 0.3 + 0.05 * (initiator_social_welfare_spending_value - 100) + 0.1 * (initiator_social_security_reform_value - 50) + 0.2 * political_similarity_value - 0.1 * target_social_welfare_value
    random_value = np.random.random()

    if random_value < social_policy_probability:
        # Find the correct index of the action column dynamically
        action_index = action_columns.index(action_column)
        row_actions[action_index] = 3  # Positive action for social policy and welfare reform
        
        # Apply the impact on states for A (Social policy)
        action_impacts[columns_X.index(initiator_social_welfare_spending)] += 0.1  # A's social welfare spending increases
        action_impacts[columns_X.index(initiator_social_security_reform)] += 0.05  # A's social security reform improves
        action_impacts[columns_X.index(f'{initiator} Public Trust')] += 0.05  # A's public trust might increase due to the welfare reform

        # Apply the impact on states for B (Benefiting from A's social reform)
        action_impacts[columns_X.index(target_social_welfare)] += 0.1  # B's social welfare improves from cooperation
        action_impacts[columns_X.index(f'{target} Political Stability')] += 0.03  # B's political stability improves as a result of the welfare cooperation

    # Calculate the probability of not implementing the welfare reform (negation)
    social_reform_negation_probability = 0.2 + 0.05 * (initiator_social_welfare_spending_value - 100) - 0.1 * target_social_welfare_value
    random_value = np.random.random()

    if random_value < social_reform_negation_probability:
        # Negative action for failing to reform or withdrawing support
        action_index = action_columns.index(action_column)
        row_actions[action_index] = -3  # Negative action for withdrawing support
        
        # Apply the impact on states for A (Negative impact)
        action_impacts[columns_X.index(initiator_social_welfare_spending)] -= 0.1  # A's social welfare spending decreases
        action_impacts[columns_X.index(f'{initiator} Public Trust')] -= 0.05  # A's public trust might decrease due to the failure

        # Apply the impact on states for B (Negative impact)
        action_impacts[columns_X.index(target_social_welfare)] -= 0.1  # B's social welfare decreases due to the lack of cooperation
        action_impacts[columns_X.index(f'{target} Political Stability')] -= 0.05  # B's political stability decreases due to the broken cooperation

    # Calculate the probability of reducing social welfare support (if unemployment rate is high)
    a_unemployment_rate = current_values[f'{initiator} Unemployment Rate']

    if a_unemployment_rate > 8 and political_similarity_value < 0.5:
        # Calculate the probability of reducing social welfare support
        welfare_reduction_probability = 0.4 + 0.05 * (a_unemployment_rate - 8) - 0.2 * political_similarity_value
        random_value = np.random.random()

        if random_value < welfare_reduction_probability:
            action_index = action_columns.index(action_column)
            row_actions[action_index] = -3  # Negative action for reducing social welfare (e.g., -3 indicates reduction)
            
            # Apply the impact on states for A (Social Welfare Reduction)
            action_impacts[columns_X.index(f'{initiator} Public Trust')] -= 0.1  # A's public trust could decrease due to social welfare cuts
            action_impacts[columns_X.index(f'{initiator} Political Stability')] -= 0.05  # A's political stability might decrease due to dissatisfaction
            action_impacts[columns_X.index(f'{initiator} Trade Balance')] -= 0.03  # A's trade balance might worsen due to reduced cooperation with B
            
            # Apply the impact on states for B (Reduction in cooperation)
            action_impacts[columns_X.index(f'{target} Public Trust')] -= 0.1  # B's public trust decreases due to the reduction in social welfare
            action_impacts[columns_X.index(f'{target} Political Stability')] -= 0.05  # B's political stability might decrease due to reduced cooperation
            action_impacts[columns_X.index(f'{target} Trade Balance')] -= 0.05  # B's trade balance might worsen due to A's reduced support

    return row_actions, action_impacts

def environmental_and_energy_policy(initiator, target, current_values, action_columns, row_actions, action_impacts):
    # Define the action column name dynamically based on initiator
    action_column = f'{initiator} Environmental and Energy Policy'

    # Check if the action column exists in action_columns
    if action_column not in action_columns:
        raise ValueError(f"Column '{action_column}' not found in action_columns!")

    # Extract relevant state parameters for the initiator and target
    initiator_environment_spending = f'{initiator} Environment Spending'
    target_environment_spending = f'{target} Environment Spending'
    political_similarity = 'Political Similarity'

    # Extract relevant state values
    initiator_environment_spending_value = current_values[initiator_environment_spending]
    target_environment_spending_value = current_values[target_environment_spending]
    political_similarity_value = current_values[political_similarity]

    # Calculate the probability of A taking environmental policy action with B
    policy_probability = 0.3 + 0.05 * (initiator_environment_spending_value - 30) + 0.1 * (target_environment_spending_value - 40) + 0.15 * (political_similarity_value - 0.5)
    random_value = np.random.random()

    if random_value < policy_probability:
        # Find the correct index of the action column dynamically
        action_index = action_columns.index(action_column)
        row_actions[action_index] = 4  # Positive action for environmental policy cooperation

        # Apply the impact on states for A (Environmental policy)
        action_impacts[columns_X.index(f'{initiator} Environment Spending')] += 0.05  # Increase A's environmental spending
        action_impacts[columns_X.index(f'{initiator} Environmental Quality')] += 0.1  # Improve A's environmental quality

        # Apply the impact on states for B (Environmental cooperation)
        action_impacts[columns_X.index(f'{target} Environment Spending')] += 0.05  # Increase B's environmental spending
        action_impacts[columns_X.index(f'{target} Environmental Quality')] += 0.1  # Improve B's environmental quality

    # Extract parameters for energy consumption and collaboration action calculation
    initiator_energy_consumption = f'{initiator} Energy Consumption'
    target_energy_production = f'{target} Energy Production'

    # Calculate the probability of A increasing energy consumption and collaborating with B
    energy_cooperation_probability = 0.3 + 0.05 * (current_values[initiator_energy_consumption] - 850) + 0.1 * (current_values[target_energy_production] - 1000) + 0.2 * (political_similarity_value - 0.5)
    random_value = np.random.random()

    if random_value < energy_cooperation_probability:
        # Positive action for increasing energy consumption and collaborating with B
        action_index = action_columns.index(action_column)
        row_actions[action_index] = 2

        # Apply the impact on states for A (Energy consumption)
        action_impacts[columns_X.index(f'{initiator} Energy Consumption')] += 0.05  # Increase A's energy consumption
        action_impacts[columns_X.index(f'{initiator} Energy Production')] += 0.02  # A might increase its energy production to support the consumption increase

        # Apply the impact on states for B (Energy cooperation)
        action_impacts[columns_X.index(f'{target} Energy Consumption')] += 0.03  # B's energy consumption might rise due to cooperation
        action_impacts[columns_X.index(f'{target} Energy Production')] += 0.05  # B may increase energy production as part of cooperation

    # Extract parameters for the environmental restriction action calculation
    initiator_to_target_exports = f'{initiator} to {target} Exports'

    # Calculate the probability of A implementing environmental measures and restricting energy exports to B
    environmental_restriction_probability = 0.3 + 0.05 * (current_values[initiator_energy_consumption] - 850) - 0.1 * (current_values[initiator_to_target_exports] - 150) + 0.2 * (current_values[initiator_environment_spending] - 30)
    random_value = np.random.random()

    if random_value < environmental_restriction_probability:
        # Negative action for restricting energy exports to B
        action_index = action_columns.index(action_column)
        row_actions[action_index] = -4  # Indicating restriction

        # Apply the impact on states for A (Energy policy)
        action_impacts[columns_X.index(f'{initiator} Energy Consumption')] -= 0.05  # A may reduce energy consumption as part of the restriction
        action_impacts[columns_X.index(f'{initiator} Environmental Quality')] += 0.1  # A's environmental quality could improve with the policy

        # Apply the impact on states for B (Energy exports restriction)
        action_impacts[columns_X.index(f'{target} Energy Consumption')] -= 0.05  # B's energy consumption might decrease due to the restriction
        action_impacts[columns_X.index(f'{target} Trade Balance')] -= 0.03  # B's trade balance could worsen due to restricted energy imports

    return row_actions, action_impacts

def technology_and_innovation_strategy(initiator, target, current_values, action_columns, row_actions, action_impacts):
    # Define the action column name dynamically based on initiator
    action_column = f'{initiator} Technology and Innovation Strategy'

    # Check if the action column exists in action_columns
    if action_column not in action_columns:
        raise ValueError(f"Column '{action_column}' not found in action_columns!")

    # Extract relevant state parameters for the initiator and target
    initiator_technology_investment = f'{initiator} Technology Investment'
    initiator_innovation_index = f'{initiator} Innovation Index'
    target_technology_investment = f'{target} Technology Investment'

    # Extract relevant state values
    initiator_technology_investment_value = current_values[initiator_technology_investment]
    initiator_innovation_index_value = current_values[initiator_innovation_index]
    political_similarity_value = current_values['Political Similarity']
    target_technology_investment_value = current_values[target_technology_investment]

    # Calculate the probability of sharing technology with B
    tech_sharing_probability = 0.3 + 0.05 * (initiator_technology_investment_value - 250) + 0.1 * (initiator_innovation_index_value - 50) + 0.2 * political_similarity_value
    random_value = np.random.random()

    if random_value < tech_sharing_probability:
        # Find the correct index of the action column dynamically
        action_index = action_columns.index(action_column)
        row_actions[action_index] = 4  # Positive action for technology sharing
        # Apply the impact on states for A (Technology Sharing)
        action_impacts[columns_X.index(initiator_technology_investment)] += 0.05  # Technology investment might increase due to shared knowledge
        action_impacts[columns_X.index(initiator_innovation_index)] += 0.05  # Innovation index might rise as a result of sharing

        # Apply the impact on states for B (Technology Sharing)
        action_impacts[columns_X.index(f'{target} Technology Adoption Rate')] += 0.05  # B's technology adoption might increase
        action_impacts[columns_X.index(f'{target} Technology Investment')] += 0.03  # B's technology investment might rise due to shared knowledge

    # Calculate the probability of A competing with B in the technology field
    tech_competition_probability = 0.4 + 0.05 * (initiator_technology_investment_value - 250) + 0.1 * (initiator_innovation_index_value - 50) - 0.15 * (target_technology_investment_value - 280)
    random_value = np.random.random()

    if random_value < tech_competition_probability:
        # Negative action indicating competition (e.g., -4 represents A's active competition with B in technology)
        action_index = action_columns.index(action_column)
        row_actions[action_index] = -4
        # Apply the impact on states for A (Competition)
        action_impacts[columns_X.index(initiator_technology_investment)] += 0.05  # A's technology investment might increase as a result of competition
        action_impacts[columns_X.index(initiator_innovation_index)] += 0.05  # Innovation index might rise as a result of competition
        action_impacts[columns_X.index(f'{initiator} Military Spending')] += 0.03  # Competition may drive more military spending as a countermeasure

        # Apply the impact on states for B (Competition)
        action_impacts[columns_X.index(f'{target} Technology Investment')] -= 0.05  # B's technology investment might decline due to increased competition
        action_impacts[columns_X.index(f'{target} Innovation Index')] -= 0.05  # B's innovation index might be impacted

    # Calculate the probability of A restricting technology exports to B
    tech_export_restriction_probability = 0.3 + 0.1 * (initiator_technology_investment_value - 300) - 0.1 * (target_technology_investment_value - 280) - 0.2 * (current_values[f'{initiator} Political Stability'] - 6.5)
    random_value = np.random.random()

    if random_value < tech_export_restriction_probability:
        # Negative action for restricting exports
        action_index = action_columns.index(action_column)
        row_actions[action_index] = -5
        # Apply the impact on states for A (Restricting exports)
        action_impacts[columns_X.index(initiator_technology_investment)] -= 0.1  # A's technology investment might be impacted by restrictions
        action_impacts[columns_X.index(f'{initiator} Government Spending')] += 0.05  # Possible increase in government spending to maintain control

        # Apply the impact on states for B (Restrictions)
        action_impacts[columns_X.index(f'{target} Technology Investment')] -= 0.1  # B's technology investment might decrease due to lack of access to A's technology
        action_impacts[columns_X.index(f'{target} Innovation Index')] -= 0.05  # B's innovation index could be impacted by technology restrictions

    return row_actions, action_impacts

def public_health_and_safety_policy(initiator, target, current_values, action_columns, row_actions, action_impacts):
    # Define the action column name dynamically based on initiator
    action_column = f'{initiator} Public Health and Safety Policy'

    # Check if the action column exists in action_columns
    if action_column not in action_columns:
        raise ValueError(f"Column '{action_column}' not found in action_columns!")

    # Extract relevant state parameters for the initiator and target
    initiator_public_health = f'{initiator} Public Health'
    target_public_health = f'{target} Public Health'
    political_similarity = 'Political Similarity'

    # Extract relevant state values
    initiator_public_health_value = current_values[initiator_public_health]
    target_public_health_value = current_values[target_public_health]
    political_similarity_value = current_values[political_similarity]

    # Calculate the probability of providing public health support to B
    health_support_probability = 0.3 + 0.1 * (initiator_public_health_value - 70) - 0.1 * (target_public_health_value - 60) + 0.2 * political_similarity_value
    random_value = np.random.random()

    if random_value < health_support_probability:
        # Find the correct index of the action column dynamically
        action_index = action_columns.index(action_column)
        row_actions[action_index] = 3  # Positive action for support
        
        # Accumulate the impact on the state parameters
        action_impacts[columns_X.index(f'{initiator} Public Trust')] += 0.05
        action_impacts[columns_X.index(f'{initiator} Political Stability')] += 0.03
        action_impacts[columns_X.index(f'{target} Public Health')] += 0.1
        action_impacts[columns_X.index(f'{target} Political Stability')] += 0.02

    # Calculate the probability of restricting medical supplies to B
    supply_restriction_probability = 0.3 + 0.05 * (initiator_public_health_value - 70) - 0.1 * (target_public_health_value - 60) - 0.2 * political_similarity_value
    random_value = np.random.random()

    if random_value < supply_restriction_probability:
        # Negative action for restricting medical supplies
        action_index = action_columns.index(action_column)
        row_actions[action_index] = -3
        
        # Accumulate the impact on the state parameters
        action_impacts[columns_X.index(f'{initiator} Public Trust')] -= 0.05
        action_impacts[columns_X.index(f'{initiator} Political Stability')] -= 0.02
        action_impacts[columns_X.index(f'{target} Public Health')] -= 0.1
        action_impacts[columns_X.index(f'{target} Political Stability')] -= 0.03

    return row_actions, action_impacts


# Initialize an empty DataFrame for actions with columns and the appropriate number of rows
data_actions = pd.DataFrame(columns=action_columns, index=range(number_rows))
data_X_optimized = []  # Initialize an empty list for X data (states)

# First row initialization (start with 0 actions for all)
first_row_actions = [0] * len(action_columns)
data_actions.loc[0] = first_row_actions  # Add first row of actions

# Initialize the starting values for each parameter based on realistic data
initial_values = {
    'A Public Trust': 80.0,  # Increased Public Trust to increase the probability of actions like support
    'A Political Stability': 8.0,  # Increased Political Stability to increase the likelihood of political actions
    'A Trade Balance': -10*100,  # Decreased Trade Balance (increase trade deficit to increase probability of sanctions)
    'A GDP': 15000,  # Increased A's GDP to make economic aid more likely
    'A Unemployment Rate': 6.0,  # Slightly reduced Unemployment Rate to keep A's economy healthy
    'A Inflation Rate': 3.0, 
    'A Foreign Debt': 300, 
    'A Government Spending': 800,
    'A Military Spending': 150, 
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
    'A Innovation Index': 0.5,  # New added parameter for A's innovation level
    'A Social Welfare Spending': 100,  # New added parameter for A's social welfare spending
    'A Social Security Reform':1,
    'A Social Welfare':100,

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
    'B Innovation Index': 0.5,  # New added parameter for A's innovation level
    'B Social Welfare Spending': 100,  # New added parameter for B's social welfare spending
    'B Social Security Reform':1,
    'B Social Welfare':100,
    
    'A to B Imports': 200, 
    'A to B Exports': 150, 
    'B to A Imports': 180, 
    'B to A Exports': 130,
    'A Bond Status': 1, 
    'B Bond Status': 1, 
    'A Sovereignty Disputes': 0, 
    'B Sovereignty Disputes': 0,
    'Ethnic Similarity': 0.5, 
    'Cultural Compatibility': 0.7,
    'Political Similarity': 0.8  # Increased political similarity to improve relations with B and make support more likely
}

# Generate state data and actions row by row
current_values = initial_values.copy()

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

        # List of initiators and targets        
        pairs = [('A', 'B'), ('B', 'A')]

        # Iterate over each pair and apply the corresponding action functions
        for initiator, target in pairs:
            row_actions, action_impacts = major_political_actions(initiator, target, current_values, action_columns, row_actions, action_impacts)
            row_actions, action_impacts = economic_policy_adjustment(initiator, target, current_values, action_columns, row_actions, action_impacts)
            row_actions, action_impacts = military_activity(initiator, target, current_values, action_columns, row_actions, action_impacts)
            row_actions, action_impacts = diplomatic_policy_change(initiator, target, current_values, action_columns, row_actions, action_impacts)
            row_actions, action_impacts = social_policy_and_welfare_reform(initiator, target, current_values, action_columns, row_actions, action_impacts)
            row_actions, action_impacts = environmental_and_energy_policy(initiator, target, current_values, action_columns, row_actions, action_impacts)
            row_actions, action_impacts = technology_and_innovation_strategy(initiator, target, current_values, action_columns, row_actions, action_impacts)
            row_actions, action_impacts = public_health_and_safety_policy(initiator, target, current_values, action_columns, row_actions, action_impacts)

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