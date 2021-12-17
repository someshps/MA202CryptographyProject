import matplotlib.pyplot as plt
import math,time
import numpy as np
import sys

#------------------------------------------------------------------------------------------------------------------------------
#The deffie hellman function

def deffie_hellman():
                                                            #These are fixed beforehand and are parameters of PRG of Diffie Hellman. These are known publicly, and we will fix them according to the degree of function we want
    def pseudorandomKeygenerator(n):                        #Function that returns a common secret shared key between Alice and Bob
        P = np.random.randint(pow(10,n-1),pow(10,n))        #The number of digits in P is taken= degree of polynomial we are using
        G = 472                                             #A random number P, will be decided publically between Alice and Bob in real life
        
        a=np.random.randint(P)                              #Alice will choose the private key a

        x = int(pow(G,a,P))

        b = np.random.randint(P)                            #Bob will choose the private key b

        y = int(pow(G,b,P))                                 #Gets the generated key
        kab = int(pow(y,a,P))                               #Secret key for Alice
        kba = int(pow(x,b,P))                               #Secret key for Bob
        
        return kab

    n=np.random.randint(2,10)                               #A random number n, will be decided publically between Alice and Bob in real life
    key=pseudorandomKeygenerator(n)
    key=key%10
    if (key==0):                                            #To avoid dividing by zero complications
        key=2
    return(max(key,2))                                      #To avoid dividing by zero complications

#------------------------------------------------------------------------------------------------------------------------------
def funx(x,vals):                                           #Function to evaluate the value of one way function
    val=3.5*(x*x*x)-2.7*(x)-17 - vals
    return val

def fdash(x):                                               #Function to evaluate the value of derivative of the one way function
    val=10.5*(x*x)-2.7*x
    return val

f=open('sample.txt','r')                                    #Reading the sample text from desktop and storing it in the array char_list
char_list=[]
while 1:
    char=f.read(1)
    if not char:
        break
    char_list.append(char)

f.close()
Ascii_values = [ord(character) for character in char_list]  #Converting to ASCII numbers and storing it in the array Ascii_values
original_ascii=Ascii_values                                 #storing original ascii, for future use. this will be untouched

print("The text to be sent is:")                            #Printing the text which is going to be shared
print("")
for i in char_list:
    print(i,end="")

print("")


#NUMBER 1 - BISECTION METHOD
print("")
print("Bisection Method begins")
print("")

print("The non garbage ASCII string is -> ")                #The non garbaged ascii string
print(Ascii_values)
print("")
#------------------------------------------------------------------------------------------------------------------------------
encrypted_l=[]                                              #array to store encrypted values, the roots
number_of_iterations_array=[0]                              #array to store number of iterations taken for every 10th character
xaxis1=[0]                                                  #array storing coordinates of x axis
time_stamps1=[0]                                            #Array of time stamps
garbage_index=deffie_hellman()                              #Getting a number, which is known only by ALice and Bob, from the function. This secret number is the index of garbages

temparr=[]                                                  #temporary array, will contain garbaged ascii value
final_length=math.ceil(len(Ascii_values)/(garbage_index-1))+len(Ascii_values) #final length is length of garbaged ascii array

j=0                                                         #pointer to original ascii array
for i in range(final_length):                               #adding garbage
    if (i%garbage_index==0):                                #if it is the garabge index, add garbage
        temparr.append(np.random.randint(65,122))           #garbage will be a random number, the range is 65 to 122 as it is the range of alphabets, small and capital
    else:
        temparr.append(Ascii_values[j])                     #if it is not garbage, add the original ascii digit
        j=j+1                                               #increment the pointer to original ascii array

Ascii_values=temparr                                        #updating the ungarbaged ascii array to garbaged one
print("New garbaged ascii array is ")                       #printing garbaged it
print("Length in Newton Raphson is",len(Ascii_values))
print(Ascii_values) 

#------------------------------------------------------------------------------------------------------------------------------
counter=0                                                   #counter to track the characters
total_iterations=0                                          #variable to store total number of iterations

start_time=time.time()                                      #variable storing start time
for j in Ascii_values:                                      #Here we run bisection method to find the root of the equation f(x)=j for each 
    xl=0                                                    #lower limit guess value
    xu=7                                                    #upper limit guess value
    xr=(xl+xu)/2                                            #midpoint to be checked 
    xdr=funx(xr,j)                                          #value of the function at xr                                           
    
    no_of_iterations=0                                      #variable to count the number of iterations
    while (abs(xdr)>0.001):                                 #running the loop till we get close enough, that is an error of 0.001
        no_of_iterations=no_of_iterations+1                 #incrementing number of iterations
        xdr=funx(xr,j)                                      #value of the function at xr
        xdl=funx(xl,j)                                      #value of the function at xl
        if(xdr*xdl<0):                                      #root is closer to xl                                      
            xu=xr                                           #update xu
            xr=(xl+xu)/2                                    #update xr
        elif (xdr*xdl>0):                                   #root is closer to xr
            xl=xr                                           #update xl
            xr=(xl+xu)/2                                    #update xr
        else:                                               #we have found the root! 
            break                                           #break out of the loop
    
    encrypted_l.append(xr)                                  #add the found root to encrypted_l
    

    if ((counter%10)==0 and counter!=0):                    #if we are on the 10th character, append to the list
        number_of_iterations_array.append(total_iterations+number_of_iterations_array[-1])
        time_stamps1.append(time.time()-start_time)
        xaxis1.append(counter)
    
    counter=counter+1                                       #incrementing counter
    total_iterations=total_iterations+no_of_iterations

