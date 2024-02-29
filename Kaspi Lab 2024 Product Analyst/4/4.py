
import numpy as np

new_users = np.array([12000, 11500, 10000, 17000, 14350, 12200, 11100, 14784, 13347, 20220])
retention_rates = np.array([100, 20.53, 18.12, 17.15, 15.95, 14.4, 14, 14, 14, 14, 14, 14, 14]) / 100

def calculate_mau(new_users, retention_rates):
    months = len(new_users)
    active_users = np.zeros(months)
    for month in range(months):
        for prev_month in range(month + 1):
            retention_rate = retention_rates[month - prev_month] if month - prev_month < len(retention_rates) else 0
            active_users[month] += new_users[prev_month] * retention_rate
    return active_users

mau = calculate_mau(new_users, retention_rates)
mau_october = mau[-1]
print(mau_october)
