import BlynkLib
from time import sleep
from sense_hat import SenseHat
from capture_image import capture_image
from upload_image import upload_image

#initialise SenseHAT
sense = SenseHat()
sense.clear()

# Blynk authentication token
BLYNK_AUTH = 'ZTy81af05xPWir2slcT-1U4BcsPESdCr'
IMAGE_PATH="./week10-lab2/images/image.jpg"
# Initialise the Blynk instance
blynk = BlynkLib.Blynk(BLYNK_AUTH)

# Register handler for virtual pin V1 write event
@blynk.on("V1")
def handle_v1_write(value):
    button_value = value[0]
    print(f'Current button value: {button_value}')
    
    if button_value=="1":
        sense.clear(255,255,255)
        capture_image(IMAGE_PATH)
        result = upload_image(IMAGE_PATH)
        
        blynk.set_property(2,"urls",result) #updates ulrs property of widget attached to Datastream2(virtual pin V2)
    else:
        sense.clear()

# Main loop to keep the Blynk connection alive and process events
if __name__ == "__main__":
    print("Blynk application started. Listening for events...")
    try:
        while True:
            blynk.run()  # Process Blynk events
            blynk.virtual_write(0, round(sense.temperature,2))
            sleep(2)  # Add a short delay to avoid high CPU usage
    except KeyboardInterrupt:
        print("Blynk application stopped.")