import RPi.GPIO as GPIO
import time
import I2C_LCD_driver
import requests ,json



token = 'secret_pIqDsfSIx4rWqucnCMY3PoDz6DxWYWkd8FpniQW34VD'
databaseID = '3574f42993fa4efe90f5e4c7f7c2c112'
tasks=None
mylcd = I2C_LCD_driver.lcd()
pageId=None

headers = {
    "Authorization":   token,
    "Content-Type": "application/json",
    "Notion-Version": "2021-05-13"
}


GPIO.setmode(GPIO.BOARD)
ledR=7
GPIO.setup(ledR,GPIO.OUT)
ledG=37
GPIO.setup(ledG,GPIO.OUT)
push=11
GPIO.setup(push,GPIO.IN)
downA=13
GPIO.setup(downA,GPIO.IN)
upA=15
GPIO.setup(upA,GPIO.IN)
	

	
	
	
def readTask(databaseID,headers):
    readUrl= f"https://api.notion.com/v1/databases/{databaseID}/query"

    res = requests.request("POST",readUrl,headers=headers)
    data= res.json()
   
    #Aca hago una estrategia para obtener el titulo de la tarea
    global tasks
    tasks = []
    for obj in data["results"]:            
        task={
            'id': obj["id"],
            'name':'',
            'checkbox': obj["properties"]["Check"]["checkbox"]
        }
        for tittle in obj["properties"]["Tarea"]["title"] :
            task["name"] = tittle["text"]["content"]
            
        tasks.append(task)  
    
    print(res.status_code)    
   
    return tasks

def taskActual(tasks):
    mylcd.lcd_display_string("Welcome TaskAPi", 2)
    index=0
    index_ref=None
    maxindex= len(tasks)
    
    while 1:
        colorCheck= tasks[index]["checkbox"]
        if(colorCheck==True):
            GPIO.output(ledG,True)
            GPIO.output(ledR,False)
        else:
            GPIO.output(ledR,True)
            GPIO.output(ledG,False)

        lec_push= GPIO.input(push)
        up = GPIO.input(upA)
        down = GPIO.input(downA)
        if(up==0):
            index=index-1
            while(up==0):
                up = GPIO.input(upA)
                time.sleep(0.1)
        elif(down==0):
            index=index+1
            while(down==0):
                down = GPIO.input(downA)
                time.sleep(0.1)
        if(index<0):
            index=maxindex-1
        elif(index>=maxindex):
            index=0
        
        if(index!=index_ref):
            global pageId
            pageId=tasks[index]["id"]
            index_ref=index
        #time.sleep(0.1)
        my_string = tasks[index]["name"]
        str_pad = " " * 16
        tam_text= len(my_string)
        my_long_string = str_pad + my_string
        my_long_string2 = my_string+ str_pad
        if(tam_text>16):
            
            for i in range (0, len(my_long_string)):
                lcd_text = my_long_string[i:(i+16)]
                mylcd.lcd_display_string(lcd_text,1)
                time.sleep(0.4)
                mylcd.lcd_display_string(str_pad,1)
                
                
        else:
            mylcd.lcd_display_string(my_long_string2, 1)
        print(index)
        
        if lec_push == 0:
            #GPIO.output(led,True)
            print("Se cumplio la tarea")
            tareaCompletada(pageId,headers)
            readTask(databaseID,headers)
            return tasks
        time.sleep(0.1)
        
        
    
        
        
    

            
                          
            

def tareaCompletada(pageId,headers):
    updateUrl= f"https://api.notion.com/v1/pages/{pageId}"
    updateData = {
        "properties": {
            "Check": {"checkbox": True}
        }
    }
    data=json.dumps(updateData)

    response = requests.request("PATCH",updateUrl,headers=headers,data=data)
    print(response.status_code)
    print(response.text)
    


readTask(databaseID,headers)
while(tasks!=[]):
	taskActual(tasks)
    
	
