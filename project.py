import matplotlib.pyplot as plt
import pybaseball.pybaseball as pyball
import sklearn.metrics as scikit
from pybaseball import cache
from new_classes import Team


def getFirstN(scores,x):
    return scores[:x]

#Prunes a list of scores, only returning run totals
def pruneList(list):
    new = []
    for i in list:
        if i >= 0:
            new.append(i)
    return new

#Scrapes the data from the Baseball Reference page
def ReadBrefPage(year,name):
    data = pyball.schedule_and_record(year,name)
    RS = data["R"].values.tolist()
    RA = data["RA"].values.tolist()
    RS,RA = pruneList(RS),pruneList(RA)
    W,L = 0,0
    for i in range(len(RS)):
        if (RS[i] > RA[i]):
            W += 1
        else:
            L += 1
    return (RS,RA,W,L)
# uses a big table to calculate a new winning percentage              
def calcNewWinPer(RS,RA):
    wins = 0
    trials = len(RS) * len(RA)
    for i in RS:
        for j in RA:
            if (i > j): wins += 1
            elif (i == j): wins += 0.5
    return wins/trials

# uses the last 5 full seasons of data to calculate 2 projection systems
# and then compares those to their actual winning percentage
    
def newPred():
    cache.enable()

    league = ["NYY","BOS","TBR","BAL","TOR",
              "MIN","DET","CHW","KCR","CLE",
              "OAK","LAA","HOU","TEX","SEA",
              "LAD","SFG","ARI","SDP","COL",
              "CIN","STL","MIL","CHC","PIT",
              "WSN","PHI","ATL","NYM","MIA"]
    trueWinPer = []
    denisWinPer = []
    pythWinPer = []
    years = [2018,2019,2021,2022,2023]
    for year in years:
        for team in league:
            R1,R2,R3 = singleTeamPrediction(team,year)
            trueWinPer.append(R1)
            denisWinPer.append(R2)
            pythWinPer.append(R3)
    
    # plotting
    x = [0.25,0.4,0.5,0.6,0.75]
    print("As a predictive metric:\n")
    print("My R2 score: " + str(scikit.r2_score(trueWinPer,denisWinPer)))
    print("Their R2 score: " + str(scikit.r2_score(trueWinPer,pythWinPer)))
    plt.figure()
    plt.clf()
    plt.plot(trueWinPer,denisWinPer,"bo",label="My Way")
    plt.plot(trueWinPer,pythWinPer,"ro",label = "Pyth Way")
    plt.legend(loc = "upper right")
    plt.plot(x,x,"-")
    plt.show()


def singleTeamPrediction(team,year):
    RS,RA,W,L = ReadBrefPage(year,team)
    RS_81 = getFirstN(RS,81)
    RA_81 = getFirstN(RA,81)
    W_81 = 0
    for i in range(81):
        if (RS_81[i] > RA_81[i]):
            W_81 += 1
    half_win_per = W_81/81
    full_win_per = W/162
    ROS_win_per = calcNewWinPer(RS_81,RA_81)
    pred_win_per = (half_win_per+ROS_win_per)/2

    pyth_win_per = (sum(RS_81)*sum(RS_81))/((sum(RS_81)*sum(RS_81)) + (sum(RA_81)*sum(RA_81)))
    pyth_win_proj = (half_win_per+pyth_win_per)/2
    return full_win_per, pred_win_per, pyth_win_proj

def singleTeamPrediction2(team,year):
    RS,RA,W,L = ReadBrefPage(year,team)

    full_win_per = W/162
    pred_win_per = calcNewWinPer(RS,RA)

    pyth_win_per = (sum(RS)*sum(RS))/((sum(RS)*sum(RS)) + (sum(RA)*sum(RA)))

    return full_win_per, pred_win_per, pyth_win_per

def newPerfMetric():
    cache.enable()

    league = ["NYY","BOS","TBR","BAL","TOR",
              "MIN","DET","CHW","KCR","CLE",
              "OAK","LAA","HOU","TEX","SEA",
              "LAD","SFG","ARI","SDP","COL",
              "CIN","STL","MIL","CHC","PIT",
              "WSN","PHI","ATL","NYM","MIA"]
    trueWinPer = []
    denisWinPer = []
    pythWinPer = []
    years = [2018,2019,2021,2022,2023]
    for year in years:
        for team in league:
            R1,R2,R3 = singleTeamPrediction2(team,year)
            trueWinPer.append(R1)
            denisWinPer.append(R2)
            pythWinPer.append(R3)
    
    # plotting
    x = [0.25,0.4,0.5,0.6,0.75]
    print("As a performance metric:\n")
    print("My R2 score: " + str(scikit.r2_score(trueWinPer,denisWinPer)))
    print("Their R2 score: " + str(scikit.r2_score(trueWinPer,pythWinPer)))
    plt.figure()
    plt.clf()
    plt.plot(trueWinPer,denisWinPer,"bo",label="My Way")
    plt.plot(trueWinPer,pythWinPer,"ro",label = "Pyth Way")
    plt.legend(loc = "upper right")
    plt.plot(x,x,"-")
    plt.show()


def main():
    newPred()
    newPerfMetric()


main()