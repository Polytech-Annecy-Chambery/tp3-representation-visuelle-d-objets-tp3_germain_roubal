# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 19:47:50 2017

@author: lfoul
"""
import OpenGL.GL as gl

class Section:
    # Constructor
    def __init__(self, parameters = {}) :  
        # Parameters
        # position: position of the wall 
        # width: width of the wall - mandatory
        # height: height of the wall - mandatory
        # thickness: thickness of the wall
        # color: color of the wall        

        # Sets the parameters
        self.parameters = parameters
        
        # Sets the default parameters
        if 'position' not in self.parameters:
            self.parameters['position'] = [0, 0, 0]        
        if 'width' not in self.parameters:
            raise Exception('Parameter "width" required.')   
        if 'height' not in self.parameters:
            raise Exception('Parameter "height" required.')   
        if 'orientation' not in self.parameters:
            self.parameters['orientation'] = 0              
        if 'thickness' not in self.parameters:
            self.parameters['thickness'] = 0.2   
        if 'color' not in self.parameters:
            self.parameters['color'] = [0.5, 0.5, 0.5]       
        if 'edges' not in self.parameters:
            self.parameters['edges'] = False             
            
        # Objects list
        self.objects = []

        # Generates the wall from parameters
        self.generate()   
        
    # Getter
    def getParameter(self, parameterKey):
        return self.parameters[parameterKey]
    
    # Setter
    def setParameter(self, parameterKey, parameterValue):
        self.parameters[parameterKey] = parameterValue
        return self     

    # Defines the vertices and faces 
    def generate(self):
        self.vertices = [ 
                [0,0,0],
                [0,0,self.parameters['height']],
                [self.parameters['width'],0,0],
                [self.parameters['width'],0,self.parameters['height']],
                [0,self.parameters['thickness'],self.parameters['height']],
                [0,self.parameters['thickness'],0],
                [self.parameters['width'],self.parameters['thickness'],self.parameters['height']],
                [self.parameters['width'],self.parameters['thickness'],0]                
                ]
        self.faces = [
                [0,1,3,2],
                [5,4,6,7],
                [0,1,4,5],
                [2,3,6,7],
                [1,4,6,3],
                [0,5,7,2]
                ]   

    # Checks if the opening can be created for the object x
    def canCreateOpening(self, x):
        if self.parameters['height']< x.parameters['height']+x.parameters['position'][2] or self.parameters['width'] < x.parameters['width'] +x.parameters['position'][0]:
            return False
        else :
            return True
        
    # Creates the new sections for the object x
    def createNewSections(self, x):
        Sec=[]
        for i in range(4):
            if i == 0 : 
                section=Section({'position':self.parameters['position'] , 'width':x.parameters['position'][0]-self.parameters['position'][0], 'height':self.parameters['height']})
            elif i==1 :
                section=Section({'position':[x.parameters['position'][0],self.parameters['position'][1],x.parameters['position'][2] + x.parameters['height'] ] , 'width':x.parameters['width'], 'height':self.parameters['height']-(x.parameters['position'][2]+x.parameters['height'])})
            elif i==2 :
                section=Section({'position':[x.parameters['position'][0],self.parameters['position'][1], self.parameters['position'][2]]  , 'width':x.parameters['width'], 'height':(x.parameters['position'][2]-self.parameters['position'][2])})
            elif i==3 :
                section=Section({'position':[x.parameters['position'][0] +  x.parameters['width'],self.parameters['position'][1],self.parameters['position'][2]], 'width':self.parameters['width']-x.parameters['width']-x.parameters['position'][0], 'height': self.parameters['height']})   
                
            if section.parameters['width'] !=0 and section.parameters['height'] !=0 :
                Sec.append(section)
        return Sec
                
                
        
    # Draws the edges
    def drawEdges(self): 
        
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK,gl.GL_LINE)
        gl.glBegin(gl.GL_QUADS)
        gl.glColor3fv([0.2, 0.2, 0.2]) 
        for i in range(len(self.faces)):
            for j in range(len(self.faces[0])):
                    gl.glVertex3fv(self.vertices[self.faces[i][j]])
        gl.glEnd() 
        
        
                    
    # Draws the faces
    def draw(self):
        gl.glPushMatrix()
        gl.glTranslate(self.parameters['position'][0],self.parameters['position'][1],self.parameters['position'][2])
        if self.parameters['edges'] == True : 
            self.drawEdges()
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL) # on trace les faces : GL_FILL
        gl.glBegin(gl.GL_QUADS) # Tracé d’un quadrilatère
        gl.glColor3fv([0.5, 0.5, 0.5]) # Couleur gris moyen
        for i in range(len(self.faces)):
            for j in range(len(self.faces[0])):
                    gl.glVertex3fv(self.vertices[self.faces[i][j]])
        gl.glEnd()      
        gl.glPopMatrix()
        
  