"""T1-b: mutual pair vs one-sided. Working-set can still list solos."""

from envs.pgg_scripted.env import ScriptedPGG


def pairs(noms):
    out = []
    for i, s in noms.items():
        for j in s:
            if i < j and i in noms.get(j, set()):
                out.append((i, j))
    return out


env = ScriptedPGG(n=4, seed=0)
mutual = {0: {0, 1}, 1: {1, 0}, 2: {2}, 3: {3, 0}}
print("working", sorted(env.form_groups(mutual)), "pairs", pairs(mutual))
# pairs should be [(0, 1)] only — 3→0 is one-sided

one_way = {0: {0, 1}, 1: {1}, 2: {2}, 3: {3}}
print("working", sorted(env.form_groups(one_way)), "pairs", pairs(one_way))
# pairs [] — 0 listed 1, 1 did not list 0
