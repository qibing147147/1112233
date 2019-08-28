from g18_env import Game_env 

env = Game_env(None,None,None,None,None,None,None)



print (env.state)

for i in range(10):
    s_,reward,done = env.step('0')
    print (s_,reward,done,env.state[-1])


