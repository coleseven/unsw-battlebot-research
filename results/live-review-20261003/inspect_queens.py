import json
from pathlib import Path
from collections import Counter, defaultdict
from bcsim import replay as rp, reconstruct

root = Path(__file__).parent
rows = json.loads((root / 'games.json').read_text())
all_out = []
for row in rows:
    r = rp.load(root / f"{row['game']}.replay")
    board = reconstruct.Board(r.map_text)
    bodies = {i: list(b) for i, (t, b) in enumerate(board.dragons)}
    teams = {i: t for i, (t, b) in enumerate(board.dragons)}
    qid = row['stats']['teams'][row['side']]['queen']['id']
    hist = []; rnd = 0; actor = None; death = None
    for e in r.events:
        k = e[0]
        if k == rp.ROUND_START: rnd = e[1]
        elif k == rp.TURN_START:
            actor = e[1]
            if actor == qid:
                b = bodies[qid]; opts = {}
                occupied = {p:(d, i, teams[d]) for d, bb in bodies.items() for i,p in enumerate(bb)}
                for dr in 'NESW':
                    dest = board.dest(*b[0], dr)
                    opts[dr] = {'dest':dest, 'occupied':occupied.get(dest), 'edge':board.edge(*b[0],dr)}
                hist.append({'round':rnd,'head':b[0],'length':len(b),'options':opts,
                             'free':[d for d,o in opts.items() if o['dest'] is not None and o['occupied'] is None]})
        elif k == rp.DRAGON_ACTION and e[1] == qid:
            hist[-1]['action'] = e[2]
        elif k == rp.DRAGON_UPDATE:
            d, head, tail = e[1], e[3], e[4]
            b = bodies.get(d)
            if b is None: continue
            if b[0] != head: b.insert(0,head)
            if tail in b: del b[len(b)-b[::-1].index(tail):]
        elif k == rp.DRAGON_SPLIT:
            _, parent, child, t, _, pb, cb = e
            bodies[parent], bodies[child], teams[child] = list(pb), list(cb), t
        elif k == rp.DRAGON_DEATH:
            if e[1] == qid:
                death = {'round':rnd,'reason':e[2],'actor':actor,'actor_team':teams.get(actor),
                         'head':bodies[qid][0], 'length':len(bodies[qid])}
                break
            bodies.pop(e[1],None)
    all_out.append({'game':row['game'],'battle':row['battle'],'map':row['map'],'side':row['side'],
                    'win':row['stats']['winner']==row['side'],'death':death,'last_turns':hist[-12:]})
(root / 'queen-cases.json').write_text(json.dumps(all_out,indent=2))
print('cases',len(all_out))
for c in all_out:
    if c['death'] and (c['death']['round'] < 40 or c['death']['actor_team']==c['side']):
        print(json.dumps({k:v for k,v in c.items() if k!='last_turns'},ensure_ascii=True))
