import math_tools

num1 = float(input("Enter the first number: "))
num2 = float(input("Enter the second number: "))
operation = input("Which operation?: ")

operations = {"add": math_tools.add, "subtract": math_tools.subtract, "multiply": math_tools.multiply, "divide": math_tools.divide}

result = "Invalid operation"
if operation in operations:
    result = operations[operation](num1, num2)

# Display the result
print(f"Result: {result}")