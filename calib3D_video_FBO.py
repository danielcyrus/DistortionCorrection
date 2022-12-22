'''
@auther : Daniel Cyrus
Offscreen rendering video
Enhanced for better performance on CPU
'''

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import Image
from PIL import ImageOps
from cv2 import cv2
import numpy as np
from progress.bar import Bar

width, height = 4450, 2000
vertices=[]
straightVertices=[]

cap = cv2.VideoCapture("new_output.mp4")
video = cv2.VideoWriter('match_calibrated_4.avi', 
                         cv2.VideoWriter_fourcc(*'MJPG'),
                         30, (width,height))

def loadVertexes(width,height):
    global vertices
    vertices  = np.load("savedpoints/test1.npy",allow_pickle=True)
    vertices[:,0] = vertices[:,0] / width
    vertices[:,1] = vertices[:,1] / height

def loadStraightVertexes():
    global straightVertices
    straightVertices  = np.load("savedpoints/straightTest1.npy",allow_pickle=True)



def init(width, height):
    
    glClearColor(0.0,0.0,0.0,1)
    glClearDepth(1.0)
    glDepthFunc(GL_LEQUAL)
    
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    #glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)



    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
   
    gluPerspective(45, (width / height), 0.1, 3000.0)
    #glTranslatef(0.0, 0.0, 0.0)
    gluLookAt(900, 500, -1050, 900, 500, 0, 0, -1, 0)
    
    
  
    
texid = 0

def loadTexture(frame,width, height):
    global texid
    frm = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    frm = cv2.resize(frm,(width,height))
    frm = Image.frombuffer("RGB",[width, height],frm)
    textureData = ImageOps.flip(frm)
    textureData = np.fromstring(textureData.tobytes(), np.uint8)
   

    glEnable(GL_TEXTURE_2D)
    texid = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, texid)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height,0, GL_RGB, GL_UNSIGNED_BYTE, textureData)

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    return texid

def Render(r1,r2):
    
    glClear(GL_DEPTH_BUFFER_BIT)
    glBegin(GL_QUADS)
    for i in range(len(vertices)-1):
        if i+r2>=len(vertices):
            break

        if (i+1)%r1 == 0:
            continue

        vert1 = straightVertices[i]
        vert2 = straightVertices[i+r1]
        vert3 = straightVertices[i+r2]
        vert4 = straightVertices[i+1]

        glTexCoord2f(vertices[i][0],vertices[i][1])
        glVertex3fv(np.append(vert1,[0]))
        glTexCoord2f(vertices[i+r1][0],vertices[i+r1][1])
        glVertex3fv(np.append(vert2,[0]))
        glTexCoord2f(vertices[i+r2][0],vertices[i+r2][1])
        glVertex3fv(np.append(vert3,[0]))
        glTexCoord2f(vertices[i+1][0],vertices[i+1][1])
        glVertex3fv(np.append(vert4,[0]))
        
    glEnd()
    glFlush()
    glDeleteTextures(texid)
    

    

def saveScene(width, height):
    
    glPixelStorei(GL_PACK_ALIGNMENT, 1)
    data = glReadPixels(0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE)
    image = Image.frombytes("RGB", (width, height), data)
    open_cv_image = np.array(image)
    open_cv_image = open_cv_image[:, :, ::-1].copy() 
    video.write(open_cv_image)
    
    

def main():
    
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(width, height)
    glutCreateWindow(b"TempWindow")
    glutHideWindow()
    
    init(width, height)
    r1,r2, _ = np.load("rowAndCol.npy",allow_pickle=True)
    loadVertexes(width,height)
    loadStraightVertexes()
    
    frm = 0
    count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    bar = Bar('Frames', max=count)
    print(gluGetString(GLU_VERSION))
    while frm<count:
        
        _, frame = cap.read()
        loadTexture(frame,width, height)
        Render(int(r1),int(r2))
        
        saveScene(width,height)
        frm+=1
        
        bar.next()
        
       

    bar.finish()
    video.release()
    cap.release()

main()