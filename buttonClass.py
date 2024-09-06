import pygame

# -------------------------------------------------------------------------------------------------
# Button Class
# -------------------------------------------------------------------------------------------------

class Button:

    def __init__(self, x, y, width, height, text=None, colour=(180, 180, 180), highlightedColour=(102, 102, 102),
                 function=None):

        self.image = pygame.Surface((width, height))
        self.position = (x, y) # coordinates used for drawing buttons
        self.rect = self.image.get_rect() # shape of buttons
        self.rect.topleft = self.position # top left of buttons
        self.text = text
        self.colour = colour
        self.highlightedColour = highlightedColour
        self.function = function # function to be called
        self.highlighted = False # indicates if mouse is hovering over button
        self.width = width
        self.height = height

    def update(self, mouse):
        # contains code used to indicate if mouse is hovering over button
        if self.rect.collidepoint(mouse):
            self.highlighted = True
        else:
            self.highlighted = False

    def draw(self, window):
        # draws the buttons
        if self.highlighted:
            # highlights button if mouse if hovering over it
            self.image.fill(self.highlightedColour)
        else:
            # highlights button with its corresponding colour
            self.image.fill(self.colour)
        # blits button onto screen in the right position
        window.blit(self.image, self.position)

        #if self.text:
        # draws text on buttons as well
        self.drawText(self.text)
        window.blit(self.image, self.position)

    def click(self):
        # calls the function when you click the button
        self.function()

    def drawText(self, text):
        # contains code for drawing text on buttons
        font = pygame.font.SysFont("system", 24, bold=1)
        text = font.render(text, False, (50, 50, 50))
        width, height = text.get_size()
        # returns tuple, first width and then height
        x = (self.width - width) // 2
        y = (self.height - height) // 2
        # working out the coordinates for positioning the text properly
        self.image.blit(text, (x, y))
        # blits text onto screen

