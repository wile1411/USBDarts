import cmath
import math
import time
import os
import usb.core
import usb.util
dev = usb.core.find(find_all=True)
device = dev[0]

dev = usb.core.find(idVendor=0x1C03, idProduct=0x0001)
_name = usb.util.get_string(device, 255, 2)
print(_name)


device.set_configuration()
cfg = device.get_active_configuration()
interface_number = cfg[(0,0)].bInterfaceNumber
alternate_setting = usb.control.get_interface(device,interface_number)
intf = usb.util.find_descriptor(cfg, bInterfaceNumber = interface_number, bAlternateSetting = alternate_setting)
ep = usb.util.find_descriptor(intf,custom_match = lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN)

import array
mtboard = array.array('B',[0,0,0,0,0,0,0,0,0,0,0,0])
exitboard = array.array('B',[0,0,0,0,0,0,0,0,0,0,0,4])
exitboardseq = ['UP','DW','UP']

dartboard = [['S20','S12','S14','S8','S7','S19','S16','S11'],['S20','S12','S14','S8','S7','S19','S16','S11'],['D20','D12','D14','D8','D7','D19','D16','D11'],['T20','T12','T14','T8','T7','T19','T16','T11'],['T1','T4','T6','T15','T17','T3','T2','T10'],['D1','D4','D6','D15','D17','D3','D2','D10'],['S1','S4','S6','S15','S17','S3','S2','S10'],['S1','S4','S6','S15','S17','S3','S2','S10'],['S9','S9','D9','T9','T13','D13','S13','S13'],['S5','S5','D5','T5','T18','D18','S18','S18'],['DB','SB','','','','','',''],['UP','DW','PC','','','','','']]


darttext = [["Single 20","Single 12","Single 14","Single 8","Single 7","Single 19","Single 16","Single 11"],["Single 20","Single 12","Single 14","Single 8","Single 7","Single 19","Single 16","Single 11"],["Double 20","Double 12","Double 14","Double 8","Double 7","Double 19","Double 16","Double 11"],["Triple 20","Triple 12","Triple 14","Triple 8","Triple 7","Triple 19","Triple 16","Triple 11"],["Triple 1","Triple 4","Triple 6","Triple 15","Triple 17","Triple 3","Triple 2","Triple 10"],["Double 1","Double 4","Double 6","Double 15","Double 17","Double 3","Double 2","Double 10"],["Single 1","Single 4","Single 6","Single 15","Single 17","Single 13","Single 2","Single 10"],["Single 1","Single 4","Single 6","Single 15","Single 17","Single 13","Single 2","Single 10"],["Single 9","Single 9","Double 9","Triple 9","Triple 13","Double 13","Single 13","Single 13"],["Single 5","Single 5","Double 5","Triple 5","Triple 18","Double 18","Single 18","Single 18"],["Double Bull!","Single Bull","","","","","",""],["Up Button","Down Button","Player Change","","","",""]]

dartnumbervalue = [[20,12,14,8,7,19,16,11],[20,12,14,8,7,19,16,11],[40,24,28,16,14,38,32,22],[60,36,42,24,21,57,48,33],[3,12,18,45,51,9,6,30],[2,8,12,30,34,6,4,20],[1,4,6,15,17,3,2,10],[1,4,6,15,17,3,2,10],[9,9,18,27,39,26,13,13],[5,5,10,15,54,36,18,18],[50,25,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]

gametotal = 101
playerone = 0
playertwo = 0
gametotal = gametotal
currentplayer = '1'
currentplayertotal = 0
p1d1 = ''
p1d2 = ''
p1d3 = ''
p2d1 = ''
p2d2 = ''
p2d3 = ''
currentset = 0
onedarts = []
twodarts = []
ponebust = '        '
ptwobust = '        '

lastthreepresses = ['0','0','0','0']
lastpress = []
prevvalue = None


while True :
  try :
    # Read from USB stream
    if prevvalue != currentvalue :
      if (lastthreepresses==exitboardseq) :
        print("!!!ExitBoard!!!")
        break
      elif (currentvalue!=mtboard) :
        li = currentvalue.tolist()
        idxval = [i for i in range(len(li)) if li[i] != 0]
        rowref = int(idxval[0])
        colref = int(abs(math.log(li[idxval[0]],2)))
        darthit = (dartboard[rowref][colref])
        lastthreepresses.append(darthit)
        if (len(lastthreepresses) > 4) :
          dummyval = lastthreepresses.pop(0)
        if (currentplayer=='1') :
          if (playerone + dartnumbervalue[rowref][colref] > gametotal) :
            darthit = 'PC'
            ponebust = '!-BUST-!'
            playerone -= currentset
        elif (currentplayer=='2') :
          if (playertwo + dartnumbervalue[rowref][colref] > gametotal) :
            darthit = 'PC'
            ptwobust = '!-BUST-!'
            playertwo -= currentset
        if (darthit=='PC') :
          currentset = 0
          if (currentplayer=='1') :
            currentplayer = '2'
            twodarts = []
            p2d1 = ''
            p2d2 = ''
            p2d3 = ''
          else :
            currentplayer = '1'
            onedarts = []
            p1d1 = ''
            p1d2 = ''
            p1d3 = ''
        elif (darthit=='DW' or darthit=='UP') :
          pass
        else :
          currentset += dartnumbervalue[rowref][colref]
          if (currentplayer=='1') :
            ponebust = '        '
            onedarts.append(darttext[rowref][colref])
            playerone += dartnumbervalue[rowref][colref]
            if (len(onedarts)==1) :
              p1d1 = onedarts[0]
            if (len(onedarts)==2) :
              p1d2 = onedarts[1]
            if (len(onedarts)==3) :
              p1d3 = onedarts[2]
          else :
            ptwobust = '        '
            twodarts.append(darttext[rowref][colref])
            playertwo += dartnumbervalue[rowref][colref]
            if (len(twodarts)==1) :
              p2d1 = twodarts[0]
            if (len(twodarts)==2) :
              p2d2 = twodarts[1]
            if (len(twodarts)==3) :
              p2d3 = twodarts[2]
        dummyval = os.system('cls' if os.name=='nt' else 'clear')
        if (playerone==gametotal) :
          ponebust = '!WINNER!'
        if (playertwo==gametotal) :
          ptwobust = '!WINNER!'
        print('           Game: ' + str(gametotal))
        print('')
        if (currentplayer=='1') :
          print('**Player 1**            Player 2  ')
        else :
          print('  Player 1            **Player 2**')
        print('    '  + '{:>3}'.format(str(gametotal-playerone)) + '                   '  + '{:>3}'.format(str(gametotal-playertwo)) + '     ')
        print('  ' + ponebust + '              ' + ptwobust)
        print('')
        print('          Last 3 Darts')
        print('')
        print('D1: ' + '{:<12}'.format(p1d1) + '      D1: ' + '{:<12}'.format(p2d1))
        print('D2: ' + '{:<12}'.format(p1d2) + '      D2: ' + '{:<12}'.format(p2d2))
        print('D3: ' + '{:<12}'.format(p1d3) + '      D3: ' + '{:<12}'.format(p2d3))
        print('')
        print('')
        print('Last Dart:' + darttext[rowref][colref] + '    Last 4: ' + lastthreepresses[0] + ', ' + lastthreepresses[1] + ', ' + lastthreepresses[2] + ', ' + lastthreepresses[3])
      else :
        pass
      # Wait for stream to return to empty
      prevvalue = currentvalue
    else :
      print(prevvalue + ' ---- ' + ep.read(16))
  except :
      currentvalue = ep.read(16)
      continue