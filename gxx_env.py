# coding=UTF-8
import numpy as np
import time
import sys

#模拟G马赛克的游戏环境
#1rmb = 1000金币 = 10万银币



class Game_env:

    def __init__(
            self,
            action_space,
            n_actions,
            gem_table,
            xiulian_table,
            fabao_table,
            jingmai_table,
            state,
            index=1,
            weapon_taiyang_pay=0,
            head_taiyang_pay=0,
            yueliang_pay=0,
            shoes_hei_pay=0,
            yaodai_hei_pay=0,

            
    ):


        
        #提升各个部位的石头
        #提升各个修炼
        #提升各个法宝
        #点经脉
        self.index = 1
        self.weapon_taiyang_pay=0
        self.head_taiyang_pay=0
        self.yueliang_pay=0
        self.shoes_hei_pay=0
        self.yaodai_hei_pay=0
        self.action_space = ['gem_weapon',
        'gem_cloth',
        'gem_head',
        'gem_shoes',
        'gem_yaodai',
        'gem_xianglian',
        'fabao_feijian',
        'fabao_fengdai',
        'fabao_jinjia',
        'fabao_doupeng',
        'xiulian_gong',
        'xiulian_wukang',
        'xiulian_fakang',
        'xiulian_fengkang',
        'jingmai']
        self.n_actions = len(self.action_space)
        #gem_table是宝石各等级所需要消耗的金钱
        #光芒石
        self.gem_table=np.zeros((9,13))
        self.gem_table[0] = [0.48*pow(2,max(i-1,0)) for i in range(13)]
        #太阳石
        self.gem_table[1] = [0.55*pow(2,max(i-1,0)) for i in range(13)]
        #昆仑玉
        self.gem_table[2] = [0.52*pow(2,max(i-1,0)) for i in range(13)]
        #月亮石
        self.gem_table[3] = [0.63*pow(2,max(i-1,0)) for i in range(13)]
        #神秘石
        self.gem_table[4] = [0.44*pow(2,max(i-1,0)) for i in range(13)]
        #红纹石
        self.gem_table[5] = [0.46*pow(2,max(i-1,0)) for i in range(13)]
        #翡翠石
        self.gem_table[6] = [0.53*pow(2,max(i-1,0)) for i in range(13)]
        #舍利子
        self.gem_table[7] = [0.6*pow(2,max(i-1,0)) for i in range(13)]
        #黑宝石
        self.gem_table[8] = [0.7*pow(2,max(i-1,0)) for i in range(13)]

        #加上宝石锤的金额
        self.gem_table[:,8]+=28.8
        self.gem_table[:,9]+=28.8*3
        self.gem_table[:,10]+=28.8*7
        self.gem_table[:,11]+=28.8*15
        self.gem_table[:,12]+=28.8*31

        guangmang_pay=0
        taiyang_pay=0
        kunlun_pay=0
        shenmi_pay=0
        hongwen_pay=0
        feicui_pay=0
        shelizi_pay=0
        hei_pay=0

        #修炼消耗表
        self.xiulian_table=np.zeros((2,25))
        #攻修
        self.xiulian_table[0] = [3,4.8,7.2,10.2,13.8,18,22.8,28.2,34.2,40.8,49.5,57.3,65.7,74.7,84.3,94.5,105.3,116.7,128.7,141.3,157.5,175.5,196.5,220.5,266.5]
        #防&抗修
        self.xiulian_table[1] = self.xiulian_table[0]*2/3


        #法宝消耗表（可同宝石）
        tmp_fabao_table=np.zeros((2,10))
        #1型消耗
        tmp_list = [0,10,20,40,60,80,100,150,200,300]
        tmp_fabao_table[0] = [i/5 for i in tmp_list]
        tmp_fabao_table[1] = [i*3/10 for i in tmp_list] 

        #法宝精华估价 风袋 附灵玉 飞剑2.2W  
        #九黎战鼓 葫芦 双甲 汇灵盏 1.5W
        #其他 1W
        self.fabao_table = np.zeros((5,10))

        #风袋 附灵玉 飞剑
        self.fabao_table[0] = tmp_fabao_table[1] 
        self.fabao_table[0][3] += 22*3
        self.fabao_table[0][7] += 22*10
        self.fabao_table[0][9] += 22*15

        #九黎战鼓 葫芦 汇灵盏
        self.fabao_table[1] = tmp_fabao_table[1] 
        self.fabao_table[1][4] += 15*3
        self.fabao_table[1][7] += 15*10
        self.fabao_table[1][9] += 15*15

        #七宝玲珑灯 番天印 捆仙绳
        self.fabao_table[2] = tmp_fabao_table[0] 
        self.fabao_table[2][4] += 10*1
        self.fabao_table[2][7] += 10*5
        self.fabao_table[2][9] += 10*10

        #双甲
        self.fabao_table[3] = tmp_fabao_table[0] 
        self.fabao_table[3][4] += 15*3
        self.fabao_table[3][7] += 15*10
        self.fabao_table[3][9] += 15*15

        
        #其他法宝
        self.fabao_table[4] = tmp_fabao_table[1] 
        self.fabao_table[4][4] += 15*3
        self.fabao_table[4][7] += 15*10
        self.fabao_table[4][9] += 15*15



        #经脉消耗表
        self.jingmai_table = [50,100,100,150,150,200,200,250,250,300,300,450]


        #随机拿出一个池子中的角色
        #test 功双防血速 
        #宝石等级：  武器 衣服 头 项链 腰带 鞋子 
        #法宝等级： 飞剑 风袋 物理甲 法术甲 
        #修炼：  攻 物防 法防 抗封
        #经脉
        #剩余金钱
        self.state = [1850,900,900,3300,850,14,14,14,14,14,14,5,5,5,5,12,10,10,10,1,3000]



    def step(self, action):
        money = self.state[-1]
        if money<=0 or self.index >=30:
            done = True
            return self.state, 0, done
        #action_space = ['gem_weapon','gem_cloth','gem_head','gem_shoes'，'gem_yaodai','gem_necklect']
        # 0-5 宝石
        if (action=='0' and self.state[5]<26):
            if(money >= self.gem_table[1][int(self.state[5]/2)]):
                self.state[0]+=8
                self.state[-1]  -= self.gem_table[1][int(self.state[5]/2)]
                self.state[5]+=1
                
        
        if action =='1' and self.state[6]<26 :
            if(money >= self.gem_table[3][int(self.state[6]/2)]):
                self.state[1]+=8
                self.state[-1]  -= self.gem_table[6][int(self.state[6]/2)]
                self.state[6]+=1

        if action =='2' and self.state[7]<26:
            if(money >= self.gem_table[1][int(self.state[7]/2)]):
                self.state[0]+=8
                self.state[-1]  -= self.gem_table[7][int(self.state[7]/2)]
                self.state[7]+=1
                
        if action =='3' and self.state[8]<26 :
            if(money >= self.gem_table[8][int(self.state[8]/2)]):
                self.state[4]+=8
                self.state[-1]  -= self.gem_table[8][int(self.state[-3]/2)]
                self.state[8]+=1
                
        
        if action =='4'  and self.state[9]<26:
            if(money >= self.gem_table[8][int(self.state[9]/2)]):
                self.state[4]+=8
                self.state[-1]  -= self.gem_table[8][int(self.state[-2]/2)]
                self.state[9]+=1
                

        if action =='5'  and self.state[10]<26:
            if(money >= self.gem_table[6][int(self.state[10]/2)]):
                self.state[2]+=8
                self.state[-1]  -= self.gem_table[6][int(self.state[-4]/2)]
                self.state[10]+=1
        
        # 6-9 飞剑 风带 金甲 斗篷
        if action == '6' and self.state[11]<10:
            if(money >= self.fabao_table[0][self.state[11]]):
               self.state[0] += (self.state[0] - 1000) * 0.02
               self.state[-1] -= self.fabao_table[0][self.state[11]]
               self.state[11] += 1
        
        if action == '7' and self.state[12]<10:
            if(money >= self.fabao_table[0][self.state[12]]):
               self.state[0] += self.state[4] * 0.02
               self.state[-1] -= self.fabao_table[0][self.state[12]]
               self.state[12] += 1
        
        if action == '8' and self.state[13]<10:
            if(money >= self.fabao_table[3][self.state[13]]):
               self.state[0] += self.state[1] * 0.02
               self.state[-1] -= self.fabao_table[3][self.state[13]]
               self.state[13] += 1

        if action == '9' and self.state[14]<10:
            if(money >= self.fabao_table[3][self.state[14]]):
               self.state[0] += self.state[2] * 0.02
               self.state[-1] -= self.fabao_table[3][self.state[14]]
               self.state[14] += 1
        
        # 10-13 攻 物 法 封

        if action == '10' and self.state[15]<10:
            if(money >= self.xiulian_table[0][self.state[15]]):
               self.state[0] += (self.state[0] - 1000) * 0.02
               self.state[-1] -= self.xiulian_table[0][self.state[15]]
               self.state[15] += 1
        
        if action == '11' and self.state[16]<10:
            if(money >= self.xiulian_table[1][self.state[16]]):
               self.state[0] += self.state[2] * 0.02
               self.state[-1] -= self.xiulian_table[1][self.state[16]]
               self.state[16] += 1
        
        if action == '12' and self.state[17]<10:
            if(money >= self.xiulian_table[1][self.state[17]]):
               self.state[0] += self.state[2] * 0.02
               self.state[-1] -= self.xiulian_table[1][self.state[17]]
               self.state[17] += 1
        
        if action == '13' and self.state[18]<10:
            if(money >= self.xiulian_table[1][self.state[18]]):
               self.state[0] += (self.state[0] - 1000) * 0.005
               self.state[-1] -= self.xiulian_table[1][self.state[18]]
               self.state[18] += 1
        
        # 经脉

        if action == '14' and self.state[19]<10:
            if(money >= self.jingmai_table[self.state[19]]):
               self.state[0] += (self.state[0] - 1000) * 0.01
               self.state[-1] -= self.jingmai_table[self.state[19]]
               self.state[19] += 1

                                                     




        
        reward = 0
        done = False
        if self.state[0]>=3000 and self.state[1]>=1000 and self.state[2]>=1040 and self.state[4]>= 850:
            reward =1 + self.state[-1]/3000
            done = True
        else:
            reward = 0
        

        #改变后的状态
        s_ = np.array(self.state)
        self.index += 1 
        return s_, reward, done






if __name__ == '__main__':
    env = Game_env()
