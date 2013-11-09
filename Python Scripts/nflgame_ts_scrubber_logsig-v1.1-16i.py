"""
Use nflgame api to pull out and compile stats. Export to .csv ready to be used with Erudite
"""
from decimal import Decimal, ROUND_DOWN
import nflgame
import csv
import sys
import fileinput

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes":True,   "y":True,  "ye":True,
             "no":False,     "n":False}
    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "\
                             "(or 'y' or 'n').\n")

print 'nflgame API loaded'
print 'Compiling training sets...'
print 'Compiling traing set for 2009 NFL season...'
season2009 = nflgame.games_gen(2009, kind="REG")
f = open('nfl2009ts_logsig_scrubbed-14i-v1.1.csv','w')
result = ''
exampleCount = 0
for g in season2009:
        HT_AVG = nflgame.games_gen(2009, home=g.home, away=g.home, kind="REG") #get all games played by HOME team of present game before current week
        #compile average stats for for HOME team: YPG, PPG, YPGA, PPGA, TOpm, QB rating
        HT_YPG = 0
        HT_TOP = 0
        HT_PPG = 0
        HT_YPGA = 0
        HT_PPGA = 0
        #HT_TOpm = 0
        HT_TO = 0
        HT_TA = 0
        HT_QByds = 0
        HT_QBatt = 0
        HT_QBcomp = 0
        HT_QBtd = 0
        HT_QBint = 0
        HT_QBR = 0
        HT_WL = 0
        count = 0
        for h in HT_AVG:
                if h.home==g.home:
                        HT_YPG += h.stats_home.total_yds
                        HT_PPG += h.score_home
                        #HT_TOpm = h.stats_away.turnovers - h.stats_home.turnovers
                        HT_TO += h.stats_home.turnovers
                        HT_TA += h.stats_away.turnovers
                        HT_TOP += getattr(h.stats_home.pos_time, 'total_seconds')
                        HT_YPGA += h.stats_away.total_yds
                        HT_PPGA += h.score_away
                        qb = h.players.passing().filter(home=True).sort('passing_att').limit(1)
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
                        #HT_TOpm = h.stats_home.turnovers - h.stats_away.turnovers
                        HT_TO += h.stats_away.turnovers
                        HT_TA += h.stats_home.turnovers
                        HT_TOP += int(h.stats_away.pos_time)
                        HT_YPGA += h.stats_home.total_yds
                        HT_PPGA += h.score_home
                        qb = h.players.passing().filter(home=False).sort('passing_att').limit(1)
                        for p in qb:
                                HT_QByds += p.passing_yds
                                HT_QBatt += p.passing_att
                                HT_QBcomp += p.passing_cmp
                                HT_QBtd += p.passing_tds
                                HT_QBint += p.passing_ints                        
                        count += 1
        HT_TO = HT_TO / Decimal(count)
        HT_TA = HT_TA / Decimal(count)
        HT_TOP = HT_TOP / Decimal(count)
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
        if g.score_home > g.score_away:
                HT_WL = 1
        elif g.score_home < g.score_away:
                HT_WL = 0
        #############
        AT_AVG = nflgame.games_gen(2009, home=g.away, away=g.away, kind="REG") #get all games played by AWAY team of present game before current week
        #compile average stats for for HOME team: YPG, PPG, YPGA, PPGA, TOpm, QB rating
        AT_YPG = 0
        AT_PPG = 0
        AT_YPGA = 0
        AT_PPGA = 0
        #AT_TOpm = 0
        AT_TO = 0
        AT_TA = 0
        AT_TOP = 0
        AT_QByds = 0
        AT_QBatt = 0
        AT_QBcomp = 0
        AT_QBtd = 0
        AT_QBint = 0
        AT_QBR = 0
        AT_WL = 0
        count = 0
        for a in AT_AVG:
                if a.home==g.away:
                        AT_YPG += a.stats_home.total_yds
                        AT_PPG += a.score_home
                        #AT_TOpm = a.stats_away.turnovers - a.stats_home.turnovers
                        AT_TO += a.stats_home.turnovers
                        AT_TA += a.stats_away.turnovers
                        AT_TOP += int(a.stats_home.pos_time)
                        AT_YPGA += a.stats_away.total_yds
                        AT_PPGA += a.score_away
                        qb = a.players.passing().filter(home=True).sort('passing_att').limit(1)
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
                        #AT_TOpm = a.stats_home.turnovers - a.stats_away.turnovers
                        AT_TO += a.stats_home.turnovers
                        AT_TA += a.stats_away.turnovers
                        AT_TOP += int(a.stats_away.pos_time)
                        AT_YPGA += a.stats_home.total_yds
                        AT_PPGA += a.score_home
                        qb = a.players.passing().filter(home=False).sort('passing_att').limit(1)
                        for p in qb:
                                AT_QByds += p.passing_yds
                                AT_QBatt += p.passing_att
                                AT_QBcomp += p.passing_cmp
                                AT_QBtd += p.passing_tds
                                AT_QBint += p.passing_ints                        
                        count += 1
        AT_TO = AT_TO / Decimal(count)
        AT_TA = AT_TA / Decimal(count)
        AT_TOP = AT_TOP / Decimal(count)
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
        if g.score_away > g.score_home:
                AT_WL = 1
        elif g.score_away < g.score_home:
                AT_WL = 0
        #############
        #compile average stats for for AWAY team: YPG, PPG, YPGA, PPGA, TOpm, QB rating
        print 'Game data for: ' + g.home + '(h)' + ' vs. ' + g.away + '(a)'
        print '-----------------------------------------------------\n'
        if HT_YPG > AT_YPG:
                print g.home + ' ***YPG: ' + str(HT_YPG) + '\t' + g.away + ' YPG: ' + str(AT_YPG)
        elif AT_YPG > HT_YPG:
                print g.home + ' YPG: ' + str(HT_YPG) + '\t' + g.away + ' ***YPG: ' + str(AT_YPG)
        if HT_PPG > AT_PPG:
                print g.home + ' ***PPG: ' + str(HT_PPG) + '\t' + g.away + ' PPG: ' + str(AT_PPG)
        elif AT_PPG > HT_PPG:
                print g.home + ' PPG: ' + str(HT_PPG) + '\t' + g.away + ' ***PPG: ' + str(AT_PPG)
        #if HT_TOpm > AT_TOpm:
        #        print g.home + ' ***TO +/-: ' + str(HT_TOpm) + '\t' + g.away + ' TO +/-: ' + str(AT_TOpm)
        #elif AT_TOpm > HT_TOpm:
        #        print g.home + ' TO +/-: ' + str(HT_TOpm) + '\t' + g.away + ' ***TO +/-: ' + str(AT_TOpm)
        if HT_TO < AT_TO:
                print g.home + ' ***TOpg: ' + str(HT_TO) + '\t' + g.away + ' TOpg: ' + str(AT_TO)
        elif AT_TO < HT_TO:
                print g.home + ' TOpg: ' + str(HT_TO) + '\t' + g.away + ' ***TOpg: ' + str(AT_TO)
        if HT_TA > AT_TA:
                print g.home + ' ***TApg: ' + str(HT_TA) + '\t' + g.away + ' TApg: ' + str(AT_TA)
        elif AT_TA > HT_TA:
                print g.home + ' TApg: ' + str(HT_TA) + '\t' + g.away + ' ***TApg: ' + str(AT_TA)
        if HT_TOP > AT_TOP:
                print g.home + ' ***Avg. ToP: ' + str(HT_TOP) + '\t' + g.away + ' Avg. ToP: ' + str(AT_TOP)
        elif AT_TOP > HT_TOP:
                print g.home + ' Avg. ToP: ' + str(HT_TOP) + '\t' + g.away + ' ***Avg. ToP: ' + str(AT_TOP)                
        if HT_YPGA < AT_YPGA:
                print g.home + ' ***YPG-A: ' + str(HT_YPGA) + '\t' + g.away + ' YPG-A: ' + str(AT_YPGA)
        elif AT_YPGA < HT_YPGA:
                print g.home + ' YPG-A: ' + str(HT_YPGA) + '\t' + g.away + ' ***YPG-A: ' + str(AT_YPGA)
        if HT_PPGA < AT_PPGA:
                print g.home + ' ***PPG-A: ' + str(HT_PPGA) + '\t' + g.away + ' PPG-A: ' + str(AT_PPGA)
        elif AT_PPGA < HT_PPGA:
                print g.home + ' PPG-A: ' + str(HT_PPGA) + '\t' + g.away + ' ***PPG-A: ' + str(AT_PPGA)
        if HT_QBR > AT_QBR:
                print g.home + ' ***QBR: ' + str(HT_QBR) + '\t' + g.away + ' QBR: ' + str(AT_QBR)
        elif AT_QBR > HT_QBR:
                print g.home + ' QBR: ' + str(HT_QBR) + '\t' + g.away + ' ***QBR: ' + str(AT_QBR)
        if HT_WL > AT_WL:
                print '***HOME W/L: ' + str(HT_WL) + '\t' + 'AWAY W/L: ' + str(AT_WL)
        elif AT_WL > HT_WL:
                print 'HOME W/L: ' + str(HT_WL) + '\t' + '***AWAY W/L: ' + str(AT_WL)        
        print 'HOME FINAL: ' + str(g.score_home) + '\t' + 'AWAY FINAL: ' + str(g.score_away)        
        print '-----------------------------------------------------\n'
        choice = query_yes_no("Add game as example to training set?")
        if choice:
                result = str(result)+str(HT_YPG/Decimal(1000))+','+ str(HT_YPGA/Decimal(1000))+','+ str(HT_TO/Decimal(10))+','+ str(HT_TA/Decimal(10))+','+ str(HT_TOP/Decimal(10))+','+ str(HT_QBR/Decimal(100))+','+ str(HT_PPG/Decimal(100))+','+ str(HT_PPGA/Decimal(100))+','+ str(AT_YPG/Decimal(1000))+','+ str(AT_YPGA/Decimal(1000))+','+ str(AT_TO/Decimal(10))+','+ str(AT_TA/Decimal(10))+','+ str(AT_TOP/Decimal(10))+','+ str(AT_QBR/Decimal(100))+','+ str(AT_PPG/Decimal(100))+','+ str(AT_PPGA/Decimal(100))+'\n'
                result = str(result)+str(HT_WL)+','+ str(AT_WL)+'\n'
                exampleCount += 1
