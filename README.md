# Tft AI (set 5.5)
Helper tool for the auto-chess game called Teamfight Tactics  

It collects data from the game using yolov3 image recognition algorithm and calculates the best build/comp  

yolov3:  
![image](https://user-images.githubusercontent.com/73612140/127324588-a6f9d30a-a295-4da0-9ddb-d4e7980e1e7c.png)

interface:  
![image](https://user-images.githubusercontent.com/73612140/128009424-542f2b6c-7562-4b17-9d0e-ffce3c41e3e7.png)


Disclaimer!  
* Current version of yolo3 can find champions and parts but not completed items, you have to enter them yourself

Before you run it make sure that the paths to files are correct!  
Open path_manager.py and change path to your needs  
Also in data/network there is missing one file named yolov3_training_last.weights (its too large for git)  
You need to download it from my drive https://drive.google.com/drive/folders/1UBTFQWdB7qEY0upLsa-DLtu_5XoCSP8Y?usp=sharing  

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
* Queue:  
![image](https://user-images.githubusercontent.com/73612140/128009503-ec0fa013-a83a-4631-b17f-70902447569b.png)  
This shows current champions/items for players  
if you have selected your champion/item then press right click to add it to the queue  
if you want to increment champion/item number then press right click on it and left click do decrease it  
if you want to remove something from the queue then just decrease it until it disappears  
numbers under the champion mean how many copies you have on your screen:  
1 aatrox => one lvl 1 aatrox
3 aatrox => one lvl 2 aatrox  
9 aatrox => one lvl 3 aatrox  
* Buttons  
![image](https://user-images.githubusercontent.com/73612140/128009542-5dd5ca22-5da0-41cf-a6e2-a24362db4c49.png)  
Get champs - takes a picture of the screen and finds all the champs/items and adds them to the queue  
if you select "inc store" then it also adds champs from your store
if you select "only me" then it takes picture of only your champions (need the be watching them), otherwise it goes through the player list one by one and takes pictures of them  all (enable if you dont have cuda, takes too long)  
if that champ/items is already in the queue then it doesn add it  
If you have cuda installed and setup correctly then it only takes 0.5 sec to read the image otherwise it takes around 2 sec  
also I have added a small delay(1 sec) so you can switch to tft game window  
if you want to change the delay then you can edit the code in interface.py press_button function  
Its reccomended that you use bordeless mode for tft so you can swithc faster between windows  

Calculate - Calcualtes the best comps for you based on what you have entered above  
Level - right click to add level and left to decrease  
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