print("NUMBER OF ITERATIONS ARRAY IS")                      #printing array showing number of iterations taken
print(number_of_iterations_array)
print("")

#------------------------------------------------------------------------------------------------------------------------------
print("Array has been encrypted! Encrypted array is -> ")   #printing the encrypted array                        
print (encrypted_l)
print("")

#NOW, WE SEND THE ENCRYPTED ARRAY TO THE RECEIVER 

#------------------------------------------------------------------------------------------------------------------------------

decrypted_l=[]                                              #decryption begins. decrypted_l is the array of decrypted ascii values
counter=0                                                   #initializing the counter

for i in range(len(encrypted_l)):                           #starting decryption                                        
    if ((i%garbage_index)!=0):                              #only decrypt if it is garbage value
        decrypted_l.append(round(funx(encrypted_l[i],0)))   #adding the ascii values to decrypted_l
        counter=counter+1                                   #increment counter

res=""
for val in decrypted_l:                                     #building answer string
    res=res+chr(val)                                        #adding converted character to final answer
    
print("The decrypted string is: ")                          #printing the answer
print("")
print(str(res))                                             #printing the decrypted string
print("")
#------------------------------------------------------------------------------------------------------------------------------

#NUMBER 2 - NEWTON RAPHSON METHOD
print("")
print("Newton Raphson Method begins")
print("")

print("The converted ASCII string is -> ")
print(Ascii_values)
print("")
#------------------------------------------------------------------------------------------------------------------------------

encrypted_l=[]                                              #array to store encrypted values, the roots
xaxis2=[0]                                                  #xaxis for second plot
time_stamps2=[0]                                            #array to store times taken

number_of_iterations_array2=[0]                             #array to store number of iterations taken for every 10th character
print("New garbaged ascii array is ")                       #printing garbaged it
print(Ascii_values) 

#------------------------------------------------------------------------------------------------------------------------------
counter2=0                                                  #counter to store number of characters      
total_iterations=0                                          #variable to store total iterations

start_time=time.time()                                      #variable storing time of start
for j in Ascii_values:                                      #running the newton raphson method
    x=3                                                     #initial guess value
    fx=funx(x,j)                                            #fx is the value of the function at x (our guess value)
    no_of_iterations=0                                      #variable to store number of iterations
    while (abs(fx)>0.001):                                  #run until error is less than equal to 0.001
        fx=funx(x,j)                                        #storing the value of f(x) at x
        slope=fdash(x)                                      #variable to store the slope, value of derivative of f(x) at x
        x=x-(fx/slope)                                      #calculating a new, closer value of x             
        no_of_iterations=no_of_iterations+1                 #incrementing number of iterations
    encrypted_l.append(x)                                   #add the found root to encrypted_l
    counter2=counter2+1                                     #incrementing the counter
    if ((counter2%10)==0 and counter2!=0):
        number_of_iterations_array2.append(total_iterations+number_of_iterations_array2[-1])
        time_stamps2.append(time.time()-start_time)
        xaxis2.append(counter2)
    
    total_iterations=total_iterations+no_of_iterations
print("Counter for newton raphosn is",counter2)

print("THE OTHER NUMBER OF ITRERTAIONS ARRAY IS ")          #printing array which stores number of iterations
print(number_of_iterations_array2)
    
#------------------------------------------------------------------------------------------------------------------------------
print("")
print("Array has been encrypted! Encrypted array is -> ")   #printing the encrypted array                        
print (encrypted_l)
print("")
#NOW, WE SEND THE ENCRYPTED ARRAY TO THE RECEIVER 

#------------------------------------------------------------------------------------------------------------------------------

decrypted_l=[]                                              #decryption begins. decrypted_l is the array of decrypted ascii values
counter=0                                                   #initializing the counter

for i in range(len(encrypted_l)):                           #starting decryption                                        
    if ((i%garbage_index)!=0):                              #only decrypt if it is garbage value
        decrypted_l.append(round(funx(encrypted_l[i],0)))   #adding the ascii values to decrypted_l
        counter=counter+1                                   #increment counter

res=""
for val in decrypted_l:                                     #building answer string
    res=res+chr(val)                                        #adding converted character to final answer
    
print("The decrypted string is: ")                          #printing the answer
print("")
print(str(res))                                             #printing the decrypted string
print("")
#------------------------------------------------------------------------------------------------------------------------------

#Plotting number of iterations

plt.plot(xaxis1,number_of_iterations_array,label="Bisection Method")
plt.plot(xaxis2,number_of_iterations_array2,label="Newton Raphson Method")
plt.title("Number of iterations per 10 characters - Text Conversion")
plt.xlabel("Number of Characters")
plt.ylabel("Number of iterations")
plt.legend()
plt.show()

#Plotting time taken
plt.plot(xaxis1,time_stamps1,label="Bisection Method")
plt.plot(xaxis2,time_stamps2,label="Newton Raphson Method")
plt.title("Time taken per 10 characters - Text Conversion")
plt.xlabel("Number of Characters")
plt.ylabel("Time in seconds")
plt.legend()
plt.show()

#------------------------------------------------------------------------------------------------------------------------------