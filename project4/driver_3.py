import sys
import sudoku as sdk

start=sys.argv[1]

result = sdk.buildString(sdk.Backtrack(sdk.AC3(start)[1]))
with open("output.txt","w") as f:
    f.write(result)