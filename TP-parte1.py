def sofiaa(vec):
    p= vec[0]
    u= vec[len(vec)-1]

    if(p>u):
        vec.pop(0)
        return p
    else:
        vec.pop(len(vec)-1)
        return u
    
def mateoo(vec):
    p= vec[0]
    u= vec[len(vec)-1]

    if(p<u):
        vec.pop(0)
        return p
    else:
        vec.pop(len(vec)-1)
        return u
    
    
def juego_greedy(vec):
    
    v_sofia = [] * (len(vec)//2)
    v_mateo = [] * (len(vec)//2)

    for i in range(0, len(vec)):
        if (i%2==0 or i==0):
            v_sofia.append(sofiaa(vec))

        else:
            v_mateo.append(mateoo(vec))

    return v_sofia, v_mateo