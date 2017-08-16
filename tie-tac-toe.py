import cv2
import numpy as np

w=500
l=500
offset=100
turn=False
end=False
mat=[0]*9
pos=[0]*9
def checkwin():
    for i in range(0,7,3):
        if mat[i]==mat[i+1]==mat[i+2] and mat[i]!=0:
            return mat[i]
    for i in range(3):
        if mat[i]==mat[i+3]==mat[i+6] and mat[i]!=0:
            return mat[i]
    if mat[0]==mat[4]==mat[8]:
        return mat[0]
    elif mat[2]==mat[4]==mat[6]:
        return mat[2]
    else:
        return 0
def setPos():
        pos[0]=(80,175)
        pos[3]=(80,340)
        pos[6]=(80,510)
        pos[1]=(240,175)
        pos[4]=(240,340)
        pos[7]=(240,510)
        pos[2]=(400,175)
        pos[5]=(400,340)
        pos[8]=(400,510)

def getgrid(x,y):
    if x<=160:
        if offset+60<y<260:
            return 0
        elif 260<y<420:
            return 3
        else:
            return 6
    elif x<=320:
        if offset+60<y<260:
            return 1
        elif 260<y<420:
            return 4
        else:
            return 7
    else:
        if offset+60<y<260:
            return 2
        elif 260<y<420:
            return 5
        else:
            return 8

cv2.namedWindow('image')
setPos()
def reset():
    global img,turn,end,mat,pos
    img = np.zeros((l+offset,w,3),np.uint8)
    img.fill(255)
    img=cv2.line(img,(160,offset+10),(160,l+offset-10),(0,0,0),10)
    img=cv2.line(img,(320,offset+10),(320,l+offset-10),(0,0,0),10)
    img=cv2.line(img,(10,offset+160),(w-10,offset+160),(0,0,0),10)
    img=cv2.line(img,(10,offset+320),(w-10,offset+320),(0,0,0),10)
    cv2.putText(img,'O',(200,70), 0, 3,(255,0,0),3,cv2.LINE_AA)
    pts = np.array([[0,0],[w-1,0],[w-1,offset-1],[0,offset-1]], np.int32)
    pts = pts.reshape((-1,1,2))
    img = cv2.polylines(img,[pts],True,(0,0,0),5)
    turn=False
    end=False
    mat=[0]*9

def draw(event,x,y,flags,param):
    global img,turn,mat,end
    if event == cv2.EVENT_LBUTTONDOWN:
        if y>=offset+60:
            g=getgrid(x,y)
            p=pos[g]
            if mat[g]==0 and end==False:
                if turn:  
                    l1=(p[0]-60,p[1]-60)
                    l2=(p[0]+60,p[1]+60)
                    l3=(p[0]-60,p[1]+60)
                    l4=(p[0]+60,p[1]-60)
                    img=cv2.line(img,l1,l2,(0,0,255),10)
                    img=cv2.line(img,l3,l4,(0,0,255),10)
                    mat[g]=1
                    turn=False
                else:   
                    cv2.circle(img,p,60,(255,0,0),5)
                    mat[g]=-1
                    turn=True
            winner=checkwin()
            cleartitle()
            if winner!=0:
                if winner==1:
                    cv2.putText(img,'Winner : X',(100,70), 0, 2,(0,0,255),3,cv2.LINE_AA)
                else:
                    cv2.putText(img,'Winner : O',(100,70), 0, 2,(255,0,0),3,cv2.LINE_AA)
                end=True
                return
            if mat.count(0)==0:
                    end=True
                    cv2.putText(img,'Tie',(200,70), 0, 2,(255,0,255),3,cv2.LINE_AA)
                    return
            if turn:
                cv2.putText(img,'X',(200,70), 0, 3,(0,0,255),3,cv2.LINE_AA)
            else:
                cv2.putText(img,'O',(200,70), 0, 3,(255,0,0),3,cv2.LINE_AA)
cv2.setMouseCallback('image',draw)
reset()
def cleartitle():
    for x in range(4,496):
        for y in range(4,96):
            img[y][x]=[255,255,255]
            
while(1):
    cv2.imshow('image',img)
    k=cv2.waitKey(1)
    if k == ord('q'):
        break
    elif k == ord('r'):
        reset()
     
cv2.destroyAllWindows()