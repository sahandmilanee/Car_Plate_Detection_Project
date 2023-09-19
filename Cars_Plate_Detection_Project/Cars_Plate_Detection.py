import cv2
import matplotlib.pyplot as plt
import imutils
import easyocr
import sqlite3

#------------ Class  ------------

class car_license_palte:
    
    def __init__(self,image_name):
        self.image = cv2.imread(image_name)
        self.cnn = sqlite3.connect("plate.db")
    
    def plate_detection(self):
        
        try: # WIDTH = 800
            
            #----------- Load the image -------------
            
            image = imutils.resize(self.image, width=800)
            
            #--------- Convert the image to grayscale -------------
            
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            #---------- Apply Gaussian blur to reduce noise ------------
            
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            #----------- Perform edge detection --------------
            
            edges = cv2.Canny(blurred, 50, 150)
            
            #--------- Find contours in the edge-detected image ----------------
            
            contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            #--------- Initialize variables to store the coordinates of the license plate ------------
            
            plate_x = 0
            plate_y = 0
            plate_width = 0
            plate_height = 0
            
            #---------- Loop through the contours and find the largest one (assumed to be the license plate) --------
            
            for contour in contours:
                
                epsilon = 0.02 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                
                #------ Filter out small contours ------
                
                if len(approx) == 4 and cv2.contourArea(contour) >500:
                    x, y, w, h = cv2.boundingRect(contour)
                    plate_x = x
                    plate_y = y
                    plate_width = w
                    plate_height = h
            
            #---------- Draw a rectangle around the license plate -----------
            
            cv2.rectangle(image, (plate_x, plate_y), (plate_x + plate_width, plate_y + plate_height), (0, 255, 0), 3)
            plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            plt.show()
            
            #------------- Separating car license plate -------------
            
            license_plate = image[plate_y:plate_y+plate_height, plate_x:plate_x+plate_width]
            plt.imshow(cv2.cvtColor(license_plate, cv2.COLOR_BGR2RGB))
            plt.show()
            
            #------------- Separating car license plate in gray scale -------------
            gray_license_plate = cv2.cvtColor(license_plate, cv2.COLOR_BGR2GRAY)
            plt.imshow(cv2.cvtColor(gray_license_plate, cv2.COLOR_BGR2RGB))
            plt.show()
            
            return gray_license_plate
            
        except: # WIDTH = 500
                #----------- Load the image -------------
                
                image = imutils.resize(self.image, width=500)
                
                #--------- Convert the image to grayscale -------------
                
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                
                #---------- Apply Gaussian blur to reduce noise ------------
                
                blurred = cv2.GaussianBlur(gray, (5, 5), 0)
                
                #----------- Perform edge detection --------------
                
                edges = cv2.Canny(blurred, 50, 150)
                
                #--------- Find contours in the edge-detected image ----------------
                
                contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                #--------- Initialize variables to store the coordinates of the license plate ------------
                
                plate_x = 0
                plate_y = 0
                plate_width = 0
                plate_height = 0
                
                #---------- Loop through the contours and find the largest one (assumed to be the license plate) --------
                
                for contour in contours:
                    
                    epsilon = 0.02 * cv2.arcLength(contour, True)
                    approx = cv2.approxPolyDP(contour, epsilon, True)
                    
                    #------ Filter out small contours ------
                    
                    if len(approx) == 4 and cv2.contourArea(contour) >500:
                        x, y, w, h = cv2.boundingRect(contour)
                        plate_x = x
                        plate_y = y
                        plate_width = w
                        plate_height = h
                
                #---------- Draw a rectangle around the license plate -----------
                
                cv2.rectangle(image, (plate_x, plate_y), (plate_x + plate_width, plate_y + plate_height), (0, 255, 0), 3)
                plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                plt.show()
                
                #------------- Separating car license plate -------------
                
                license_plate = image[plate_y:plate_y+plate_height, plate_x:plate_x+plate_width]
                plt.imshow(cv2.cvtColor(license_plate, cv2.COLOR_BGR2RGB))
                plt.show()
                
                #------------- Separating car license plate in gray scale -------------
                gray_license_plate = cv2.cvtColor(license_plate, cv2.COLOR_BGR2GRAY)
                plt.imshow(cv2.cvtColor(gray_license_plate, cv2.COLOR_BGR2RGB))
                plt.show()
                
                return gray_license_plate
                
    def plate_number(self):
        
        gray_license_plate = self.plate_detection()
        reader = easyocr.Reader(["fa"])
        result = reader.readtext(gray_license_plate)
        if len(result) > 1:
            car_plate = result[1][1]
            return car_plate
        else:
            car_plate = result[0][1]
            return car_plate
        
            
 #-------- M A I N -------   

car = car_license_palte("1.jpg")
car_plate_number = car.plate_number()
print(car_plate_number)

#-----------------------------