TSheader = str(exampleCount)+',14,2\n'     
result = str(TSheader) + str(result)
f.write(result)
print 'Done Compiling season data...'
print 'Done exporting to .csv file...'
f.close()
print 'Compiling traing set for 2010 NFL season...'
season2009 = nflgame.games_gen(2010, kind="REG")
f = open('nfl2010ts_logsig_scrubbed-14i-v1.1.csv','w')
result = ''
exampleCount = 0
for g in season2009:
        HT_AVG = nflgame.games_gen(2010, home=g.home, away=g.home, kind="REG") #get all games played by HOME team of present game before current week
        #compile average stats for for HOME team: YPG, PPG, YPGA, PPGA, TOpm, QB rating
        HT_YPG = 0
        HT_PPG = 0
        HT_YPGA = 0
        HT_PPGA = 0
        #HT_TOpm = 0
        HT_TO = 0
        HT_TA = 0
        HT_QByds = 0
        HT_QBatt = 0
        HT_QBcomp = 0
        HT_QBtd = 0
        HT_QBint = 0
        HT_QBR = 0
        HT_WL = 0
        count = 0
        for h in HT_AVG:
                if h.home==g.home:
                        HT_YPG += h.stats_home.total_yds
                        HT_PPG += h.score_home
                        #HT_TOpm = h.stats_away.turnovers - h.stats_home.turnovers
                        HT_TO += h.stats_home.turnovers
                        HT_TA += h.stats_away.turnovers
                        HT_YPGA += h.stats_away.total_yds
                        HT_PPGA += h.score_away
                        qb = h.players.passing().filter(home=True).sort('passing_att').limit(1)
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
                        #HT_TOpm = h.stats_home.turnovers - h.stats_away.turnovers
                        HT_TO += h.stats_away.turnovers
                        HT_TA += h.stats_home.turnovers
                        HT_YPGA += h.stats_home.total_yds
                        HT_PPGA += h.score_home
                        qb = h.players.passing().filter(home=False).sort('passing_att').limit(1)
                        for p in qb:
                                HT_QByds += p.passing_yds
                                HT_QBatt += p.passing_att
                                HT_QBcomp += p.passing_cmp
                                HT_QBtd += p.passing_tds
                                HT_QBint += p.passing_ints                        
                        count += 1
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
        if g.score_home > g.score_away:
                HT_WL = 1
        elif g.score_home < g.score_away:
                HT_WL = 0
        #############
        AT_AVG = nflgame.games_gen(2009, home=g.away, away=g.away, kind="REG") #get all games played by AWAY team of present game before current week
        #compile average stats for for HOME team: YPG, PPG, YPGA, PPGA, TOpm, QB rating
        AT_YPG = 0
        AT_PPG = 0
        AT_YPGA = 0
        AT_PPGA = 0
        #AT_TOpm = 0
        AT_TO = 0
        AT_TA = 0
        AT_QByds = 0
        AT_QBatt = 0
        AT_QBcomp = 0
        AT_QBtd = 0
        AT_QBint = 0
        AT_QBR = 0
        AT_WL = 0
        count = 0
        for a in AT_AVG:
                if a.home==g.away:
                        AT_YPG += a.stats_home.total_yds
                        AT_PPG += a.score_home
                        #AT_TOpm = a.stats_away.turnovers - a.stats_home.turnovers
                        AT_TO += a.stats_home.turnovers
                        AT_TA += a.stats_away.turnovers
                        AT_YPGA += a.stats_away.total_yds
                        AT_PPGA += a.score_away
                        qb = a.players.passing().filter(home=True).sort('passing_att').limit(1)
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
                        #AT_TOpm = a.stats_home.turnovers - a.stats_away.turnovers
                        AT_TO += a.stats_home.turnovers
                        AT_TA += a.stats_away.turnovers
                        AT_YPGA += a.stats_home.total_yds
                        AT_PPGA += a.score_home
                        qb = a.players.passing().filter(home=False).sort('passing_att').limit(1)
                        for p in qb:
                                AT_QByds += p.passing_yds
                                AT_QBatt += p.passing_att
                                AT_QBcomp += p.passing_cmp
                                AT_QBtd += p.passing_tds
                                AT_QBint += p.passing_ints                        
                        count += 1
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
        if g.score_away > g.score_home:
                AT_WL = 1
        elif g.score_away < g.score_home:
                AT_WL = 0
        #############
        #compile average stats for for AWAY team: YPG, PPG, YPGA, PPGA, TOpm, QB rating
        print 'Game data for: ' + g.home + '(h)' + ' vs. ' + g.away + '(a)'
        print '-----------------------------------------------------\n'
        if HT_YPG > AT_YPG:
                print g.home + ' ***YPG: ' + str(HT_YPG) + '\t' + g.away + ' YPG: ' + str(AT_YPG)
        elif AT_YPG > HT_YPG:
                print g.home + ' YPG: ' + str(HT_YPG) + '\t' + g.away + ' ***YPG: ' + str(AT_YPG)
        if HT_PPG > AT_PPG:
                print g.home + ' ***PPG: ' + str(HT_PPG) + '\t' + g.away + ' PPG: ' + str(AT_PPG)
        elif AT_PPG > HT_PPG:
                print g.home + ' PPG: ' + str(HT_PPG) + '\t' + g.away + ' ***PPG: ' + str(AT_PPG)
        #if HT_TOpm > AT_TOpm:
        #        print g.home + ' ***TO +/-: ' + str(HT_TOpm) + '\t' + g.away + ' TO +/-: ' + str(AT_TOpm)
        #elif AT_TOpm > HT_TOpm:
        #        print g.home + ' TO +/-: ' + str(HT_TOpm) + '\t' + g.away + ' ***TO +/-: ' + str(AT_TOpm)
        if HT_TO < AT_TO:
                print g.home + ' ***TOpg: ' + str(HT_TO) + '\t' + g.away + ' TOpg: ' + str(AT_TO)
        elif AT_TO < HT_TO:
                print g.home + ' TOpg: ' + str(HT_TO) + '\t' + g.away + ' ***TOpg: ' + str(AT_TO)
        if HT_TA > AT_TA:
                print g.home + ' ***TApg: ' + str(HT_TA) + '\t' + g.away + ' TApg: ' + str(AT_TA)
        elif AT_TA > HT_TA:
                print g.home + ' TApg: ' + str(HT_TA) + '\t' + g.away + ' ***TApg: ' + str(AT_TA)                
        if HT_YPGA < AT_YPGA:
                print g.home + ' ***YPG-A: ' + str(HT_YPGA) + '\t' + g.away + ' YPG-A: ' + str(AT_YPGA)
        elif AT_YPGA < HT_YPGA:
                print g.home + ' YPG-A: ' + str(HT_YPGA) + '\t' + g.away + ' ***YPG-A: ' + str(AT_YPGA)
        if HT_PPGA < AT_PPGA:
                print g.home + ' ***PPG-A: ' + str(HT_PPGA) + '\t' + g.away + ' PPG-A: ' + str(AT_PPGA)
        elif AT_PPGA < HT_PPGA:
                print g.home + ' PPG-A: ' + str(HT_PPGA) + '\t' + g.away + ' ***PPG-A: ' + str(AT_PPGA)
        if HT_QBR > AT_QBR:
                print g.home + ' ***QBR: ' + str(HT_QBR) + '\t' + g.away + ' QBR: ' + str(AT_QBR)
        elif AT_QBR > HT_QBR:
                print g.home + ' QBR: ' + str(HT_QBR) + '\t' + g.away + ' ***QBR: ' + str(AT_QBR)
        if HT_WL > AT_WL:
                print '***HOME W/L: ' + str(HT_WL) + '\t' + 'AWAY W/L: ' + str(AT_WL)
        elif AT_WL > HT_WL:
                print 'HOME W/L: ' + str(HT_WL) + '\t' + '***AWAY W/L: ' + str(AT_WL)        
        print 'HOME FINAL: ' + str(g.score_home) + '\t' + 'AWAY FINAL: ' + str(g.score_away)        
        print '-----------------------------------------------------\n'
        choice = query_yes_no("Add game as example to training set?")
        if choice:
                result = str(result)+str(HT_YPG/Decimal(1000))+','+ str(HT_YPGA/Decimal(1000))+','+ str(HT_TO/Decimal(10))+','+ str(HT_TA/Decimal(10))+','+ str(HT_QBR/Decimal(100))+','+ str(HT_PPG/Decimal(100))+','+ str(HT_PPGA/Decimal(100))+','+ str(AT_YPG/Decimal(1000))+','+ str(AT_YPGA/Decimal(1000))+','+ str(AT_TO/Decimal(10))+','+ str(AT_TA/Decimal(10))+','+ str(AT_QBR/Decimal(100))+','+ str(AT_PPG/Decimal(100))+','+ str(AT_PPGA/Decimal(100))+'\n'
                result = str(result)+str(HT_WL)+','+ str(AT_WL)+'\n'
                exampleCount += 1
