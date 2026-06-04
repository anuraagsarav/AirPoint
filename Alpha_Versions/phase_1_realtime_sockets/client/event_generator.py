import random
import time

def generat_fake_event():
    events = [
        {
            "event" : "move",
            "dx" : random.randint(-20, 20),
            "dy" : random.randint(-20, 20)
        },
         
        {
            "event" : "click",
            "button" : "left"
        },

        {
            "event" : "scroll",
            "amount" : random.randint(-5, 5)   
        },
       
    ]

    return random.choice(events)