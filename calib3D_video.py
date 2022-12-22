import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import glob
import cv2 as cv2
from PIL import Image
from PIL import ImageOps
##Define the vertices. usually a cube contains 8 vertices
vertices=[]
straightVertices=[]
lenVertex = 0
cap = cv2.VideoCapture("new_output.mp4")

def loadVertexes():
    global vertices
    vertices  = np.load("savedpoints/test1.npy",allow_pickle=True)

def loadStraightVertexes():
    global straightVertices
    straightVertices  = np.load("savedpoints/straightTest1.npy",allow_pickle=True)

texid =0
def loadTexture(frame):
    
    #textureSurface = pygame.image.load(files[frame])
    #textureSurface = pygame.transform.flip(frame, False,True)
    #textureSurface = pygame.transform.rotate(textureSurface, 180)
    #frm = cv2.resize(frame,(4450,2000))
    frm = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    frm = pygame.image.frombuffer(frm.tostring(), frm.shape[1::-1],"RGB")
    textureSurface = pygame.transform.flip(frm, False,True)
    textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
    width = textureSurface.get_width()
    height = textureSurface.get_height()
    


    glEnable(GL_TEXTURE_2D)
    texid = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, texid)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height,
                 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    
    return texid

def Plane(r1,r2):
    
    #glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glBegin(GL_QUADS)
    for i in range(lenVertex-1):
        if i+r2>=lenVertex:
            break

        if (i+1)%r1 == 0:
            continue

        vert1 = straightVertices[i] 
        vert2 = straightVertices[i+r1]
        vert3 = straightVertices[i+r2]
        vert4 = straightVertices[i+1]
        glTexCoord2f(vertices[i][0]/4450,vertices[i][1]/2000)
        glVertex3fv(np.append(vert1,[0]))
        glTexCoord2f(vertices[i+r1][0]/4450,vertices[i+r1][1]/2000)
        glVertex3fv(np.append(vert2,[0]))
        glTexCoord2f(vertices[i+r2][0]/4450,vertices[i+r2][1]/2000)
        glVertex3fv(np.append(vert3,[0]))
        glTexCoord2f(vertices[i+1][0]/4450,vertices[i+1][1]/2000)
        glVertex3fv(np.append(vert4,[0]))
        
        
    glEnd()
    glFlush()
    glDeleteTextures(texid)    


def saveScene(video):
    glPixelStorei(GL_PACK_SWAP_BYTES, 1)
    data = glReadPixels(0, 0, 4450, 2000, GL_RGB, GL_UNSIGNED_BYTE)
    image = Image.frombytes("RGB", (4450, 2000), data)
    image = ImageOps.flip(image)
    open_cv_image = np.array(image) 
    open_cv_image = open_cv_image[:, :, ::-1].copy() 
    video.write(open_cv_image)


def main():
    video = cv2.VideoWriter('match_calibrated_new3.avi', 
                         cv2.VideoWriter_fourcc(*'MJPG'),
                         30, (4450,2000))
    pygame.init()
    display=(4450,2000)
    pygame.display.set_caption("Camera calibration")
    pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 3000.0)
    glTranslatef(0.0, 0.0, 0.0)
    gluLookAt(950, 400, -1150, 950, 400, 0, 0, -1, 0)
    r1,r2, _ = np.load("rowAndCol.npy",allow_pickle=True)
   
    loadVertexes()
    loadStraightVertexes()
    lenVertex = len(vertices)
    ret = True
    while cap.isOpened():
        
        ret, frame = cap.read()
        
        loadTexture(frame)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                video.release()
                cap.release()
                quit()
            if  event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    video.release()
                    cap.release()
                    quit()
        #glRotatef(1, 3, 1, 1)

        glClearColor(1,1,1,1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        Plane(int(r1),int(r2))
        pygame.display.flip()
        saveScene(video)
        pygame.time.wait(1500)
        
    video.release()
    cap.release()

main()