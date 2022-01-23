import pyautogui as pg
import time
import random

metamask_img = "refs/metamask.png"
metamask_sign_img = "refs/metamask_sign.png"

adventure_img = "refs/adventure.png"
adventure_exit_img = "refs/back.png"

hero_img = "refs/hero.png"
hero_work_img = "refs/work_all.png"
hero_close_img = "refs/hero_close.png"

close_img = "refs/close.png"
login_img = "refs/login.png"
login_timeout_img = "refs/login_timeout.png"
serverup_img = 'refs/online.png'

restart_flag = 0


def click(box):
    w = box.left
    h = box.top

    w += random.random() * box.width * 0.7 + box.width * 0.2
    h += random.random() * box.height * 0.7 + box.height * 0.2

    pg.click(w, h)
    time.sleep(0.5)

    w = box.left
    h = box.top

    w += random.random() * box.width * 0.7 + box.width * 0.2
    h += random.random() * box.height * 0.7 + box.height * 0.2

    pg.click(w, h)


def raise_alert(alert):
    if alert == 'failed_restart':
        print("MANY RESTARTS FAILED, TRYING AGAIN IN 20 MIN")
        global restart_flag
        restart_flag = 0

        time.sleep(1200)
        Bomb_refresh()

    else:
        pass


def wait_until_present(timeout, ref):
    flag = 0
    step = 1
    while True:
        box = pg.locateOnScreen(ref, confidence = 0.9)

        if box is not None:
            return box
        else:
            time.sleep(step)
            flag += step
            if flag > timeout:
                raise TimeoutError


def validate_metamask():
    box = wait_until_present(10, metamask_sign_img)
    click(box)

    # box = wait_until_present(3, login_timeout_img)
    # if box is not None:
    #     raise TimeoutError


def Bomb_refresh():
    pg.hotkey("ctrl", "f5")
    time.sleep(5)

    box = wait_until_present(10, login_img)

    # CHECK SERVER STATUS
    status = pg.locateOnScreen(serverup_img)
    if status is None:
        # server status != ONLINE
        raise_alert('server_offline')

    click(box)

    time.sleep(3)
    validate_metamask()


def main_loop():
    # IF IN GAME
    # EXIT ADVENTURE MODE
    try:
        box = wait_until_present(2, adventure_exit_img)
        click(box)
    except TimeoutError:
        pass

    # CHECK FOR ALERT
    # nah

    # IF NOT IN GAME OR GRAVE ALERT
    global restart_flag
    restart_flag += 1
    if restart_flag > 5:
        raise_alert('failed_restart')

    Bomb_refresh()

    restart_flag = 0

    # SET ALL HEROS TO WORK
    box = wait_until_present(10, hero_img)
    click(box)
    time.sleep(5)

    try:
        box = wait_until_present(2, hero_work_img)
        click(box)
        time.sleep(2)
    except:
        pass

    box = wait_until_present(2, close_img)
    click(box)
    time.sleep(0.5)

    # ENTER ADVENTURE MODE

    box = wait_until_present(5, adventure_img)
    time.sleep(0.5)
    click(box)

    # GET AND FORWARD WALLET VALUE

    # TODO

    time.sleep(1200 + random.randint(0, 180))
    # time.sleep(15)

if __name__ == '__main__':
    while True:
        try:
            main_loop()

        except TimeoutError:
            continue
