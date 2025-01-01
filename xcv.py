# Example list of indicators with internal conditions
indicators_with_internal_conditions = ['MACD', 'RSI', 'BollingerBands']

historical_data = fetch_historical_data("symbol")

indicator_values = {}

# Calculate all indicators first
for component in strategy:
    if component['type'] == 'indicator':
        indicator = Indicator(component['name'], component['parameters'])
        value = indicator.calculate(historical_data)
        indicator_key = f"{component['name']}_{component['parameters']['time period']}"
        if value is not None and len(value) > 0:
            indicator_values[indicator_key] = value.iloc[-1]

print(indicator_values)  # Debug print to see indicator values

condition_results = []
# Evaluate conditions and logical operators
for component in strategy:
    if component['type'] == 'condition':
        condition = Condition(component['name'])
        if component['name'] in indicators_with_internal_conditions:
            indicator_key = component['name']
            value = indicator_values.get(indicator_key)
            if value is not None:
                result = condition.evaluate([value])
                condition_results.append(result)
        else:
            if len(indicator_values) >= 2:
                values = list(indicator_values.values())
                result = condition.evaluate([values[-2], values[-1]])
                condition_results.append(result)
    elif component['type'] == 'logicalOperator':
        logical_operator = LogicalOperator(component['name'])
        conditions_met = logical_operator.evaluate(condition_results)
        condition_results = [conditions_met]  # Reset for next logical operation

print("condition_results", condition_results)
