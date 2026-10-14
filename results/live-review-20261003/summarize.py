import json, statistics
from pathlib import Path
from collections import Counter, defaultdict
root=Path(__file__).parent
rows=json.loads((root/'games.json').read_text())
classes=defaultdict(Counter); maps=defaultdict(Counter); deaths=Counter(); surv=Counter(); lengths=[]; rounds=[]
details=[]; sides=defaultdict(Counter)
for r in rows:
 s=r['stats']; u=r['side']; v='B' if u=='A' else 'A'
 a=s['teams'][u];b=s['teams'][v];q=a['queen'];e=b['queen']
 outcome='win' if s['winner']==u else 'draw' if s['winner'] is None else 'loss'
 category='elimination' if s['end']=='eliminated' else 'queen survival' if bool(q['length'])!=bool(e['length']) else 'queen length' if q['length']!=e['length'] else 'longest/total'
 classes[category][outcome]+=1; maps[r['map']][outcome]+=1;sides[u][outcome]+=1
 surv['ours']+=q['alive'];surv['theirs']+=e['alive']
 ds=[d for d in s['deaths'] if d[6]==q['id']]
 if ds:
  d=ds[0]; label='friendly '+d[2] if d[3]==u else 'enemy '+d[2] if d[3]==v else d[2]
  deaths[label]+=1;rounds.append(d[0]);lengths.append(d[4])
 details.append({'game':r['game'],'battle':r['battle'],'map':r['map'],'opponent':r['opponent']['name'],'side':u,'outcome':outcome,'category':category,'queen':q,'enemy_queen':e,'queen_death':ds,'rounds':s['rounds'],'own_final':a['final'],'enemy_final':b['final'],'own_pearls':a['pearls'],'enemy_pearls':b['pearls'],'timeline':s['timeline']})
summary={'games':len(rows),'from':min(r['at'] for r in rows),'to':max(r['at'] for r in rows),'classes':dict(classes),'maps':dict(maps),'sides':dict(sides),'queen_survival':surv,'queen_deaths':deaths,'median_queen_death_round':statistics.median(rounds),'median_queen_death_length':statistics.median(lengths),'unique_games':len(set(r['game'] for r in rows))}
(root/'summary.json').write_text(json.dumps(summary,indent=2));(root/'details.json').write_text(json.dumps(details,indent=2))
print(json.dumps(summary,indent=2))
