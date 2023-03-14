import schedule
import time


def do_my_job():
    print("First Scheduler")


schedule.every(5).seconds.do(do_my_job)
# schedule.every(10).minutes.do(do_my_job)
# schedule.every().hour.do(do_my_job)
# schedule.every().day.at("10:30").do(do_my_job)
# schedule.every(5).to(10).minutes.do(do_my_job)
# schedule.every().monday.do(do_my_job)
# schedule.every().wednesday.at("13:15").do(do_my_job)
# schedule.every().minute.at(":17").do(do_my_job)


while True:
    schedule.run_pending()
    time.sleep(1)
