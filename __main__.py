
from model import Model
from controller import Controller
from view import View
 
 
def main():
    width = 250
    height = 175
    fps = 30
 
    model = Model(width, height, fps)
    view = View(model.width, model.height, fps)
    controller = Controller(model, view)
 
    controller.start()
 
 
if __name__ == '__main__':
    main()
