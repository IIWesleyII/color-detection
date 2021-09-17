import cv2
import pandas as pd
import argparse

"""Given an image, allow user to double click the image to
show the rgb color of the location.
"""

# Creating argument parser to take image path from command line
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help="Image Path")
args = vars(ap.parse_args())
img_path = args['image']
img = cv2.imread(img_path)

# Globals
r = g = b = xpos = ypos = 0
clicked = False

# read csv file with pandas and giving names to each column
index=["color","color_name","hex","R","G","B"]
csv = pd.read_csv('colors.csv', names=index, header=None)

# Calculate minimum distance from all colors and get closest matching color
def getColorName(R,G,B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
        if d<=minimum:
            minimum = d
            cname = csv.loc[i,"color_name"]
    return cname

# get x,y coordinates of double-click
def draw_function(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b,g,r,xpos,ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b,g,r = img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)
       
cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_function)


if __name__ == "__main__":
    while True:
        cv2.imshow("image",img)
        if clicked:

            # cv2.rectangle(image, startpoint(20,20), endpoint, color, thickness
            cv2.rectangle(img,(30,30), (700,60), (b,g,r), -1)

            # Creating text string to display( Color name and RGB values )
            text = getColorName(r,g,b) + ' R='+ str(r) +  ' G='+ str(g) +  ' B='+ str(b)

            # cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
            cv2.putText(img, text,(50,50),2,0.7,(255,255,255),2,cv2.LINE_AA)

            # if light color, display text in black color
            if r+g+b>=600:
                cv2.putText(img, text,(50,50),2,0.7,(0,0,0),2,cv2.LINE_AA)
                
            clicked=False

        # Break the loop when user hits 'esc' key    
        if cv2.waitKey(20) & 0xFF ==27:
            break
        
        # Exit program if exit button is pressed
        if cv2.getWindowProperty('image',cv2.WND_PROP_VISIBLE) < 1:        
            break       
    cv2.destroyAllWindows()
