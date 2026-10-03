import sys,re,os
D=os.path.dirname(os.path.abspath(__file__))
def src(u):
    return open(f"{D}/dict/{u}.txt").readline().strip().replace("## unit 1: ","")
def add(u,body):
    s=f"\n=== {u} ===\nSOURCE      {src(u)}\n"+body.strip("\n")+"\n"
    open(f"{D}/tantra.construal.md","a").write(s)
