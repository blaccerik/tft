# Tft AI (set 5.5)
Helper tool for the auto-chess game called Teamfight Tactics  

It collects data from the game using yolov3 image recognition algorithm and calculates the best build/comp  

yolov3:  
![image](https://user-images.githubusercontent.com/73612140/127324588-a6f9d30a-a295-4da0-9ddb-d4e7980e1e7c.png)

interface:  
![image](https://user-images.githubusercontent.com/73612140/127324752-d714c062-b252-4a53-9403-3b6fbb7f24e5.png)


Disclaimer!  
* Current version of yolo3 can find champions and parts but not completed items
* Current prediction algorithm only factors in your champions and /items. Since set 5.5 was recently released I dont have enough data to train nn which factors in other players builds, but it shouldn't make that big of a diffrence  

Before you run it make sure that the paths to files are correct!  
Open the following files and on the top there should be "C:/Users/theerik/PycharmProjects/tft/ xx / xx" line  
change it to the path where you have it stored. For example in Champions.py  
link = "C:/Users/theerik/PycharmProjects/tft/data/champions_store/edited" => link = "C:/Users/your_user/tft/champions_store/edited"  
Files:  
static_data.py  
Champions.py  
Champions_pic.py  
Champions.py  
Items.py  
screen.py files can be found in https://drive.google.com/drive/folders/1UBTFQWdB7qEY0upLsa-DLtu_5XoCSP8Y?usp=sharing  
Templates.py  

Also make sure you have all the needed modules installed:  
mss  
numpy  
cv2  
pyautogui  
difflib  
pytorch(torch)  

How to use:  
* find interface.py file and run it, it should take some time to load but thats okay
* the interface (shown above) should open
* Champion/Item selector:  
![image](https://user-images.githubusercontent.com/73612140/127325012-05fe3b49-8bf2-417e-ab3a-0d97b904ab85.png)  
type champion/item name into the white box and press enter/"?" to select the champion/item  
* Your champions:  
* ![image](https://user-images.githubusercontent.com/73612140/127325102-505d2c8e-21d6-476a-a694-99e8a010f16e.png)  
if you have selected your champion/item then press right click to add it to the queue  
if you want to increment champion/item number then press right click on it and left click do decrease it  
if you want to remove something from the queue then just decrease it until it disappears  
numbers under the champion mean how many copies you have on your screen:  
1 aatrox => one lvl 1 aatrox
3 aatrox => one lvl 2 aatrox  
9 aatrox => one lvl 3 aatrox  
* Buttons  
![image](https://user-images.githubusercontent.com/73612140/127325687-b5b73941-e024-44df-a857-f52f952c6e33.png)  
Get champs - takes a picture of the screen and finds all the champs/items (inc store) and adds them to the queue  
if that champ/items is already in the queue then it doesn add it  
If you have cuda installed and setup correctly then it only takes 0.5 sec to read the image otherwise it takes around 2 sec  
also I have added a small delay(1 sec) so you can switch to tft game window  
if you want to change the delay then you can edit the code in interface.py press_button function  
Its reccomended that you use bordeless mode for tft so you can swithc faster between windows  
Calculate - Calcualtes the best comps for you based on what you have entered above  
* Comps  
![image](https://user-images.githubusercontent.com/73612140/127326454-68b1a1e0-0a85-4b79-b9ed-660f2af37e3c.png)  
System shows top 3 comps for you and how to play them  
top 1 comp is the most top one  
* Single comp  
![image](https://user-images.githubusercontent.com/73612140/127329193-de95637d-cde1-4731-8fe8-06a2d7549298.png)  
Blue - main comp, this is what you should try to build  
Green - extra champs, use them to fill missing positions if you dont have all main comps champs  
Yellow - Core items, build these first if possible  
Red - Extra items, build these if you have core items built  





