import requests ,json

token = 'secret_pIqDsfSIx4rWqucnCMY3PoDz6DxWYWkd8FpniQW34VD'
databaseID = '3574f42993fa4efe90f5e4c7f7c2c112'
tasks=None

headers = {
    "Authorization":   token,
    "Content-Type": "application/json",
    "Notion-Version": "2021-05-13"
}
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
    print("Welcome TaskAPi")
    up=1
    down=1
    while 1:

        
        for i in tasks: 
            up = int(input("Up"))
            down =int(input("Down"))               
            if(up==1 and down==0):        
                print(i["name"])

            if(up==1 and down==1):
                pass
            if(up==0 and down==0):
                pass
            if(up==0 and down==1):
                pass






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



#readTask(databaseID,headers)
#dezplazarTarea(tasks)


#pageId="7ccdf40a-114b-47dd-a3ec-13ff0bcd9103"
#tareaCompletada(pageId,headers)
