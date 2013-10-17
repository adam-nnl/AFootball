"""
Use nflgame api to pull out and compile stats. Export to .csv ready to be used with Erudite
"""
from decimal import Decimal, ROUND_DOWN
import nflgame
import csv


print 'nflgame API loaded and updated'
week = raw_input('What week of the season, 1-17?: ')
filename = 'nfl_weeklystats_week' + str(week) + '.csv'
f = open(filename,'a')
numGames = raw_input('Enter the number of games to gather data for: ')
f.write(numGames + ',12\n')
for i in range(int(numGames)):
        awayTeam = raw_input('Enter the AWAY team: ').upper()
        homeTeam = raw_input('Enter the HOME team: ').upper()
        HT_AVG = nflgame.games_gen(2013, home=homeTeam, away=homeTeam, kind="REG") #get all games played by HOME team of present game before current week
        #compile average stats for for HOME team: YPG, PPG, YPGA, PPGA, TOpm, QB rating
        HT_YPG = 0
        HT_PPG = 0
        HT_YPGA = 0
        HT_PPGA = 0
        HT_TOpm = 0
        HT_QByds = 0
        HT_QBatt = 0
        HT_QBcomp = 0
        HT_QBtd = 0
        HT_QBint = 0
        HT_QBR = 0
        HT_WL = 0
        count = 0
        for h in HT_AVG:
                if h.home==homeTeam:
                        HT_YPG += h.stats_home.total_yds
                        HT_PPG += h.score_home
                        HT_TOpm = h.stats_away.turnovers - h.stats_home.turnovers
                        HT_YPGA += h.stats_away.total_yds
                        HT_PPGA += h.score_away
                        qb = h.players.passing().filter(home=True, passing_att=lambda x: x >= 10)
                        for p in qb:
                                HT_QByds += p.passing_yds
                                HT_QBatt += p.passing_att
                                HT_QBcomp += p.passing_cmp
                                HT_QBtd += p.passing_tds
                                HT_QBint += p.passing_ints
                        count += 1
                else:
                        HT_YPG += h.stats_away.total_yds
                        HT_PPG += h.score_away
                        HT_TOpm = h.stats_home.turnovers - h.stats_away.turnovers                       
                        HT_YPGA += h.stats_home.total_yds
                        HT_PPGA += h.score_home
                        qb = h.players.passing().filter(home=False, passing_att=lambda x: x >= 10)
                        for p in qb:
                                HT_QByds += p.passing_yds
                                HT_QBatt += p.passing_att
                                HT_QBcomp += p.passing_cmp
                                HT_QBtd += p.passing_tds
                                HT_QBint += p.passing_ints                        
                        count += 1                        
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
        AT_TOpm = 0
        AT_QByds = 0
        AT_QBatt = 0
        AT_QBcomp = 0
        AT_QBtd = 0
        AT_QBint = 0
        AT_QBR = 0
        AT_WL = 0
        count = 0
        for a in AT_AVG:
                if a.home==awayTeam:
                        AT_YPG += a.stats_home.total_yds
                        AT_PPG += a.score_home
                        AT_TOpm = a.stats_away.turnovers - a.stats_home.turnovers
                        AT_YPGA += a.stats_away.total_yds
                        AT_PPGA += a.score_away
                        qb = a.players.passing().filter(home=True, passing_att=lambda x: x >= 10)
                        for p in qb:
                                AT_QByds += p.passing_yds
                                AT_QBatt += p.passing_att
                                AT_QBcomp += p.passing_cmp
                                AT_QBtd += p.passing_tds
                                AT_QBint += p.passing_ints
                        count += 1
                else:
                        AT_YPG += a.stats_away.total_yds
                        AT_PPG += a.score_away
                        AT_TOpm = a.stats_home.turnovers - a.stats_away.turnovers                       
                        AT_YPGA += a.stats_home.total_yds
                        AT_PPGA += a.score_home
                        qb = a.players.passing().filter(home=False, passing_att=lambda x: x >= 10)
                        for p in qb:
                                AT_QByds += p.passing_yds
                                AT_QBatt += p.passing_att
                                AT_QBcomp += p.passing_cmp
                                AT_QBtd += p.passing_tds
                                AT_QBint += p.passing_ints                        
                        count += 1                        
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
        print homeTeam + ' TO +/-: ' + str(HT_TOpm) + '\t' + awayTeam + ' TO +/-: ' + str(AT_TOpm)
        print homeTeam + ' YPG-A: ' + str(HT_YPGA) + '\t' + awayTeam + ' YPG-A: ' + str(AT_YPGA)
        print homeTeam + ' PPG-A: ' + str(HT_PPGA) + '\t' + awayTeam + ' PPG-A: ' + str(AT_PPGA)
        print homeTeam + ' QBR: ' + str(HT_QBR) + '\t' + awayTeam + ' QBR: ' + str(AT_QBR)
        print '-----------------------------------------------------\n'
        print 'Writing data to file...'
        f.write(homeTeam + '(HOME)' + ' vs. ' + awayTeam + '(AWAY)\n')
        f.write(str(HT_YPG/Decimal(1000))+',' + str(HT_YPGA/Decimal(1000))+',' + str(HT_TOpm/Decimal(10))+',' + str(HT_QBR/Decimal(100))+',' + str(HT_PPG/Decimal(100))+ ','+ str(HT_PPGA/Decimal(100))+',' + str(AT_YPG/Decimal(1000))+ ','+ str(AT_YPGA/Decimal(1000))+',' + str(AT_TOpm/Decimal(10))+',' + str(AT_QBR/Decimal(100))+',' + str(AT_PPG/Decimal(100)) + ','+ str(AT_PPGA/Decimal(100))+ '\n')
print 'Done Compiling weekly game data...'
print 'Done exporting to .csv file...'
f.close()
print 'All done.'
