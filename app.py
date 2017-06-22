from multiprocessing import Process

import webservice
import yotsuba_bot

if __name__ == '__main__':
    yotsuba = Process(target=yotsuba_bot.main)
    webservice = Process(target=webservice.main)

    yotsuba.start()
    webservice.start()


