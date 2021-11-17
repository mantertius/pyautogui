import pyautogui, time, os, logging, sys, random, copy
ms = 0.3
#refresh search

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s.%(msecs)03d: %(message)s', datefmt='%H:%M:%S')
def refresh_search():
    logging.debug('Atualizando a busca...')
    pyautogui.press('home')
    pyautogui.click(x=1136,y=442)
    pyautogui.sleep(10)

def imPath(filename):
    """A shortcut for joining the 'images/'' file path, since it is used so often. Returns the filename with 'images/' prepended."""
    return os.path.join('images', filename)

#the search has been refreshed, enter a pacient
def enter_patient(sleep_time):
    logging.debug('Entrando no paciente...')
    pyautogui.click(x=1020,y=578)
    pyautogui.sleep(sleep_time)

    #638,125
    #638,459
    #1275,459
    #1275,125
#inside a patient
def deactivate_laudo(ms):
    logging.debug('Tentando desativar o laudo...')
    region = (638,125,637,334)
    while True:
        if pyautogui.locateOnScreen('deactivate_protocol_image.png', region=region) != None :
            pyautogui.click(x=1770,y=970,duration=ms)
            pyautogui.sleep(ms)
            pyautogui.scroll(-1000)
            pyautogui.sleep(ms)
            pyautogui.click(x=1780,y=964,duration=ms)
            pyautogui.click(x=970,y=605,duration=ms)
            break
        else:
            logging.debug('Menu de seleção de radiologista não encontrado.')
            continue
    


#closing the newtab
def close_new_tab():
    logging.debug('Laudo desativado.')
    pyautogui.sleep(3)
    pyautogui.hotkey('ctrl','w')

def run(ms, refresh_search, enter_patient, deactivate_laudo, close_new_tab):
    refresh_search()
    enter_patient(7)
    deactivate_laudo(ms)
    close_new_tab()

i=0
prompted = pyautogui.prompt(text='Digite o número de pacientes',title='Desativar Laudos',default=10)
while i<int(prompted):
    pyautogui.hotkey('alt','tab')
    run(ms, refresh_search, enter_patient, deactivate_laudo, close_new_tab)
    i+=1
pyautogui.alert(text=f'Desativado o laudo de {prompted} pacientes',title='Finalizado',button='OK')