import bottle
import os
import random


@bottle.route('/static/path:path')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    data = bottle.request.json
    game_id = data['game_id']
    board_width = data['width']
    board_height = data['height']
    
    #head_url = '%s://%s/gears.png' % (
    #    bottle.request.urlparts.scheme,
    #    bottle.request.urlparts.netloc
    # )
        
    # TODO: Do things with data

    return {
        'color': 'gold',
        'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
        'head_type': 'tongue',
        'tail_type': 'fat-rattle',
        'name': 'GodKing'
    }


@bottle.post('/move')
def move():
    
    snakes = bottle.request.json[u'snakes']
    data = bottle.request.json
    myID = data[u'you']
    mysnake = [0]
    
    for snake in snakes:
        if snake[u'id'] == myID:
            mysnake = snake

    # TODO: Do things with data
    directions = ['up', 'down', 'left', 'right']

    size = len(mysnake[u'coords'])
    head = mysnake[u'coords'] [0]
    neck = mysnake[u'coords'] [1]
    tail = mysnake[u'coords'] [size - 1]
    direction = [head[0] - neck[0], head[1] - neck[1]]

    headU = [head[0],head[1]-1]
    headL = [head[0]-1,head[1]]
    headD = [head[0],head[1]+1]
    headR = [head[0]+1,head[1]]

    h = 0
    w = 0
    h1 = 0
    w1 = 0

    walls = []                                       #CREATING WALLS ARRAY

    while (h < data['height']):
        a = [[-1, h]]
        walls.extend(a)
        h = h + 1

    while (w < data['width']):
        a = [[w, -1]]
        walls.extend(a)
        w = w + 1
    
    while (h1 < data['height']):
        a = [[data['width'], h1]]
        walls.extend(a)
        h1 = h1 + 1

    while (w1 < data['width']):
        a = [[w1, data['height']]]
        walls.extend(a)
        w1 = w1 + 1

    for snake in snakes:
        bodies = snake[u'coords']
        snakenotail = len(snake[u'coords']) - 1
        tailcoord = snake[u'coords'] [snakenotail]
        bodies.remove(tailcoord)
        walls.extend(bodies)

    map = []

    s = 0
    z = 0
        
    while (s < data['width']):
        z = 0
        while (z < data['height']):
            place = [s, z]
            if place not in walls:
                map.append(place)
            z = z + 1
        s = s + 1

#print map

    if mysnake['health_points'] >= 70:                      #SAFE PATTERN CHASING TAIL
        
        if data['turn'] == 0:                               #START
            if headD in walls:
                return {
                    'move': 'up'
            }
            return {
                'move': 'down'
        }

        tailX = tail [0] - head [0]
        tailY = tail [1] - head [1]

        if abs(tailX) <= abs(tailY):
            if tailY < 0:                                   #UP
                if headU in walls:
                    if tailX > 0:
                        if headR in walls:
                            if headD in walls:
                                return {
                                    'move': 'left'
                            }
                            return {
                                'move': 'down'
                        }
                        return {
                            'move': 'right'
                    }
                    else:
                        if headL in walls:
                            if headD in walls:
                                return {
                                    'move': 'right'
                            }
                            return {
                                'move': 'down'
                        }
                        return {
                            'move': 'left'
                    }
                return {
                    'move': 'up'
            }
            
            else:                                           #DOWN
                if headD in walls:
                    if tailX > 0:
                        if headR in walls:
                            if headU in walls:
                                return {
                                    'move': 'left'
                            }
                            return {
                                'move': 'up'
                        }
                        return {
                            'move': 'right'
                    }
                    else:
                        if headL in walls:
                            if headU in walls:
                                return {
                                    'move': 'right'
                            }
                            return {
                                'move': 'up'
                        }
                        return {
                            'move': 'left'
                }
                return {
                    'move': 'down'
            }
        else:
            if tailX > 0:                                   #RIGHT
                if headR in walls:
                    if tailY > 0:
                        if headD in walls:
                            if headL in walls:
                                return {
                                    'move': 'up'
                            }
                            return {
                                'move': 'left'
                        }
                        return {
                            'move': 'down'
                    }
                    else:
                        if headU in walls:
                            if headL in walls:
                                return {
                                    'move': 'down'
                            }
                            return {
                                'move': 'left'
                        }
                        return {
                            'move': 'up'
                }
                return {
                    'move': 'right'
            }
            
            else:                                           #LEFT
                if headL in walls:
                    if tailY > 0:
                        if headD in walls:
                            if headR in walls:
                                return {
                                    'move': 'up'
                            }
                            return {
                                'move': 'right'
                        }
                        return {
                            'move': 'down'
                    }
                    else:
                        if headU in walls:
                            if headR in walls:
                                return {
                                    'move': 'down'
                            }
                            return {
                                'move': 'right'
                        }
                        return {
                            'move': 'up'
                }
                return {
                    'move': 'left'
            }

    else:                                                   #FOOD SEARCH PATTERN
        i = 0
        Dist = [0] * len(data['food'])
        j = 0
        
        while (i < len(data['food'])):
            Dist[i] = abs(data['food'][i][0]-head[0]) + abs(data['food'][i][1]-head[1])
            i = i + 1

        cFDist = min(Dist)
        cF = -5
        
        while (j < len(data['food'])):
            if Dist[j] == cFDist:
                cF = j
            j = j + 1

        foodX = data['food'][cF][0] - head[0]
        foodY = data['food'][cF][1] - head[1]

        if abs(foodX) > 0:
            if foodX > 0:                                   #FOOD RIGHT
                if headR in walls:
                    if headD in walls:
                        if headL in walls:
                            return {
                                'move': 'up'
                        }
                        return {
                            'move': 'left'
                    }
                    return {
                        'move': 'down'
                }
                return {
                    'move': 'right'
            }

            else:                                           #FOOD LEFT
                if headL in walls:
                    if headU in walls:
                        if headR in walls:
                            return {
                                'move': 'down'
                        }
                        return {
                            'move': 'right'
                    }
                    return {
                        'move': 'up'
                }
                return {
                    'move': 'left'
            }
                
        else:
            if foodY > 0:                                   #FOOD DOWN
                if headD in walls:
                    if headL in walls:
                        if headU in walls:
                            return {
                                'move': 'right'
                        }
                        return {
                            'move': 'up'
                    }
                    return {
                        'move': 'left'
                }
                return {
                    'move': 'down'
            }
            
            else:                                           #FOOD UP
                if headU in walls:
                    if headR in walls:
                        if headD in walls:
                            return {
                                'move': 'left'
                        }
                        return {
                            'move': 'down'
                    }
                    return {
                        'move': 'right'
                }
                return {
                    'move': 'up'
            }

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '192.168.0.11'), port=os.getenv('PORT', '8080'))
