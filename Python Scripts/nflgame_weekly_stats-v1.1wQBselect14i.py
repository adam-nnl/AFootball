"""
Use nflgame api to pull out and compile stats. Export to .csv ready to be used with Erudite
"""
from decimal import Decimal, ROUND_DOWN
import nflgame
import csv
import itertools


print 'nflgame API loaded and updated'
week = raw_input('What week of the season, 1-17?: ')
filename = 'nfl_weeklystats_week' + str(week) + '.csv'
f = open(filename,'a')
numGames = raw_input('Enter the number of games to gather data for: ')
f.write(numGames + ',14\n')
for i in range(int(numGames)):
        awayTeam = raw_input('Enter the AWAY team: ').upper()
        homeTeam = raw_input('Enter the HOME team: ').upper()
        HT_AVG1 = nflgame.games_gen(2013, home=homeTeam, away=homeTeam, kind="REG")
        QBs = nflgame.combine(HT_AVG1)
        print 'Which HOME QB statistics to use?'
        for p in QBs.passing().sort("passing_att"):
                print p
        QBname = raw_input('Enter the quarterback name as it is written: ')        
        QB_AVG = nflgame.games_gen(2013, kind="REG")
        playerStats = nflgame.combine(QB_AVG)
        QBplayer = playerStats.name(QBname)
        AT_AVG1 = nflgame.games_gen(2013, home=awayTeam, away=awayTeam kind="REG")
        aQBs = nflgame.combine(AT_AVG1)
        print 'Which AWAY QB statistics to use?'
        for p in aQBs.passing().sort("passing_att"):
                print p
        aQBname = raw_input('Enter the quarterback name as it is written: ')        
        aQB_AVG = nflgame.games_gen(2013, kind="REG")
        playerStats = nflgame.combine(aQB_AVG)
        aQBplayer = playerStats.name(aQBname)        
        HT_AVG = nflgame.games_gen(2013, home=homeTeam, away=homeTeam, kind="REG")
        HT_YPG = 0
        HT_PPG = 0
        HT_YPGA = 0
        HT_PPGA = 0
        #HT_TOpm = 0
        HT_TO = 0
        HT_TA = 0
        HT_QByds = QBplayer.passing_yds
        HT_QBatt = QBplayer.passing_att
        HT_QBcomp = QBplayer.passing_cmp
        HT_QBtd = QBplayer.passing_tds
        HT_QBint = QBplayer.passing_ints          
        HT_QBR = 0
        HT_WL = 0
        count = 0
        for h in HT_AVG:
                count += 1 
                if h.home==homeTeam:
                        HT_YPG += h.stats_home.total_yds
                        HT_PPG += h.score_home
                        HT_TO += h.stats_home.turnovers
                        HT_TA += h.stats_away.turnovers
                        HT_YPGA += h.stats_away.total_yds
                        HT_PPGA += h.score_away
                else:
                        HT_YPG += h.stats_away.total_yds
                        HT_PPG += h.score_away
                        HT_TO += h.stats_away.turnovers
                        HT_TA += h.stats_home.turnovers
                        HT_YPGA += h.stats_home.total_yds
                        HT_PPGA += h.score_home                       
        HT_TO = HT_TO / Decimal(count)
        HT_TA = HT_TA / Decimal(count)
        HT_YPG = HT_YPG / count
        HT_PPG = HT_PPG / Decimal(count)
        HT_PPG = Decimal(str(HT_PPG)).quantize(Decimal('.01'), rounding=ROUND_DOWN)
        HT_YPGA = HT_YPGA / count
        HT_PPGA = HT_PPGA / Decimal(count)
        HT_PPGA = Decimal(str(HT_PPGA)).quantize(Decimal('.01'), rounding=ROUND_DOWN)
        HT_QBR = Decimal(HT_QBcomp) / Decimal(HT_QBatt)
        HT_QBR = HT_QBR * Decimal(100)
        HT_QBR = (HT_QBR - 30) * Decimal(0.05)
        HT_QBR += ((HT_QByds / HT_QBatt) - 3) * Decimal(0.25)
        HT_QBR += (HT_QBtd / HT_QBatt) * Decimal(0.2)
        HT_QBR += Decimal(2.375) - ((HT_QBint / HT_QBatt) * Decimal(0.25))
        HT_QBR = HT_QBR / Decimal(6)
        HT_QBR = HT_QBR * Decimal(100)
        HT_QBR = Decimal(str(HT_QBR)).quantize(Decimal('.01'), rounding=ROUND_DOWN)
        #############        
        AT_AVG = nflgame.games_gen(2013, home=awayTeam, away=awayTeam, kind="REG") #get all games played by AWAY team of present game before current week
        #compile average stats for for HOME team: YPG, PPG, YPGA, PPGA, TOpm, QB rating
        AT_YPG = 0
        AT_PPG = 0
        AT_YPGA = 0
        AT_PPGA = 0
        #AT_TOpm = 0
        AT_TO = 0
        AT_TA = 0
        AT_QByds = aQBplayer.passing_yds
        AT_QBatt = aQBplayer.passing_att
        AT_QBcomp = aQBplayer.passing_cmp
        AT_QBtd = aQBplayer.passing_tds
        AT_QBint = aQBplayer.passing_ints
        AT_QBR = 0
        AT_WL = 0
        count = 0
        for a in AT_AVG:
                count += 1
                if a.home==awayTeam:
                        AT_YPG += a.stats_home.total_yds
                        AT_PPG += a.score_home
                        #AT_TOpm = a.stats_away.turnovers - a.stats_home.turnovers
                        AT_TO += a.stats_home.turnovers
                        AT_TA += a.stats_away.turnovers
                        AT_YPGA += a.stats_away.total_yds
                        AT_PPGA += a.score_away
                else:
                        AT_YPG += a.stats_away.total_yds
                        AT_PPG += a.score_away
                        #AT_TOpm = a.stats_home.turnovers - a.stats_away.turnovers
                        AT_TO += a.stats_away.turnovers
                        AT_TA += a.stats_home.turnovers
                        AT_YPGA += a.stats_home.total_yds
                        AT_PPGA += a.score_home
        AT_TO = AT_TO / Decimal(count)
        AT_TA = AT_TA / Decimal(count)
        AT_YPG = AT_YPG / count
        AT_PPG = AT_PPG / Decimal(count)
        AT_PPG = Decimal(str(AT_PPG)).quantize(Decimal('.01'), rounding=ROUND_DOWN)
        AT_YPGA = AT_YPGA / count
        AT_PPGA = AT_PPGA / Decimal(count)
        AT_PPGA = Decimal(str(AT_PPGA)).quantize(Decimal('.01'), rounding=ROUND_DOWN)
        AT_QBR = Decimal(AT_QBcomp) / Decimal(AT_QBatt)
        AT_QBR = AT_QBR * Decimal(100)
        AT_QBR = (AT_QBR - 30) * Decimal(0.05)
        AT_QBR += ((AT_QByds / AT_QBatt) - 3) * Decimal(0.25)
        AT_QBR += (AT_QBtd / AT_QBatt) * Decimal(0.2)
        AT_QBR += Decimal(2.375) - ((AT_QBint / AT_QBatt) * Decimal(0.25))
        AT_QBR = AT_QBR / Decimal(6)
        AT_QBR = AT_QBR * Decimal(100)
        AT_QBR = Decimal(str(AT_QBR)).quantize(Decimal('.01'), rounding=ROUND_DOWN)
        #############
        #compile average stats for for AWAY team: YPG, PPG, YPGA, PPGA, TOpm, QB rating
        print '\nGame data for: ' + homeTeam + '(HOME)' + ' vs. ' + awayTeam + '(AWAY)'
        print '-----------------------------------------------------\n'
        print homeTeam + ' YPG: ' + str(HT_YPG) + '\t' + awayTeam + ' YPG: ' + str(AT_YPG)
        print homeTeam + ' PPG: ' + str(HT_PPG) + '\t' + awayTeam + ' PPG: ' + str(AT_PPG)
        #print homeTeam + ' TO +/-: ' + str(HT_TOpm) + '\t' + awayTeam + ' TO +/-: ' + str(AT_TOpm)
        print homeTeam + ' TOs: ' + str(HT_TO) + '\t' + awayTeam + ' TOs: ' + str(AT_TO)
        print homeTeam + ' TAs: ' + str(HT_TA) + '\t' + awayTeam + ' TAs: ' + str(AT_TA)
        print homeTeam + ' YPG-A: ' + str(HT_YPGA) + '\t' + awayTeam + ' YPG-A: ' + str(AT_YPGA)
        print homeTeam + ' PPG-A: ' + str(HT_PPGA) + '\t' + awayTeam + ' PPG-A: ' + str(AT_PPGA)
        print homeTeam + ' QBR: ' + str(HT_QBR) + '\t' + awayTeam + ' QBR: ' + str(AT_QBR)
        print '-----------------------------------------------------\n'
        print 'Writing data to file...'
        f.write(homeTeam + '(HOME)' + ' vs. ' + awayTeam + '(AWAY)\n')
        f.write(str(HT_YPG/Decimal(1000))+',' + str(HT_YPGA/Decimal(1000))+',' + str(HT_TO/Decimal(10))+',' + str(HT_TA/Decimal(10))+',' + str(HT_QBR/Decimal(100))+',' + str(HT_PPG/Decimal(100))+ ','+ str(HT_PPGA/Decimal(100))+',' + str(AT_YPG/Decimal(1000))+ ','+ str(AT_YPGA/Decimal(1000))+',' + str(AT_TO/Decimal(10))+',' + str(AT_TA/Decimal(10))+',' + str(AT_QBR/Decimal(100))+',' + str(AT_PPG/Decimal(100)) + ','+ str(AT_PPGA/Decimal(100))+ '\n')
print 'Done Compiling weekly game data...'
print 'Done exporting to .csv file...'
f.close()
print 'All done.'
