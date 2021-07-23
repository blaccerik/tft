# Tft AI (set 5.5)
Helper tool for the auto-chess game called Teamfight Tactics

It collects data from the game using yolov3 image recognition algorithm and calculates the best build/comp for you

yolov3:  
![image](https://user-images.githubusercontent.com/73612140/126772272-b9dc5cd7-b159-45b4-bb9f-dc4f6b57484b.png)

interface:  
![image](https://user-images.githubusercontent.com/73612140/126773738-16dcb206-ec9c-47a3-85af-f0f548b9b953.png)


Disclaimer!  
* Current version of yolo3 can only find champions and not items. I'm working on a updated version
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
* Champion selector:  
type champion name into the white box and press enter/"?" to select the champion  
![image](https://user-images.githubusercontent.com/73612140/126774890-9a789ff5-4cc2-49a1-a13a-daf16cdbfe80.png)  
* Your champions:  
if you have selected your champion then press right click to add champion to the queue  
press right click on a champ to add 1 to it and left click to either remove 1 or remove it entierly from the queue  
numbers under the champion mean how many copies you have on your screen -> 3 aatrox => one lvl 2 aatrox (3 * lvl 1 aatrox)  
9 aatrox => one lvl 3 aatrox  
![image](https://user-images.githubusercontent.com/73612140/126775054-c7ab69e7-6afd-453f-9143-ac49955dc7cc.png)  
* Buttons  
Get champs - takes a picture of the screen and finds all the champs (inc store) and adds them to the queue, if that champ is already in the queue then it doesn add it  
If you have cuda installed and setup correctly then it only takes 0.5 sec to read the image but I have added a 2 sec (you can change it: interface.py function press_button 1st line "time.sleep(2)" => "time.sleep(1)") delay so that you can switch back to your game window   
without cuda it can take up to 2 sec to read the image + delay time  
Its reccomended that you use bordeless mode for tft  
Calculate - Calcualtes the best comps for you based on what you have entered above  
![image](https://user-images.githubusercontent.com/73612140/126775348-a11e9357-1e39-48a7-875b-609bf79f8491.png)  
* Comps
There are 3 comps/build which are the top 3 (top1 is on the top) that the system thinks is the best  
![image](https://user-images.githubusercontent.com/73612140/126775723-0be58f98-e942-4ff8-8160-840a66db540b.png)  
* Single comp  
Green - main comp, this is what you should try to build  
Red - extra champs, use them to fill missing positions if you dont have all main comps champs  
Blue - Core items, build these first if possible  
Yellow - Extra items, build these if you have core items built  
![image](https://user-images.githubusercontent.com/73612140/126776222-8e16ea9b-8f35-48ef-918f-53a5cd93b7f2.png)  