TSheader = str(exampleCount)+',14,2\n'      
result = str(TSheader) + str(result)
f.write(result)
print 'Done Compiling season data...'
print 'Exporting to .csv file...'
print 'Compiling traing set for 2011 NFL season...'
season2009 = nflgame.games_gen(2011, kind="REG")
f = open('nfl2011ts_logsig_scrubbed-14i-v1.1.csv','w')
result = ''
exampleCount = 0
for g in season2009:
        HT_AVG = nflgame.games_gen(2011, home=g.home, away=g.home, kind="REG") #get all games played by HOME team of present game before current week
        #compile average stats for for HOME team: YPG, PPG, YPGA, PPGA, TOpm, QB rating
        HT_YPG = 0
        HT_PPG = 0
        HT_YPGA = 0
        HT_PPGA = 0
        #HT_TOpm = 0
        HT_TO = 0
        HT_TA = 0
        HT_QByds = 0
        HT_QBatt = 0
        HT_QBcomp = 0
        HT_QBtd = 0
        HT_QBint = 0
        HT_QBR = 0
        HT_WL = 0
        count = 0
        for h in HT_AVG:
                if h.home==g.home:
                        HT_YPG += h.stats_home.total_yds
                        HT_PPG += h.score_home
                        #HT_TOpm = h.stats_away.turnovers - h.stats_home.turnovers
                        HT_TO += h.stats_home.turnovers
                        HT_TA += h.stats_away.turnovers
                        HT_YPGA += h.stats_away.total_yds
                        HT_PPGA += h.score_away
                        qb = h.players.passing().filter(home=True).sort('passing_att').limit(1)
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
                        #HT_TOpm = h.stats_home.turnovers - h.stats_away.turnovers
                        HT_TO += h.stats_away.turnovers
                        HT_TA += h.stats_home.turnovers
                        HT_YPGA += h.stats_home.total_yds
                        HT_PPGA += h.score_home
                        qb = h.players.passing().filter(home=False).sort('passing_att').limit(1)
                        for p in qb:
                                HT_QByds += p.passing_yds
                                HT_QBatt += p.passing_att
                                HT_QBcomp += p.passing_cmp
                                HT_QBtd += p.passing_tds
                                HT_QBint += p.passing_ints                        
                        count += 1
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
        if g.score_home > g.score_away:
                HT_WL = 1
        elif g.score_home < g.score_away:
                HT_WL = 0
        #############
        AT_AVG = nflgame.games_gen(2009, home=g.away, away=g.away, kind="REG") #get all games played by AWAY team of present game before current week
        #compile average stats for for HOME team: YPG, PPG, YPGA, PPGA, TOpm, QB rating
        AT_YPG = 0
        AT_PPG = 0
        AT_YPGA = 0
        AT_PPGA = 0
        #AT_TOpm = 0
        AT_TO = 0
        AT_TA = 0
        AT_QByds = 0
        AT_QBatt = 0
        AT_QBcomp = 0
        AT_QBtd = 0
        AT_QBint = 0
        AT_QBR = 0
        AT_WL = 0
        count = 0
        for a in AT_AVG:
                if a.home==g.away:
                        AT_YPG += a.stats_home.total_yds
                        AT_PPG += a.score_home
                        #AT_TOpm = a.stats_away.turnovers - a.stats_home.turnovers
                        AT_TO += a.stats_home.turnovers
                        AT_TA += a.stats_away.turnovers
                        AT_YPGA += a.stats_away.total_yds
                        AT_PPGA += a.score_away
                        qb = a.players.passing().filter(home=True).sort('passing_att').limit(1)
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
                        #AT_TOpm = a.stats_home.turnovers - a.stats_away.turnovers
                        AT_TO += a.stats_home.turnovers
                        AT_TA += a.stats_away.turnovers
                        AT_YPGA += a.stats_home.total_yds
                        AT_PPGA += a.score_home
                        qb = a.players.passing().filter(home=False).sort('passing_att').limit(1)
                        for p in qb:
                                AT_QByds += p.passing_yds
                                AT_QBatt += p.passing_att
                                AT_QBcomp += p.passing_cmp
                                AT_QBtd += p.passing_tds
                                AT_QBint += p.passing_ints                        
                        count += 1
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
        if g.score_away > g.score_home:
                AT_WL = 1
        elif g.score_away < g.score_home:
                AT_WL = 0
        #############
        #compile average stats for for AWAY team: YPG, PPG, YPGA, PPGA, TOpm, QB rating
        print 'Game data for: ' + g.home + '(h)' + ' vs. ' + g.away + '(a)'
        print '-----------------------------------------------------\n'
        if HT_YPG > AT_YPG:
                print g.home + ' ***YPG: ' + str(HT_YPG) + '\t' + g.away + ' YPG: ' + str(AT_YPG)
        elif AT_YPG > HT_YPG:
                print g.home + ' YPG: ' + str(HT_YPG) + '\t' + g.away + ' ***YPG: ' + str(AT_YPG)
        if HT_PPG > AT_PPG:
                print g.home + ' ***PPG: ' + str(HT_PPG) + '\t' + g.away + ' PPG: ' + str(AT_PPG)
        elif AT_PPG > HT_PPG:
                print g.home + ' PPG: ' + str(HT_PPG) + '\t' + g.away + ' ***PPG: ' + str(AT_PPG)
        #if HT_TOpm > AT_TOpm:
        #        print g.home + ' ***TO +/-: ' + str(HT_TOpm) + '\t' + g.away + ' TO +/-: ' + str(AT_TOpm)
        #elif AT_TOpm > HT_TOpm:
        #        print g.home + ' TO +/-: ' + str(HT_TOpm) + '\t' + g.away + ' ***TO +/-: ' + str(AT_TOpm)
        if HT_TO < AT_TO:
                print g.home + ' ***TOpg: ' + str(HT_TO) + '\t' + g.away + ' TOpg: ' + str(AT_TO)
        elif AT_TO < HT_TO:
                print g.home + ' TOpg: ' + str(HT_TO) + '\t' + g.away + ' ***TOpg: ' + str(AT_TO)
        if HT_TA > AT_TA:
                print g.home + ' ***TApg: ' + str(HT_TA) + '\t' + g.away + ' TApg: ' + str(AT_TA)
        elif AT_TA > HT_TA:
                print g.home + ' TApg: ' + str(HT_TA) + '\t' + g.away + ' ***TApg: ' + str(AT_TA)                
        if HT_YPGA < AT_YPGA:
                print g.home + ' ***YPG-A: ' + str(HT_YPGA) + '\t' + g.away + ' YPG-A: ' + str(AT_YPGA)
        elif AT_YPGA < HT_YPGA:
                print g.home + ' YPG-A: ' + str(HT_YPGA) + '\t' + g.away + ' ***YPG-A: ' + str(AT_YPGA)
        if HT_PPGA < AT_PPGA:
                print g.home + ' ***PPG-A: ' + str(HT_PPGA) + '\t' + g.away + ' PPG-A: ' + str(AT_PPGA)
        elif AT_PPGA < HT_PPGA:
                print g.home + ' PPG-A: ' + str(HT_PPGA) + '\t' + g.away + ' ***PPG-A: ' + str(AT_PPGA)
        if HT_QBR > AT_QBR:
                print g.home + ' ***QBR: ' + str(HT_QBR) + '\t' + g.away + ' QBR: ' + str(AT_QBR)
        elif AT_QBR > HT_QBR:
                print g.home + ' QBR: ' + str(HT_QBR) + '\t' + g.away + ' ***QBR: ' + str(AT_QBR)
        if HT_WL > AT_WL:
                print '***HOME W/L: ' + str(HT_WL) + '\t' + 'AWAY W/L: ' + str(AT_WL)
        elif AT_WL > HT_WL:
                print 'HOME W/L: ' + str(HT_WL) + '\t' + '***AWAY W/L: ' + str(AT_WL)        
        print 'HOME FINAL: ' + str(g.score_home) + '\t' + 'AWAY FINAL: ' + str(g.score_away)        
        print '-----------------------------------------------------\n'
        choice = query_yes_no("Add game as example to training set?")
        if choice:
                result = str(result)+str(HT_YPG/Decimal(1000))+','+ str(HT_YPGA/Decimal(1000))+','+ str(HT_TO/Decimal(10))+','+ str(HT_TA/Decimal(10))+','+ str(HT_QBR/Decimal(100))+','+ str(HT_PPG/Decimal(100))+','+ str(HT_PPGA/Decimal(100))+','+ str(AT_YPG/Decimal(1000))+','+ str(AT_YPGA/Decimal(1000))+','+ str(AT_TO/Decimal(10))+','+ str(AT_TA/Decimal(10))+','+ str(AT_QBR/Decimal(100))+','+ str(AT_PPG/Decimal(100))+','+ str(AT_PPGA/Decimal(100))+'\n'
                result = str(result)+str(HT_WL)+','+ str(AT_WL)+'\n'
                exampleCount += 1
