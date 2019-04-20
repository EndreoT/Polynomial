# Polynomial

### Description
A simple API for manipulating polynomials and performing polynomial algebraic and calculus operations.

### Motivation
Gives users an easy to use mathematical polynomial API. Great for checking homework answers involving polynomials. 

### Result
Create a polynomial object first with the constructor accepting either of two arguments:
First, an array of either type int or float. The array's index becomes the polynomial term, and the value of that index is the term's coefficient. Example:
``` Python
>>> poly2 = Polynomial([4, 2, 0, 5, 0])
>>> str(poly2)
'5X^3 + 2X + 4'
```

Second, a list of tuples of length two, each representing a full polynomial term. The first tuple element corresponds to the term's coefficient and is either an int or float. The second tuple element corresponds to the term's power and is must also be either an int or float.
Examples:
``` Python
>>> poly = Polynomial([(2, 3), (5, -2), (.5, 1), (6, 3)])
>>> str(poly)
'8X^3 + 5X^-2 + 1/2X'
```

### Future Improvements
- [ ] Allow for multi-variable polynomials. Example: 3X^2 -7XY + Z^3 + XYZ
