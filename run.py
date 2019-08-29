from RL_brain import DoubleDQN
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import gxx_env as game_env
import time



MEMORY_SIZE = 3000
ACTION_SPACE = 15

sess = tf.Session()
with tf.variable_scope('Natural_DQN'):
    natural_DQN = DoubleDQN(
        n_actions=ACTION_SPACE, n_features=21, memory_size=MEMORY_SIZE,
        e_greedy_increment=0.001, double_q=False, sess=sess
    )

with tf.variable_scope('Double_DQN'):
    double_DQN = DoubleDQN(
        n_actions=ACTION_SPACE, n_features=21, memory_size=MEMORY_SIZE,
        e_greedy_increment=0.001, double_q=True, sess=sess, output_graph=True)

sess.run(tf.global_variables_initializer())




def train(RL):

    for episode in range(100):
        # initial observation
        env = game_env.Game_env(None,None,None,None,None,None,None,None)
        step = 1
        while True:
           
            arr4nor=np.array([3000,1200,1200,5000,1100,26,26,26,26,26,26,10,10,10,10,20,20,20,20,10,3000])

            observation = np.array(env.state)
            # RL choose action based on observation
            action = RL.choose_action(observation/arr4nor)


            # RL take action and get next observation and reward
            observation_, reward, done = env.step(str(action))

            arr4nor=np.array([3000,1200,1200,5000,1100,26,26,26,26,26,26,10,10,10,10,20,20,20,20,10,3000])


            
            RL.store_transition(observation/arr4nor, action, reward, observation_/arr4nor)

            RL.learn()

            if (episode < 5 or episode >95) :
                print (episode+1, step ,observation_[:5],int(observation_[-1]),action,reward,done)
            # swap observation
            observation = observation_
            step+=1
            # break while loop when end of this episode

            if done:       
                break

        

q_double = train(double_DQN)


