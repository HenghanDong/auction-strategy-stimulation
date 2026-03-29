import numpy as np
import pandas as pd


# define 4 strategies

def strategy_rational(value, mechanism):
    if mechanism == "first_price":
        return 0.7 * value
    else:
        return value

def strategy_cautious(value, mechanism):
    if mechanism == "first_price":
        return 0.5 * value
    else:
        return 0.8 * value

def strategy_aggressive(value, mechanism):
    if mechanism == "first_price":
        return 0.9 * value
    else:
        return min(value * 1.2, 100)

def strategy_random(value, mechanism):
    return np.random.uniform(0, value)

strategy_funcs = [
    strategy_rational,
    strategy_cautious,
    strategy_aggressive,
    strategy_random
]

strategy_names = ["Rational", "Cautious", "Aggressive", "Random"]

# 2. set suitable data to stimulate
num_rounds = 1000
values_list = []
bids_fp_list = []
bids_sp_list = []
bids_ap_list = []  # All-Pay bids

for _ in range(num_rounds):
    values = np.random.uniform(5, 20, size=len(strategy_funcs))

    bids_fp = [f(v, "first_price") for f, v in zip(strategy_funcs, values)]
    bids_sp = [f(v, "second_price") for f, v in zip(strategy_funcs, values)]
    bids_ap = [f(v, "all_pay") for f, v in zip(strategy_funcs, values)]  # All-Pay 使用同样策略

    values_list.append(values)
    bids_fp_list.append(bids_fp)
    bids_sp_list.append(bids_sp)
    bids_ap_list.append(bids_ap)

df = pd.DataFrame({
    "values": values_list,
    "bids_first": bids_fp_list,
    "bids_second": bids_sp_list,
    "bids_allpay": bids_ap_list
})


profit_first = {name: [] for name in strategy_names}
profit_second = {name: [] for name in strategy_names}
profit_allpay = {name: [] for name in strategy_names}

#caculate profit
for _, row in df.iterrows():
    values = row["values"]

    # ---------- First Price ----------
    bids_fp = row["bids_first"]
    winner_fp = max(range(len(bids_fp)), key=lambda i: bids_fp[i])
    payment_fp = bids_fp[winner_fp]
    profit_first[strategy_names[winner_fp]].append(values[winner_fp] - payment_fp)

    # ---------- Second Price ----------
    bids_sp = row["bids_second"]
    winner_sp = max(range(len(bids_sp)), key=lambda i: bids_sp[i])
    payment_sp = sorted(bids_sp, reverse=True)[1]
    profit_second[strategy_names[winner_sp]].append(values[winner_sp] - payment_sp)

    # ---------- All-Pay Auction ----------
    bids_ap = row["bids_allpay"]
    winner_ap = max(range(len(bids_ap)), key=lambda i: bids_ap[i])

    for i, name in enumerate(strategy_names):
        if i == winner_ap:
            profit_allpay[name].append(values[i] - bids_ap[i])  # 赢了
        else:
            profit_allpay[name].append(-bids_ap[i])             # 输了也要付钱


print("Average Profit (First Price Auction):")
for name in strategy_names:
    print(f"{name}: {np.mean(profit_first[name]):.4f}")

print("\nAverage Profit (Second Price Auction):")
for name in strategy_names:
    print(f"{name}: {np.mean(profit_second[name]):.4f}")

print("\nAverage Profit (All-Pay Auction):")
for name in strategy_names:
    print(f"{name}: {np.mean(profit_allpay[name]):.4f}")
