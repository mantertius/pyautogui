import pyautogui, os, logging

#pip install pyautogui && pip install opencv-python
timeInterval = 0.2
LEFT = 'left'
RIGHT = 'right'
logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s.%(msecs)03d]: %(message)s', datefmt='%H:%M:%S')

def imgPath(filename):
    return os.path.join('images',f'{filename}.png')

def configSearch():
    logging.debug('Começando configuração da busca...')
    try:
        logging.debug('Ajustando a data...')
        b1x,b1y = pyautogui.locateCenterOnScreen(imgPath('qualquer_data'), confidence=.9)
        pyautogui.click(duration=timeInterval, x=b1x, y=b1y)
        logging.debug('Data ajustada.')

        logging.debug('Ajustando o tipo de exame...')
        b2x,b2y = pyautogui.locateCenterOnScreen(imgPath('dx'), confidence=.8) #será que ele vai encontrar o dx que eu quero????
        pyautogui.click(duration=timeInterval, x=b2x, y=b2y)
        logging.debug('Tipo de exame ajustado.')

        ##### de alguma forma ele nao consegue localizar esse noImage... não sei o que fazer! desativado por agora.
        # logging.debug('Filtrando laudos sem imagem...')
        # x,y = pyautogui.locateCenterOnScreen(imgPath('noImage', confidence=.8))
        # pyautogui.click(x=x,y=y,duration=timeInterval)
        # logging.debug('Laudos sem imagem filtrados.')

        logging.debug('Busca configurada.')
    except TypeError:
        pyautogui.alert('O proradis não está na página inicial. Por favor, cerifique-se de que o Proradis foi o último programa aberto e tente novamente.')
        
def refreshSearch():
    logging.debug('Atualizando a busca...')
    pyautogui.press('home')
    btnX,btnY = pyautogui.locateCenterOnScreen(imgPath('buscar'), confidence=.8)
    pyautogui.click(duration=timeInterval, x=btnX, y=btnY)
    pyautogui.sleep(10)
    logging.debug('Busca atualizada.')

def enterViewer():
    logging.debug('Entrando no visualizador...')
    x,y = pyautogui.locateCenterOnScreen(imgPath('viewer'), confidence=.8)
    pyautogui.click(x=x,y=y)
    logging.debug('Entrada no visualizador confirmada.')
    return x,y

def enterLaudo():
    logging.debug('Entrando na tela de laudo...')
    x,y = pyautogui.locateCenterOnScreen(imgPath('NomeFromBar'), confidence=.9)
    pyautogui.click(duration=timeInterval, x=x,y=y+50)
    pyautogui.sleep(10)
    x,y = pyautogui.locateCenterOnScreen(imgPath('selecioneUmResponsavel'), confidence=.8)
    pyautogui.click(x=x,y=y+200)
    logging.debug('Entrou na tela de laudo.')

def selectResponsable():
    try:            
        logging.debug('Selecionando responsável...')
        x,y = pyautogui.locateCenterOnScreen(imgPath('selecioneUmResponsavel'), confidence=.8)
        pyautogui.click(duration=timeInterval, x=x,y=y+200)
        logging.debug('Responsável selecionado.')
    except:
        x,y = pyautogui.locateCenterOnScreen(imgPath('enterViewerResponsable'), confidence=.8)
        pyautogui.click(duration=timeInterval, x=x,y=y+200)
        logging.debug('Responsável selecionado.')


def enterViewerFromLaudo():
    logging.debug('Entrando no visualizador...')
    x,y = pyautogui.locateCenterOnScreen(imgPath('enterViewer'), confidence=.8)
    pyautogui.click(duration=timeInterval, x=x,y=y) 
    logging.debug('Entrada no visualizador confirmada.')


