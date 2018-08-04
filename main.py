import pygame
import random
import time

####

class Question:

    def __init__(self):
        self.font = pygame.font.Font('fonts/DK Crayon Crumble.ttf', 72)
        self.a = random.randint(0,9)
        self.b = random.randint(5,9)
        self.type = '*'
        self.text = "Hvad er {} {} {} = ?".format(self.a, self.type, self.b)
        self.answer = None
        self.time = time.time()
        self.expect = self.calc()
        self.status = None


    def calc(self):
        if self.type == '*':
            return self.a * self.b
        elif self.type == '+':
            return self.a + self.b
        elif self.type == '-':
            return self.a - self.b
        elif self.type == '/':
            return self.a / self.b
            

    def draw_question(self, screen):
        if self.answer is not None:
            self.text = self.text.replace('?', '')
            line = "{}{}".format(self.text, self.answer)
        else:
            line = self.text
        fw, fh = self.font.size(line) # fw: font width,  fh: font height
        surface = self.font.render(line, True, (255, 255, 255))
        width, hight = screen.get_size()
        # // makes integer division in python3
        screen.blit(surface, ((width - fw) // 2, (hight - fh) // 2))


class App(object):


    def __init__(self, width=640, height=400, fps=30):
        """Initialize pygame, window, background, font,...
        """
        pygame.init()
        pygame.display.set_caption("Press ESC to quit")
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.background = pygame.image.load("images/bg1.jpg")
        self.background = pygame.transform.scale(self.background, self.screen.get_size())
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.playtime = 0.0
        self.questions = []
        self.font = pygame.font.Font('fonts/DK Crayon Crumble.ttf', 72)
        self.max_questions = 2
        

    def start(self):
        self.questions = []
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()
        time.sleep(1)      
        self.draw_text("Parat?")
        pygame.display.flip()
        time.sleep(1)
        self.screen.blit(self.background, (0, 0))
        self.draw_text("Start")
        pygame.display.flip()
        time.sleep(1)
        self.screen.blit(self.background, (0, 0))
        self.draw_text("Nu!")
        pygame.display.flip()
        time.sleep(1)
        self.screen.blit(self.background, (0, 0))


    def run(self):
        """The mainloop
        """
        running = True
        self.start()
        q = Question()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_RETURN:
                        q.time = time.time() - q.time
                        if int(q.answer) == q.expect:
                            q.status = True
                            self.draw_text("Rigtigt")
                        else:
                            q.status = False
                            self.draw_text("Forkert")
                            pygame.mixer.init()
                            pygame.mixer.music.load("sounds/fail.mp3")
                            pygame.mixer.music.play()
                        q.text = "{}{}".format(q.text, q.answer)
                        self.questions.append(q)
                        pygame.display.flip()
                        time.sleep(1)
                        q = Question()
                    elif event.key == pygame.K_BACKSPACE:
                        if q.answer is not None and len(q.answer) > 0:
                            q.answer = q.answer[:-1]
                    else:
                        if event.unicode in "1234567890":
                            if q.answer is None:
                                q.answer = event.unicode
                            else:
                                q.answer += event.unicode
                        print (q.answer)


            milliseconds = self.clock.tick(self.fps)
            self.playtime += milliseconds / 1000.0
#            self.draw_text("FPS: {:6.3}{}PLAYTIME: {:6.3} SECONDS".format(
#                           self.clock.get_fps(), " "*5, self.playtime))
            
            q.draw_question(self.screen)
            pygame.display.flip()
            self.screen.blit(self.background, (0, 0))
            if len(self.questions) >= self.max_questions:
                fails = [q for q in self.questions if q.status == False]
                slow = [q for q in self.questions if q.time > 4.0]
                farstest = min([q.time for q in self.questions])
                slowest = max([q.time for q in self.questions])
                average = sum([q.time for q in self.questions])/self.max_questions
                correct = len([q for q in self.questions if q.status == True])
                wrong = len([q for q in self.questions if q.status == False])
                if len(fails) == 0 and len(slow) == 0:
                    pygame.mixer.init()
                    pygame.mixer.music.load("sounds/level1000.mp3")
                    pygame.mixer.music.play()
                    self.draw_text("Tillykke du er level 1000!")
                    pygame.display.flip()
                    while pygame.mixer.music.get_busy():
                        time.sleep(1)                       
                    self.screen.blit(self.background, (0, 0))
                for q in self.questions:
                    print("{} ({:0.1f})".format(q.text, q.time))
                print("Rigtige svar:          {}".format(correct))
                print("Forkerte svar:         {}".format(wrong))
                print("Hurtigste svar tid:    {:0.1f} sekunder".format(farstest))
                print("Langsommeste svar tid: {:0.1f} sekunder".format(slowest))
                print("Middel svar tid:       {:0.1f} sekunder".format(average))
                self.draw_text("Vil du prøve igen tryk 'y'")
                pygame.display.flip()
                key_pressed = False
                while not key_pressed:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:                        
                            key_pressed = True
                            if event.key == pygame.K_y:
                                self.start()
                                q = Question()
                            else:
                                running = False
    
        pygame.quit()

        

    def draw_text(self, text):
        """Center text in window
        """
        fw, fh = self.font.size(text) # fw: font width,  fh: font height
        surface = self.font.render(text, True, (255, 255, 255))
        # // makes integer division in python3
        self.screen.blit(surface, ((self.width - fw) // 2, (self.height - fh) // 2))

####

if __name__ == '__main__':

    # call with width of window and fps
    App(1024, 720).run()
