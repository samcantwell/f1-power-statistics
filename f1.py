import fastf1

fastf1.Cache.enable_cache('~/f1_cache')

# When changing seasons, change drivers list at top for loop
# Actual year number at the top of the get_Scores function
# And the race list near the bottom in the loop


drivers_2018 = ['44', '7', '5', '33', '3', '20', '8', '27', '55', '77', '14', '2', '11', '18', '31', '28', '9', '16', '35', '10']
races_2018 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]

drivers_2019 = ['44', '77', '5', '33', '16', '8', '20', '4', '7', '11', '27', '3', '23', '99', '26', '18', '10', '55', '63', '88']
races_2019 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]

drivers_2020 = ['77', '44', '33', '4', '23', '11', '16', '55', '18', '3', '5', '10', '26', '31', '8', '20', '63', '99', '7', '6']
races_2020 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]

drivers_2021 = ['33', '44', '77', '16', '10', '3', '4', '55', '14', '18', '11', '99', '22', '7', '63', '31', '6', '5', '47', '9']
races_2021 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22]


drivers = {}
for driver in drivers_2018:
    drivers[driver] = {}


def get_scores_for_race(race):
    session = fastf1.get_session(2018, race, 'Q')
    session.load()
    
    
    for driver in drivers:
        drivers[driver][race] = {}
        lap = session.laps.pick_driver(driver).pick_fastest()
        try:
            tel = lap.get_car_data().add_distance()
        except AttributeError:
            drivers[driver][race] = 0
            continue

        drivers[driver][race]['lap'] = lap
        drivers[driver][race]['tel'] = tel
    
    for driver in drivers:
        if drivers[driver][race] == 0:
            continue

        tel = drivers[driver][race]['tel']
        fastest_acc = 0
        high_p = 0
        drivers[driver][race]['acc'] = []
        drivers[driver][race]['p'] = []
        for i in range(len(tel)-4):
            dtm = tel['Time'][i+3] - tel['Time'][i]
            dt = dtm.microseconds / 1000000
            ds = tel['Speed'][i+3] - tel['Speed'][i]
            acc = ds/dt
            drivers[driver][race]['acc'].append(acc)
            if acc > fastest_acc:
                fastest_acc = acc

            tm = tel['Time'][i+2] - tel['Time'][i]
            t = tm.microseconds / 1000000
            s0 = tel['Speed'][i] / 3.6
            s1 = tel['Speed'][i+2] / 3.6
            a = (s1-s0)/t
            f = 740 * a
            d = tel['Distance'][i+2] - tel['Distance'][i]
            w = f * d
            p = w / t

            print("p:", p, "t:", t, "k0, k1:", k0, k1, tel['Speed'][i] / 3.6, tel['Speed'][i+2] / 3.6)
            if p > high_p:
                high_p = p
            drivers[driver][race]['p'].append(p)

    
        drivers[driver][race]['acc'].sort(reverse=True)
        drivers[driver][race]['p'].sort(reverse=True)
        drivers[driver][race]['avg_acc'] = sum(drivers[driver][race]['acc'][1:7]) / 6
        drivers[driver][race]['avg_p'] = sum(drivers[driver][race]['p'][0:3]) / 3


    fastest_avg_acc = 0
    high_avg_p = 0
    for driver in drivers:
        if drivers[driver][race] == 0:
            continue

        avg_acc = drivers[driver][race]['avg_acc']
        avg_p = drivers[driver][race]['avg_p']
        if avg_acc > fastest_avg_acc:
            fastest_avg_acc = avg_acc
        if avg_p > high_avg_p:
            high_avg_p = avg_p
    

    for driver in drivers:
        if drivers[driver][race] == 0:
            drivers[driver][race] = {'avg_acc': 0, 'avg_p': 0}

        acc_score = drivers[driver][race]['avg_acc'] / fastest_avg_acc
        drivers[driver][race]['acc_score'] = acc_score 
   

for race in races_2018:
    get_scores_for_race(race)


scores = {}
for driver in drivers:
    total = 0
    total_p = 0
    count = 0
    for race in drivers[driver]:
        if drivers[driver][race] != 0:
            total += drivers[driver][race]['acc_score']
            total_p += drivers[driver][race]['avg_p']
            count += 1

    avg = total / count
    avg_p = total_p / count
    drivers[driver]['avg_score'] = avg
    drivers[driver]['avg_p'] = avg_p
    scores[driver] = avg
    print(driver, ":", avg, ": power:", avg_p / 1000)

