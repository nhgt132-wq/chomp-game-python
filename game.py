# -*- coding:utf-8 -*-
#-------------------------------------------------------
# Pythonで実装した「チョンプ（Chomp）」ゲームです。  
# MINMAX探索を用いたコンピュータ対戦ができます。
#-------------------------------------------------------
#
# ゲーム概要：
# - チョンプは、毒入りチョコを避けながら交互にチョコを食べるゲームです。
#
#  N = 5, M = 3 の配置
# +----+----+----+----+----+
# |  1 |  2 |  3 |  4 |  5 |
# +----+----+----+----+----+
# |  6 |  7 |  8 |  9 | 10 |
# +----+----+----+----+----+
# | 11 | 12 | 13 | 14 | 15 |
# +----+----+----+----+----+
#
# ルール：
# ・ プレイヤーは交互にチョコを選択します。
# ・ 選択したチョコより右かつ下にあるチョコはすべて食べられます。
# ・ 左上の「1」は毒入りチョコです。
# ・ 毒入りチョコを食べたプレイヤーの負けです。
#
# 例：
# - 「9」を選択すると、
# -    9, 10, 14, 15
# -  が同時に取り除かれます。
#
# 使用技術：
#
# - Python 3
# - MINMAX探索
#
# 実行方法：
#
# 1. リポジトリをクローン
#
# ```bash
# git clone https://github.com/nhgt132-wq/chomp-game-python.git
# ```
#
# 2. ディレクトリへ移動
#
# ```bash
# cd chomp-game-python
# ```
#
# 3. 実行
#
# ```bash
# python game.py
# ```
#
# 操作方法
#
# - 盤面に表示されている数字を入力してください。
# 例：
#
# ```text
# You > 9
# ```
#
# 終了する場合：
#
# ```text
# You > q
# ```
#
# アルゴリズム：
# - コンピュータ側は MINMAX 法を利用して最適手を探索しています。
#
# ライセンス：
# - MIT License

class Game():
    def __init__(self,N=5,M=3):
        self.N = N
        self.M = M
        self.chomp = list(range(1,self.M*self.N+1))
        self.node = {}
        self.edge = {}
        self.eat = []

    #---------------------------------------------------------
    # 盤面の表示
    #---------------------------------------------------------
    def show_chomp(self):
        print('+'+'----+'*max(self.chomp[0:self.N]))
        for i in range(self.M):
            n = sum(map(bool,self.chomp[i*self.N:(i+1)*self.N]))
            if n == 0:
                continue
            print('|',end='')
            for j in range(n):
                print(' {0:2d} |'.format(self.chomp[i*self.N+j] ),end='')
            print('\n+'+'----+'*n)

    #=========================================================
    # MINMAX 探索
    #=========================================================
    def minmax(self,n,player):
        if len(self.edge[n])==0:
            return self.change(player)

        val = []
        for s in self.edge[n]:
            val.append(self.minmax(s,self.change(player)))
        if player == 0:
            return max(val)
        else:
            return min(val)

    #---------------------------------------------------------
    # 交代 先手:0 / 後手:1
    #---------------------------------------------------------
    def change(self,player):
        if player == 0:
            return 1
        else:
            return 0

    #---------------------------------------------------------
    # コンピュータの選択
    #---------------------------------------------------------        
    def select(self,p):
        n = self.chomp2node(self.chomp)
        hlist = [self.minmax(s,p) for s in self.edge[n]]
        if max(hlist) != 0:
            s = self.edge[n][hlist.index(max(hlist))]
        else:
            s = self.edge[n][-1]
        for i in range(self.M*self.N):
            if self.node[n][i] != self.node[s][i]:
                return i

    def hint(self,c,p):
        print([self.minmax(s,p) for s in self.edge[self.chomp2node(c)]])

    #---------------------------------------------------------
    # 盤面の展開
    #---------------------------------------------------------
    def expand_chomp(self,c):
        return [self.next_chomp(c,k) for k in range(self.M*self.N) if c[k]]

    #---------------------------------------------------------
    # 選択した盤面
    #---------------------------------------------------------
    def next_chomp(self,c,k):
        new = c.copy()
        for i in range(int(k/self.N),self.M):
            for j in range(k%self.N,self.N):
                new[i*self.N+j] = 0
        return new

    #---------------------------------------------------------
    # 盤面から節点名への変換
    #---------------------------------------------------------        
    def chomp2node(self,c):
        return [k for k, v in self.node.items() if v == c][0]

    #=========================================================
    # 木の作成
    #=========================================================
    # 節点
    #---------------------------------------------------------
    def make_node(self,n):
        if n in self.node.values():
            return
        self.node['n'+str(len(self.node))] = n
        for s in self.expand_chomp(n):
            self.make_node(s)
    #---------------------------------------------------------
    # 枝
    #---------------------------------------------------------
    def make_edge(self):
        for n in self.node:
            self.edge[n] = [self.chomp2node(s)
                            for s in self.expand_chomp(self.node[n])]

    #=========================================================
    # ゲーム・メイン
    #=========================================================
    def run(self):

        self.make_node(self.chomp)
        self.make_edge()

        player = 0
        while True:
            self.show_chomp()
            print('')

            if player == 0:
                key = input('You > ')
                if key == 'q':
                    break
                if key not in [ str(i) for i in self.chomp if i != 0 ]:
                    print('盤面にある数字を入力して下さい。')
                    continue
                k = int(key)-1
                self.eat.append(k+1)
            else:
                k = self.select(player)
                print('Computer > ', k+1)

            self.chomp = self.next_chomp(self.chomp,k)

            if sum(self.chomp) == 0:
                if player == 1:
                    print('\nあなたの勝ちです')
                    print('最初に',self.eat[0],'を食べました\n')
                else:
                    print('\nあなたの負けです\n')
                break

            player = self.change(player)

        input()

if __name__ == '__main__':
    game = Game()
    game.run()

# EOF