def zoomOut(sleep:int):
    logging.debug('Esperando a página carregar.')
    pyautogui.sleep(sleep)
    logging.debug('Procurando pelo ponto de referência...')
    try:
        reference_x, reference_y = pyautogui.locateCenterOnScreen(imgPath('render_time'), confidence=.8)
        logging.debug('Ponto de referência foi encontrado.')
        logging.debug('Começando zoom out...')
        pyautogui.moveTo(x=reference_x, y=reference_y-(20), duration=timeInterval)
        pyautogui.dragTo(x=reference_x, y=reference_y-200, duration=timeInterval, button=RIGHT)
        logging.debug('Zoom out terminado.')
    except TypeError:
        logging.debug('Ponto de referência 1 não foi encontrado.')
        try:
            logging.debug('Procurando pelo segundo ponto de referência ...')
            reference_x, reference_y = pyautogui.locateCenterOnScreen(imgPath('pedido'), confidence=.8)
            logging.debug('Ponto de referência foi encontrado.')
            logging.debug('Começando zoom out...')
            pyautogui.moveTo(x=reference_x, y=reference_y+(300), duration=timeInterval)
            pyautogui.dragTo(x=reference_x, y=reference_y, duration=timeInterval, button=RIGHT)
            logging.debug('Zoom out terminado.')
        except TypeError:
            logging.debug('Nenhum ponto de referência foi encontrado. A tag não pode ser assimilada.')

def assimilateTag(tag):
    logging.debug('Procurando balão de assimilação de etiqueta...')
    ref_x,ref_y = pyautogui.locateCenterOnScreen(imgPath('blank_tag'), confidence=.8)
    logging.debug('Balão de assimilação de tag encontrado.')
    pyautogui.click(x=ref_x, y=ref_y, duration=timeInterval)
    logging.debug('Começando a assimalação de etiqueta...')
    pyautogui.write(tag)
    pyautogui.press('enter')
    logging.debug('Assimilação finalizada.')

def locateUpaName(nomeUpa):
    logging.debug(f'Procurando por {nomeUpa}...')
    try:
        ref_x, ref_y = pyautogui.locateCenterOnScreen(imgPath('upa_palmera'), confidence=.8) #procurando somente por upa palmeira
        logging.debug('Encontrado.')
        pyautogui.hotkey('ctrl','w')
        logging.debug('Buscando balão de assimilação de tag...')
        assimilateTagFromLaudo('UPA - PALMEIRA/OK') #somente locateUpaName pode chamar assimilateTag/assimilateTagFromLaudo!
    except TypeError:
        logging.debug(f'{nomeUpa} não foi encontrado.')
        pyautogui.hotkey('ctrl','w')


#good way
def assimilateTagFromLaudo(tag):
    logging.debug('Procurando por referência para chegar na etiqueta...')
    ref_x,ref_y = pyautogui.locateCenterOnScreen(imgPath('obsSolicitante'), confidence=.9)
    logging.debug('Referência encontrada.')
    pyautogui.click(x=ref_x, y=ref_y, duration=timeInterval)
    pyautogui.scroll(10)
    logging.debug('Procurando balão de assimilação de etiqueta...')
    ref_x,ref_y = pyautogui.locateCenterOnScreen(imgPath('blankCircularTag'), confidence=.8)
    logging.debug('Balão de assimilação de tag encontrado.')
    pyautogui.click(x=ref_x, y=ref_y, duration=timeInterval, clicks=2)
    logging.debug('Começando a assimalação de etiqueta...')
    pyautogui.write(tag)
    pyautogui.press('enter')
    logging.debug('Assimilação finalizada.')

def nextPatient():
    logging.debug('Indo para o próximo paciente...')
    x,y = pyautogui.locateCenterOnScreen(imgPath('nextPatient'), confidence=.9)
    pyautogui.click(x=x,y=y,duration=.3)
    pyautogui.sleep(5)
    logging.debug('Laudo do próximo paciente aberto.')

if __name__ == '__main__':
    try:
        logging.debug('Começando aplicação...')
        i = 0 
        prompted = int(pyautogui.prompt(text='Digite o número de pacientes.',title='Assimilar TAGS',default=10))
        pyautogui.sleep(3)
        pyautogui.hotkey('alt','tab')
        configSearch()
        refreshSearch()
        enterLaudo()    
        while i<prompted:
            logging.debug(f'Analisando paciente de número {i}...')
            if i>0:
                selectResponsable()
            enterViewerFromLaudo()
            zoomOut(10) 
            locateUpaName('UPA PALMERA DOS INDIOS')
            logging.debug(f'Paciente {i} analisado.')
            i+=1
            if i<prompted-1:
                nextPatient()
    except KeyboardInterrupt:
        logging.debug('Programa interrompido.')

