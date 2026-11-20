import json,sys
d=json.load(open('tools/sentix_base.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for l in d:
    if a<=l['n']<=b: print(f"## {l['n']} need {25-len(l['s'])} | {l['fa']}\n  " + " / ".join(x[0] for x in l['s']))
