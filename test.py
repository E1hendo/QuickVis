from direct.showbase.DirectObject import DirectObject
from direct.showbase.ShowBase import ShowBase


class CameraController(DirectObject):
	def	__init__(self):
		base.disableMouse()
		self.setupVars()
		self.setupCamera()
		self.setupInput()
		self.setupTasks()
		
	def setupVars(self):
		self.initZoom = 200			#meters
		self.zoomInLimit = 1		
		self.zoomOutLimit = 1000	
		self.moveSpeed = .5			
		self.zoom = None
		self.orbit = None
		self.move = None
	
	def setupCamera(self):
		self.camAnchor = render.attachNewNode("Cam Anchor")
		base.camera.reparentTo(self.camAnchor)
		base.camera.setPos(0, -self.initZoom, 0)
		base.camera.lookAt(self.camAnchor)
		
	def setupInput(self):
		self.accept("mouse1", self.setMove, [True])
		self.accept("mouse1-up", self.setMove, [False])
		self.accept("mouse3", self.setOrbit, [True])
		self.accept("mouse3-up", self.setOrbit, [False])
	
	def setupTasks(self):
		taskMgr.add(self.orbitCam, "Camera Orbit")
		
	def setOrbit(self, orbit):
		if(orbit == True):
			props = base.win.getProperties()
			window_x = props.getXSize()
			window_y = props.getYSize()
			if base.mouseWatcherNode.hasMouse():
				mouse_x = base.mouseWatcherNode.getMouseX()
				mouse_y = base.mouseWatcherNode.getMouseY()
				mPX = window_x * ((mouse_x+1)/2)
				mPY = window_y * ((-mouse_y+1)/2)
			self.orbit = [[mouse_x, mouse_y], [mPX, mPY]]
		else:
			self.orbit = None
	
	def orbitCam(self, task):
		if(self.orbit != None):
			if base.mouseWatcherNode.hasMouse():
				mpos = base.mouseWatcherNode.getMouse()
				base.win.movePointer(0, int(self.orbit[1][0]), int(self.orbit[1][1]))
				
				deltaH = 90 * (mpos[0] - self.orbit[0][0])
				deltaP = 90 * (mpos[1] - self.orbit[0][1])
				newH = (self.camAnchor.getH() + -deltaH)
				newP = (self.camAnchor.getP() + deltaP)
				self.camAnchor.setHpr(newH, newP, 0)				
		return task.cont
	
	def setMove(self, value):
		self.move = value
		
	def cameraMove(self, task):
		if(self.move == True):
			self.camAnchor.setY(self.camAnchor, self.moveSpeed)
			
		return task.cont


class PlayBackSpace(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)


        self.environ = self.loader.loadModel("models/clouds")
        self.environ.reparentTo(self.render)
        self.environ.setScale(12.25, 12.25, 12.25)
        self.environ.setPos(-8, 42, -12)


        #got to copy the models to the models folder or relink
        #probably want to get tiles from openmaps anyway
        self.environ = self.loader.loadModel("models/CityTerrain")
        self.environ.reparentTo(self.render)
        self.environ.setScale(0.25, 0.25, 0.25)
        self.environ.setPos(-8, 42, 0)



        self.disableMouse()
        self.camera = CameraController()
        self.plane = self.loader.loadModel("models/T3A")
        self.plane.reparentTo(self.render)
        self.plane.setScale(0.5, 0.5, 0.5)
        self.plane.setPos(0, 0, 2)
        self.taskMgr.add(self.update, "update")


    def update(self, task):
        dt = globalClock.getDt()

        #we would need to do playback in here by moving the plane
        speed = 32.0
        self.plane.setPos(self.plane.getPos()+ (0.0,speed * dt,0.0))
        self.camera.camAnchor.setPos(self.plane.getPos())
        return task.cont

game = PlayBackSpace()
game.run()
