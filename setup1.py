
'''

welcome to the setup1-- part-1;
this file must be run before the setup2-- part2
Affter you installed both the parts you may now enjoy the main.py file!!

'''
import subprocess
import socket

def is_connected():
    try:
        # Try connecting to Google's DNS (8.8.8.8) on port 53
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        return True
    except OSError:
        return False

if is_connected():
    con=1
else:
    con=0

cres=is_connected()
if cres==1:
    def install_modules(module_list):
        not_found_modules = []
        
        for module in module_list:
            try:
                subprocess.run(['pip', 'install', module], check=True)
            except subprocess.CalledProcessError:
                not_found_modules.append(module)
        
        if not_found_modules:
            print("Modules not found and not installed:")
            for module in not_found_modules:
                print(module)
        else:
            print("All modules installed successfully!")

    # List of modules to install
    modules_to_install = ['tk-tools','requests','mysql-connector-python','pillow',
                          'tkcalendar','tabulate','random-number','random2','db-sqlite3',
                          'customtkinter']
    install_modules(modules_to_install)
    print("\n\n________SETUP PART--1--Done________")
else:
    print("++==++==++==++Connect to the internet first! ++==++==++==++")