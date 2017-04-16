import sys
import math
from Nboard import *

method=sys.argv[1]
state=list(map(int,sys.argv[2].split(",")))
print(method)
print(state)
solve(method,state)