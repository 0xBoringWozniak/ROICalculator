# python ROI calculator

**General theory**

Let we have some investments in strategy and we want to calclulate ROI. If we dont make any withdrawals or deposits it is easy to calculate ROI = NAV / initital investments - 1. However, if we make potfolio rebalancing or new deposits/withdrawals we should account them too and simple ROI formula is not enough. For this purpose we can use following algorithm:

1. Create virtual pie with shares = deposited asset (in shares) and set share price P = 1.

2. Any deposit or withrawal is equivalent to buying or selling some shares per share price P_T0.

Let X was added to virtual pie at time T, where X > 0 wneh we make deposit, and X < 0 when we make withdrawal;

T0 = T - eps - timestamp before transaction
T1 = T + eps - timestamp after transaction

Pie consisted of N SHARES with share price P_0 = NAV_T0 / N.

New shares amount will be M = N + X / P_0
Updated share price P_T1 = NAV_T1 / M

3. So, for each moment we have our NAV_t, virtual shares amount N_t and share price P_t = NAV_t / N_t and we can calculate ROI as P_t / P_t0 - 1
Moreover we can calculate ROI at any period (t, t0), t > t0.

**Full theory**: https://www.investopedia.com/terms/r/returnoninvestment.asp
