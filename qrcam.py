import qrcode
import cv2 
from pyzbar.pyzbar import decode
from PIL import Image
import tkinter as tk
from tkinter import filedialog

def scan_qrcode_from_camera() :
    cap= cv2.VideoCapture(0)

    while True :
        ret,frame= cap.read()

        if not ret :
           break

        decoded_objects= decode (frame)

        for obj in decoded_objects :
            points= obj.polygon
            if len(points)>4: 
               hull = cv2.convexHull(points,returnPoints=True)
               points=[tuple(points[0]) for point in hull]
            for i in range(len(points)):
               pt1=points[i]
               pt2=points[(i+1)% len(points)]
               cv2.line(frame,pt1,pt2,(0,255,0),2)
            
            # Get data from QR code
            qr_data = obj.data.decode('utf-8')
            print("QR Code Data:", qr_data)

            # Display data on the frame
            cv2.putText(frame, qr_data, (points[0][0], points[0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Display the frame with drawn rectangles and text
        cv2.imshow("QR Code Scanner", frame)

        # Exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close the window
    cap.release()
    cv2.destroyAllWindows()

def scan_qr_code_from_gallery():
    # Open file dialog to select image
    root = tk.Tk()
    
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])

    if file_path:
        image = Image.open(file_path)
        decoded_objects = decode(image)

        if decoded_objects:
            for obj in decoded_objects:
                qr_data = obj.data.decode('utf-8')
                print("QR Code Data:", qr_data)
        else:
            print("No QR Code found in the selected image.")

def makeqr():
    choiceqr=input("enter your choice of qr > URL or password :")
    myqr= qrcode.make(choiceqr)
    myqr.save("myqr.png")

def read_qr():
     seeqr= decode(Image.open("myqr.png"))
     print(seeqr[0].data.decode("ascii"))  

def main():
    print("Choose an option:")
    print("1. Scan QR Code from Camera")
    print("2. Scan QR Code from Gallery")
    print("3.Create a new QRcode")
    print("4.Read your QRcode")


    choice = input("Enter your choice (1,2,3 or 4): ")
    if choice == '1':
        scan_qrcode_from_camera()
    elif choice == '2':
        scan_qr_code_from_gallery()
    elif choice == '3':
        makeqr() 
    elif choice == '4':
        read_qr()        
    else:
        print("Invalid choice. Please choose 1,2,3 or 4.")

if __name__ == "__main__":
    main()