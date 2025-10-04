# Usage Examples

## Basic Calculation
```
User: Calculate 15% tip on $84.50
Assistant: [uses calculate tool with "84.50 * 0.15"]
Result: 12.675
```

## Statistical Analysis
```
User: What's the average of these test scores: 85, 92, 78, 96, 88?
Assistant: [uses statistics tool with numbers=[85,92,78,96,88], operation="mean"]
Mean: 87.8
```

## Investment Planning
```
User: If I invest $5000 at 4.5% annually, compounded monthly, what will it be worth in 10 years?
Assistant: [uses compound_interest tool]
Principal: $5000.00
Final Amount: $7814.17
Total Interest: $2814.17
```

## Persistent Workspace
```
User: Save this portfolio calculation for later: 10000 * 1.07^5
Assistant: [uses save_calculation tool]
Saved Variable: portfolio_return = 14025.52
Expression: 10000 * 1.07^5
Status: Success

User: What was my portfolio return calculation?
Assistant: [uses load_variable tool]
Loaded Variable: portfolio_return = 14025.52
Expression: 10000 * 1.07^5
Saved: 2025-01-15T10:30:00

User: Show me my complete workspace
Assistant: [uses math://workspace resource]
# Math Workspace (2 variables)

## Saved Variables
- portfolio_return: 10000 * 1.07^5 = 14025.52
- circle_area: pi * 5^2 = 78.54

## Statistics
- Total Calculations: 2
- Last Access: 2025-01-15T10:35:00
```
