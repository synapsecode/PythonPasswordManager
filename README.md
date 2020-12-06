# Python Password Manager
PythonPasswordManager abbreviated as ppm is a simple and easy-to-use command-line based password manager for Windows (as of now).

## Why use this?
I personally find this incredibly useful as I dont have to keep track of my passwords in my head. I can just go to my terminal and get the password that I want or I can list out all of my Passwords at once! This is really useful to me! Hence i made a tool so that you could benefit from it too!

## Installation (Windows only)
1. Clone this project to a directory in your machine and cd into it
2. Make sure you have python3 installed 
3. go to cmd type, 
```
pip install pyperclip prettytable
```
4. Copy the Directory path and then add it to your Path User Environment Variable
5. Close Cmd and Open it again. You should now be able to type ppm and access this script
6. Run the Keygen (only for the first time) and then you will get a cryptokey which will be copied to your clipboard
```
ppm keygen
```
7. create a new user environment variable called 'ppmcryptokey' and save the key in your clipboard as its value
8. Close and open the cmd again
9. Done. PythonPasswordManager has been setup on your PC

## Commands
> ### Adding a new Password
>> ```ppm add -n "Facebook" -p "123456" -k "abcd"```
>> The -n flag is the name of the password, -p flag is the password and the -k is your custom ppm encryption key

> ### Getting your Password
>> ```ppm get -n "Facebook" -k "abcd"``` you get the password based on its name! If you pass in any ppmkey except the one that you passed when creating the password entry then it will generate some useless garbage password

> ### Deleting an exsting password entry
>> ```ppm del -n "Facebook" -k "abcd"```

> ### Getting a list of all Saved Passwords
>> ```ppm list -k "abcd"``` You must remember to add the same ppmkey for all your passwords if you want to utilize this command. Else, it will produce garbage results

>>> Example(Using **Correct ppmkey**)
>>>> ![](https://github.com/synapsecode/PythonPasswordManager/blob/master/GithubData/1.JPG)


>>> Example(Using **Wrong ppmkey**): Notice how it generates incorrect passwords
>>>> ![](https://github.com/synapsecode/PythonPasswordManager/blob/master/GithubData/2.JPG)

> ### Clear All the Passwords at once
>>> ```ppm clear```

> ### Change the location where your encrypted passwords are saved
>> #### Saving it to root
>>> ```ppm config -ppxp .```

>> #### Saving it to any other location
>>> ```ppm config -ppxp <path>```

>> #### Get the location of current save path
>>> ```ppm -cppxp```

**Note: You technically can have a different ppmkey for each password but then you cannot use ppm list to list out all your passwords as that works only if you have the same ppmkey for all the passwords**

**Note: The ppmkey is not saved anywhere, If you lose it, its lost forever**

## Do not want to enter the ppmkey everytime? There is a solution!
**Warning: Use this only if youre sure that only you use the system and no one else knows that you have ppm installed. Otherwise, acess to your passwords becomes easy**

1. Clear all your passwords using ppm clear
2. Think of a custom ppmkey lets assume "a1b2c3"
3. Create a new environment variable named 'ppmkey' and put "a1b2c3" in it.
4. Close and open cmd again and now you can use the same commands but without entering the ppmkey each time! This also ensures that you have the same key for all the passwords. However, you can still specify another key and ppm will use that key instead of the environment one.

## Security (Is this safe?)
Yes it is. If you know the ppmkey that you provided during the password entry, then only that key can decipher the encrypted password! Otherwise it generates a random garbage password and displays it. It is less safe if you save the ppmkey into your environment variable. But if only you use your computer, then it is safe.

## Future Roadmap
I will be updating this with more nice features now and then! This is personally very useful and hence updating it frequently is not going to be a waste of time.
