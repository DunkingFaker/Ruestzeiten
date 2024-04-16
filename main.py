
import mip
import chm

inst=chm.get_instance2()
print(inst)

chm.show_demand(inst)

m=mip.Model()
# Zusätzliche Variablen in Periode T, damit p[c][-1] definiert ist
p=[[m.add_var() for _ in range(inst.T+1)] for _ in range(inst.C)]
x=[[[m.add_var() for _ in range(inst.k)] for _ in range(inst.T)] for _ in range(inst.C)]
y=[[[m.add_var(var_type=mip.BINARY) for _ in range(inst.k)] for _ in range(inst.T)] for _ in range(inst.C)]
z=[[m.add_var(var_type=mip.BINARY) for _ in range(inst.k)] for _ in range(inst.T)]

# Bedingungen
for t in range(inst.T):
    m+=mip.xsum(p[c][t] for c in range(inst.C))<=inst.B

for t in range(inst.T):
    for v in range(inst.k):    
        m+=mip.xsum(x[c][t][v] for c in range(inst.C))<=z[t][v]*inst.h

for c in range(inst.C):
    for t in range(inst.T):
        for v in range(inst.k):    
            m+=x[c][t][v]<=inst.h*y[c][t][v]

for c,cc in inst.I:
    for t in range(inst.T):
        for v in range(inst.k):
            m+=y[c][t][v]+y[cc][t][v]<=1

for c in range(inst.C):
    m+=p[c][-1]==0
for t in range(inst.T):
    for c in range(inst.C):
        m+=p[c][t]+inst.d[c][t]==p[c][t-1]+mip.xsum(x[c][t][v] for v in range(inst.k)) 

for t in range(inst.T):
    for v in range(inst.k):
        start=max(0,t-inst.r+1)
        m+=mip.xsum(z[i][v] for i in range(start,t+1))<=1     

# Zielfunktion
m.objective=mip.minimize(mip.xsum(inst.g*z[t][v] for t in range(inst.T) for v in range(inst.k)))

m.verbose=0 # suppress solver output
opt_status=m.optimize()
print("opt status: {}".format(opt_status))
print("Gesamtkosten: {}".format(m.objective_value))

chm.show_solution2(x,z,p,inst,chemical='all')

chm.show_solution2(x,z,p,inst,chemical="Chlor")
chm.show_solution2(x,z,p,inst,chemical="Schwefel")