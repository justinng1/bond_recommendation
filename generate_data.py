
import numpy as np

num_customers = 1500
num_weeks = 52
starting_tres_yield = 1.0
filename = '/home/ec2-user/rbc_project/data/trade_data{}.txt'
customer_filename = '/home/ec2-user/rbc_project/data/customer_prefs.txt'

# generate customer attributes.

# generates average trade frequencies for customers.
def generate_avg_trade_freq(size):
    mu, sigma = 1.25, 1.5 # mean and standard deviation
    s = np.random.lognormal(mu, sigma, size)
    return s

# generates risk preferences for customers.
def generate_customer_risk(size):
    return np.random.dirichlet((0.70,0.2,0.1), size)

# generates sector preferences for customers. Assumes 4 sectors.
def generate_customer_sector(size):
    num_cat = 4
    return np.random.dirichlet((1/num_cat,)*num_cat, size)

# generates maturity length preferences for customers. Assumes 1-5 years.
def generate_customer_maturity(size):
    num_cat = 5
    return np.random.dirichlet((1/num_cat,)*num_cat, size)


# generates the number of trades in each week.
def get_num_weekly_trades(avg_freq, num_weeks):
    mu = avg_freq
    stdev = avg_freq * 0.5
    s = np.random.normal(mu, stdev, num_weeks)
    s[s < 0] = 0
    return np.rint(s)

# Get a new treasury yield.
def get_treasury_yield(prev_yield):
    mu = 0.01
    sigma = 0.05
    s = np.random.lognormal(mu, sigma, 1)
    return s[0]

# loop through trades using these.
def generate_bond_risk(customer_risk_appetites):
    # one draw from a multinomial distribution.
    level = np.random.multinomial(1, customer_risk_appetites)
    if level[0] == 1:
        risk = 'LOW'
    elif level[1] == 1:
        risk = 'MED'
    else:
        risk = 'HIGH'
    return risk

def generate_bond_maturity(customer_maturity_pref):
    # one draw from a multinomial distribution.
    maturity = np.random.multinomial(1, customer_maturity_pref)
    ind = np.nonzero(maturity)[0][0] + 1
    return ind

def generate_bond_sector(customer_sector_pref):
    # one draw from a multinomial distribution.
    sector = np.random.multinomial(1, customer_sector_pref)
    ind = np.nonzero(sector)[0][0]
    if ind == 0:
        return 'A'
    elif ind == 1:
        return 'B'
    elif ind == 2:
        return 'C'
    else:
        return 'D'

def generate_bond_yield(risk_level, time_until_maturity, treasury_yield):
    if risk_level == 'LOW':
        mu = treasury_yield + 0.25
    elif risk_level == 'MED':
        mu = treasury_yield + 1.0
    else:
        mu = treasury_yield + 3.0

    if time_until_maturity == 2:
        mu = mu + 0.35
    elif time_until_maturity == 3:
        mu = mu + 0.4
    elif time_until_maturity == 4:
        mu = mu + 0.45
    elif time_until_maturity == 5:
        mu = mu + 0.5
        
    stdev = mu * 0.15
    s = np.random.normal(mu, stdev, 1)
    return s[0]

# use the functions above to generate data.    
customer_avg_freqs = generate_avg_trade_freq(num_customers)
customer_risk_appetites = generate_customer_risk(num_customers)
customer_sector_prefs = generate_customer_sector(num_customers)
customer_maturity_prefs = generate_customer_maturity(num_customers)
prev_tres_yield = starting_tres_yield

# output customer preferences (could be helpful to evaluate results).
with open(customer_filename, 'w') as f:
    for i in range(num_customers):
        avg_freq = customer_avg_freqs[i]
        low_risk_pref = customer_risk_appetites[i,0]
        med_risk_pref = customer_risk_appetites[i,1]
        high_risk_pref = customer_risk_appetites[i,2]
        sector_a_pref = customer_sector_prefs[i,0]
        sector_b_pref = customer_sector_prefs[i,1]
        sector_c_pref = customer_sector_prefs[i,2]
        sector_d_pref = customer_sector_prefs[i,3]
        
        mat_1_pref = customer_maturity_prefs[i,0]
        mat_2_pref = customer_maturity_prefs[i,1]
        mat_3_pref = customer_maturity_prefs[i,2]
        mat_4_pref = customer_maturity_prefs[i,3]
        mat_5_pref = customer_maturity_prefs[i,4]
        f.write('{0},{1:.2f},{2:.2f},{3:.2f},{4:.2f},{5:.2f},{6:.2f},{7:.2f},{8:.2f},{9:.2f},{10:.2f},{11:.2f},{12:.2f},{13:.2f}\n'.format(
                i,avg_freq, 
                low_risk_pref, med_risk_pref, 
                high_risk_pref, sector_a_pref,sector_b_pref,
                sector_c_pref, sector_d_pref,mat_1_pref,mat_2_pref,
                mat_3_pref,mat_4_pref,mat_5_pref))
    


for j in range(num_weeks):
    # get tresury yield.
    tres_yield = get_treasury_yield(prev_tres_yield)
    prev_tres_yield = tres_yield
                
    for i in range(num_customers):
        num_trades_in_week = get_num_weekly_trades(customer_avg_freqs[i], 1)
        with open(filename.format(j), 'a') as f:
            for k in range(int(num_trades_in_week)):
                # get risk level of trade.
                risk_appetite = customer_risk_appetites[i]
                risk_level = generate_bond_risk(risk_appetite)
                
                # get maturity of bond.
                maturity_pref = customer_maturity_prefs[i]
                maturity = generate_bond_maturity(maturity_pref)
                
                # generate bond yield.
                bond_yield = generate_bond_yield(risk_level, maturity, tres_yield)
                
                # generate bond sector.
                sector_pref = customer_sector_prefs[i]
                bond_sector = generate_bond_sector(sector_pref)
                
                f.write('{},{},{},{},{},{},{}\n'.format(j,i,bond_sector,risk_level, maturity, bond_yield, tres_yield))