TSheader = str(exampleCount)+',14,2\n'     
result = str(TSheader) + str(result)
f.write(result)
print 'Done Compiling season data...'
print 'Exporting to .csv file...'
print 'Compiling traing set for 2012 NFL season...'
season2009 = nflgame.games_gen(2012, kind="REG")
f = open('nfl2012ts_logsig_scrubbed-14i-v1.1.csv','w')
result = ''
exampleCount = 0
for g in season2009:
        HT_AVG = nflgame.games_gen(2012, home=g.home, away=g.home, kind="REG") #get all games played by HOME team of present game before current week
        #compile average stats for for HOME team: YPG, PPG, YPGA, PPGA, TOpm, QB rating
        HT_YPG = 0
        HT_PPG = 0
        HT_YPGA = 0
        HT_PPGA = 0
        #HT_TOpm = 0
        HT_TO = 0
        HT_TA = 0
        HT_QByds = 0
        HT_QBatt = 0
        HT_QBcomp = 0
        HT_QBtd = 0
        HT_QBint = 0
        HT_QBR = 0
        HT_WL = 0
        count = 0
        for h in HT_AVG:
                if h.home==g.home:
                        HT_YPG += h.stats_home.total_yds
                        HT_PPG += h.score_home
                        #HT_TOpm = h.stats_away.turnovers - h.stats_home.turnovers
                        HT_TO += h.stats_home.turnovers
                        HT_TA += h.stats_away.turnovers
                        HT_YPGA += h.stats_away.total_yds
                        HT_PPGA += h.score_away
                        qb = h.players.passing().filter(home=True).sort('passing_att').limit(1)
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
                        #HT_TOpm = h.stats_home.turnovers - h.stats_away.turnovers
                        HT_TO += h.stats_away.turnovers
                        HT_TA += h.stats_home.turnovers
                        HT_YPGA += h.stats_home.total_yds
                        HT_PPGA += h.score_home
                        qb = h.players.passing().filter(home=False).sort('passing_att').limit(1)
                        for p in qb:
                                HT_QByds += p.passing_yds
                                HT_QBatt += p.passing_att
                                HT_QBcomp += p.passing_cmp
                                HT_QBtd += p.passing_tds
                                HT_QBint += p.passing_ints                        
                        count += 1
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
        if g.score_home > g.score_away:
                HT_WL = 1
        elif g.score_home < g.score_away:
                HT_WL = 0
        #############
        AT_AVG = nflgame.games_gen(2009, home=g.away, away=g.away, kind="REG") #get all games played by AWAY team of present game before current week
        #compile average stats for for HOME team: YPG, PPG, YPGA, PPGA, TOpm, QB rating
        AT_YPG = 0
        AT_PPG = 0
        AT_YPGA = 0
        AT_PPGA = 0
        #AT_TOpm = 0
        AT_TO = 0
        AT_TA = 0
        AT_QByds = 0
        AT_QBatt = 0
        AT_QBcomp = 0
        AT_QBtd = 0
        AT_QBint = 0
        AT_QBR = 0
        AT_WL = 0
        count = 0
        for a in AT_AVG:
                if a.home==g.away:
                        AT_YPG += a.stats_home.total_yds
                        AT_PPG += a.score_home
                        #AT_TOpm = a.stats_away.turnovers - a.stats_home.turnovers
                        AT_TO += a.stats_home.turnovers
                        AT_TA += a.stats_away.turnovers
                        AT_YPGA += a.stats_away.total_yds
                        AT_PPGA += a.score_away
                        qb = a.players.passing().filter(home=True).sort('passing_att').limit(1)
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
                        #AT_TOpm = a.stats_home.turnovers - a.stats_away.turnovers
                        AT_TO += a.stats_home.turnovers
                        AT_TA += a.stats_away.turnovers
                        AT_YPGA += a.stats_home.total_yds
                        AT_PPGA += a.score_home
                        qb = a.players.passing().filter(home=False).sort('passing_att').limit(1)
                        for p in qb:
                                AT_QByds += p.passing_yds
                                AT_QBatt += p.passing_att
                                AT_QBcomp += p.passing_cmp
                                AT_QBtd += p.passing_tds
                                AT_QBint += p.passing_ints                        
                        count += 1
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
        if g.score_away > g.score_home:
                AT_WL = 1
        elif g.score_away < g.score_home:
                AT_WL = 0
        #############
        #compile average stats for for AWAY team: YPG, PPG, YPGA, PPGA, TOpm, QB rating
        print 'Game data for: ' + g.home + '(h)' + ' vs. ' + g.away + '(a)'
        print '-----------------------------------------------------\n'
        if HT_YPG > AT_YPG:
                print g.home + ' ***YPG: ' + str(HT_YPG) + '\t' + g.away + ' YPG: ' + str(AT_YPG)
        elif AT_YPG > HT_YPG:
                print g.home + ' YPG: ' + str(HT_YPG) + '\t' + g.away + ' ***YPG: ' + str(AT_YPG)
        if HT_PPG > AT_PPG:
                print g.home + ' ***PPG: ' + str(HT_PPG) + '\t' + g.away + ' PPG: ' + str(AT_PPG)
        elif AT_PPG > HT_PPG:
                print g.home + ' PPG: ' + str(HT_PPG) + '\t' + g.away + ' ***PPG: ' + str(AT_PPG)
        #if HT_TOpm > AT_TOpm:
        #        print g.home + ' ***TO +/-: ' + str(HT_TOpm) + '\t' + g.away + ' TO +/-: ' + str(AT_TOpm)
        #elif AT_TOpm > HT_TOpm:
        #        print g.home + ' TO +/-: ' + str(HT_TOpm) + '\t' + g.away + ' ***TO +/-: ' + str(AT_TOpm)
        if HT_TO < AT_TO:
                print g.home + ' ***TOpg: ' + str(HT_TO) + '\t' + g.away + ' TOpg: ' + str(AT_TO)
        elif AT_TO < HT_TO:
                print g.home + ' TOpg: ' + str(HT_TO) + '\t' + g.away + ' ***TOpg: ' + str(AT_TO)
        if HT_TA > AT_TA:
                print g.home + ' ***TApg: ' + str(HT_TA) + '\t' + g.away + ' TApg: ' + str(AT_TA)
        elif AT_TA > HT_TA:
                print g.home + ' TApg: ' + str(HT_TA) + '\t' + g.away + ' ***TApg: ' + str(AT_TA)                
        if HT_YPGA < AT_YPGA:
                print g.home + ' ***YPG-A: ' + str(HT_YPGA) + '\t' + g.away + ' YPG-A: ' + str(AT_YPGA)
        elif AT_YPGA < HT_YPGA:
                print g.home + ' YPG-A: ' + str(HT_YPGA) + '\t' + g.away + ' ***YPG-A: ' + str(AT_YPGA)
        if HT_PPGA < AT_PPGA:
                print g.home + ' ***PPG-A: ' + str(HT_PPGA) + '\t' + g.away + ' PPG-A: ' + str(AT_PPGA)
        elif AT_PPGA < HT_PPGA:
                print g.home + ' PPG-A: ' + str(HT_PPGA) + '\t' + g.away + ' ***PPG-A: ' + str(AT_PPGA)
        if HT_QBR > AT_QBR:
                print g.home + ' ***QBR: ' + str(HT_QBR) + '\t' + g.away + ' QBR: ' + str(AT_QBR)
        elif AT_QBR > HT_QBR:
                print g.home + ' QBR: ' + str(HT_QBR) + '\t' + g.away + ' ***QBR: ' + str(AT_QBR)
        if HT_WL > AT_WL:
                print '***HOME W/L: ' + str(HT_WL) + '\t' + 'AWAY W/L: ' + str(AT_WL)
        elif AT_WL > HT_WL:
                print 'HOME W/L: ' + str(HT_WL) + '\t' + '***AWAY W/L: ' + str(AT_WL)        
        print 'HOME FINAL: ' + str(g.score_home) + '\t' + 'AWAY FINAL: ' + str(g.score_away)        
        print '-----------------------------------------------------\n'
        choice = query_yes_no("Add game as example to training set?")
        if choice:
                result = str(result)+str(HT_YPG/Decimal(1000))+','+ str(HT_YPGA/Decimal(1000))+','+ str(HT_TO/Decimal(10))+','+ str(HT_TA/Decimal(10))+','+ str(HT_QBR/Decimal(100))+','+ str(HT_PPG/Decimal(100))+','+ str(HT_PPGA/Decimal(100))+','+ str(AT_YPG/Decimal(1000))+','+ str(AT_YPGA/Decimal(1000))+','+ str(AT_TO/Decimal(10))+','+ str(AT_TA/Decimal(10))+','+ str(AT_QBR/Decimal(100))+','+ str(AT_PPG/Decimal(100))+','+ str(AT_PPGA/Decimal(100))+'\n'
                result = str(result)+str(HT_WL)+','+ str(AT_WL)+'\n'
                exampleCount += 1
TSheader = str(exampleCount)+',14,2\n'     
result = str(TSheader) + str(result)
f.write(result)
print 'Done Compiling season data...'
print 'Exporting to .csv file...'
print 'All done.'
#export to .csv
#move on to next season, rinse, repeat
