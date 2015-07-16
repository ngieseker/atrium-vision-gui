
def match(obj_list, tar):
    """matches two objects based on the position closest to target"""

    if not len(obj_list):
        return -1

    # Arbirtary initial distance
    m = 10000
    cnt = 0;
    idx = -1

    
    # Split on coordinate seperator for given coordinate
    td = tar.split(":")
    tx = int(td[0])
    ty = int(td[1])
    
    # Iterates through each current objects coordinates
    for i in obj_list:
        # see above
        l = i["text"].split(":")
        cx, cy = int(l[0]), int(l[1])
        
        cur = dist(cx, cy, tx, ty)
        if cur < m:
            idx = cnt
            m = cur
        cnt += 1
    return idx

def dist(cx, cy, x, y):
    """just a little distance function 
    (square root omitted for time considerations)"""
    
    x = 2*(x - cx)
    y = y - cy
    
    # This is the minimum distance for something to be considered the
    # same object, will need tuning before final value is decided
    if (8 < x or 4 < y):
        return 10001
    return (x*x) + (y*y)
    

