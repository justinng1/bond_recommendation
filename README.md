# bond_recommendation

## Notes
- 1500 customers are generated.
- 52 weeks of trades.

### Generating customer preferences
- Average # of trades per customer per week: ~5 (lognormal distributon)
- Customer risk appetite generated using a dirichlet distribution (np.random.dirichlet((0.70,0.2,0.1), size))
- Customer sector preferences generated using a dirichlet distribution (np.random.dirichlet((1/4,)*4, size))
- Customer maturity preferences generated using a dirichlet distribution (np.random.dirichlet((1/5,)*5, size))

### Generating treasury yields
- starting yield: 1.0%
- a random number is generated and added to the yield each week.

### Generating customer trades
1. Generate bond risk based on preferences.
2. Generate bond maturity based on preferences.
3. Generate treasury yield.
4. Generate bond yield based on risk level, maturity and treasury yield.
5. Generate bond sector based on preferences.

## Recommendation Engines
- bond_trade1.ipynb contains BI Report and content based filtering techniques.
- bond_trade2.ipynb contains implicit/explicit Matrix factorization using Spark ML.

## references
Collaborative Filtering for Implicit Feedback Datasets: http://yifanhu.net/PUB/cf.pdf

Optimal client recommendation for market makers in illiquid financial products: http://ecmlpkdd2017.ijs.si/papers/paperID482.pdf
