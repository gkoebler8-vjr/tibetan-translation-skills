import json, glob, os, sys, collections
W="<session>/subagents/workflows"
def agent_usage(path):
    req={}
    model=effort=None; t0=t1=None
    for line in open(path):
        try: j=json.loads(line)
        except: continue
        m=j.get("message") or {}
        u=m.get("usage") if isinstance(m,dict) else None
        if not u: continue
        model=model or j.get("advisorModel"); effort=effort or j.get("effort")
        ts=j.get("timestamp"); t0=t0 or ts; t1=ts
        r=j.get("requestId") or m.get("id")
        d=req.setdefault(r,{"in":u.get("input_tokens",0),"cc":u.get("cache_creation_input_tokens",0),"cr":u.get("cache_read_input_tokens",0),"out":0})
        d["out"]=max(d["out"],u.get("output_tokens",0))
    tot={"in":0,"cc":0,"cr":0,"out":0,"calls":len(req)}
    for d in req.values():
        for k in ("in","cc","cr","out"): tot[k]+=d[k]
    return tot, model, effort, t0, t1
rows=[]
for wf in sorted(glob.glob(W+"/wf_*")):
    for meta in glob.glob(wf+"/agent-*.meta.json"):
        m=json.load(open(meta)); tr=meta.replace(".meta.json",".jsonl")
        if not os.path.exists(tr): continue
        u,model,effort,t0,t1=agent_usage(tr)
        rows.append((os.path.basename(wf)[3:11], m.get("description","?"), model, effort, u, t0, t1))
print(f"{'wf':9s} {'run':34s} {'model':16s} {'eff':6s} {'calls':>5s} {'new(in+cw+out)':>14s} {'out':>7s} {'cache_r':>9s}")
for wf,label,model,effort,u,t0,t1 in sorted(rows,key=lambda r:(r[0],r[1])):
    new=u["in"]+u["cc"]+u["out"]
    print(f"{wf:9s} {label[:34]:34s} {str(model)[7:23]:16s} {str(effort):6s} {u['calls']:5d} {new:14d} {u['out']:7d} {u['cr']:9d}")
if len(sys.argv)>1:
    json.dump([dict(wf=r[0],run=r[1],model=r[2],effort=r[3],**r[4]) for r in rows], open(sys.argv[1],"w"), indent=1)
