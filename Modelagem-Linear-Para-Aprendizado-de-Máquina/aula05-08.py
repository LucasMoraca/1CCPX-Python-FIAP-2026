# Exercício de aula com o professor
# preparando o ambiente:
from scipy.stats import norm

# Exercício 1
# A)
print(norm.cdf(164, 175, 10))

# B)

print (norm.sf(164, 175, 10))

# C)
a = norm.cdf(164, 175, 10)
b = norm.cdf(174, 175, 10)
print (b-a)