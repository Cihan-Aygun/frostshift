"""Synthetic inventory experiment. Units are cartons; money is illustrative TRY."""
import random
import math

STORES=[('Coast',0,0),('Marina',3,1),('Campus',7,4),('Center',4,6),('Park',1,7),('Suburb',10,8)]
PRODUCTS=['Classic','Almond','White']

def run(seed=42,heat=25,fee=35,policy='transfer'):
    if policy not in ('none','depot','transfer'):raise ValueError('Unknown policy')
    if not 0<=heat<=80 or not 0<=fee<=200:raise ValueError('Parameter outside supported range')
    rng=random.Random(seed)
    demand=[[[max(0,round(rng.gauss((8+s%3*2)*(1+heat/100 if s<2 else 1),2))) for p in PRODUCTS] for s in range(6)] for d in range(7)]
    stock=[[22 if s<2 else 65 for p in PRODUCTS] for s in range(6)]
    initial=sum(map(sum,stock));sold=lost=cost=moved=delivered=0;events=[];history=[]
    for day in range(7):
        # A one-day forecast is generated independently of realized demand.
        forecast=[[math.ceil((8+s%3*2)*(1+heat/100 if s<2 else 1)) for p in PRODUCTS] for s in range(6)]
        if policy=='depot':
            for s in range(6):
                for p in range(3):
                    qty=min(max(0,forecast[s][p]*2-stock[s][p]),240-sum(stock[s]))
                    if qty>0:
                        stock[s][p]+=qty;delivered+=qty;cost+=fee+qty*3
                        events.append(dict(day=day+1,source='Depot',target=STORES[s][0],product=PRODUCTS[p],quantity=qty,cost=fee+qty*3))
        if policy=='transfer':
            capacity=50
            for p in range(3):
                for target in sorted(range(6),key=lambda s:stock[s][p]-forecast[s][p]):
                    need=max(0,forecast[target][p]*2-stock[target][p])
                    donors=sorted((s for s in range(6) if s!=target),key=lambda s:math.dist(STORES[s][1:],STORES[target][1:]))
                    for source in donors:
                        surplus=max(0,stock[source][p]-forecast[source][p]*3)
                        qty=min(need,surplus,capacity,240-sum(stock[target]))
                        distance=math.dist(STORES[source][1:],STORES[target][1:])
                        expense=fee+distance*2+qty
                        # Expected avoided lost-sale contribution is 18 TRY/carton.
                        if qty<=0 or qty*18<=expense:continue
                        stock[source][p]-=qty;stock[target][p]+=qty;need-=qty;capacity-=qty
                        cost+=expense;moved+=qty
                        events.append(dict(day=day+1,source=STORES[source][0],target=STORES[target][0],product=PRODUCTS[p],quantity=qty,cost=round(expense,2)))
        daily_lost=0
        for s in range(6):
            for p in range(3):
                qty=min(stock[s][p],demand[day][s][p]);stock[s][p]-=qty;sold+=qty
                short=demand[day][s][p]-qty;lost+=short;daily_lost+=short
        history.append(dict(day=day+1,stock=[r[:] for r in stock],lost=daily_lost))
    return dict(policy=policy,sold=sold,lost=lost,cost=round(cost,2),contribution=round(sold*18-cost,2),moved=moved,delivered=delivered,remaining=sum(map(sum,stock)),initial=initial,events=events,history=history)

def compare(seed=42,heat=25,fee=35):
    return dict(stores=[dict(name=n,x=x,y=y) for n,x,y in STORES],products=PRODUCTS,
                scenarios=[run(seed,heat,fee,p) for p in ('none','depot','transfer')])

def experiment(heat=25,fee=35,runs=100):
    gains=[]
    for seed in range(runs):
        s=compare(seed,heat,fee)['scenarios']
        gains.append(s[2]['contribution']-s[0]['contribution'])
    ordered=sorted(gains)
    return dict(runs=runs,mean_gain=round(sum(gains)/runs,2),p10=round(ordered[int(.1*(runs-1))],2),p90=round(ordered[int(.9*(runs-1))],2),positive_share=sum(x>0 for x in gains)/runs)
