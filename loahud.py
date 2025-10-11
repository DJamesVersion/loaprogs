import socket
import os
import smtplib
from email.message import EmailMessage
import netifaces as ni
import time
from datetime import datetime

# --- Configuration ---
# NOTE: Replace these with your actual SMTP server details and credentials.
# You MUST use an App Password or equivalent security feature from your email provider
# (e.g., Gmail, Outlook) for login() to work, not your main account password.
SMTP_SERVER = "smtp.example.com" # Example: "smtp.gmail.com"
SMTP_PORT = 587                    # Usually 587 for TLS
SENDER_EMAIL = "your.email@example.com"
SENDER_PASSWORD = "your_app_password"


def get_local_ip_and_mac(interface='eth0'):
    """Retrieves the local IP, netmask, and MAC address for the specified interface."""
    data = {}
    try:
        # Get IP and Netmask
        if_info = ni.ifaddresses(interface).get(ni.AF_INET, [{}])[0]
        data['ip'] = if_info.get('addr', 'N/A')
        data['netmask'] = if_info.get('netmask', 'N/A')
        
        # Get MAC
        mac_info = ni.ifaddresses(interface).get(ni.AF_LINK, [{}])[0]
        data['mac'] = mac_info.get('addr', 'N/A')
    except ValueError:
        data['ip'] = 'Interface Not Found'
        data['netmask'] = 'N/A'
        data['mac'] = 'N/A'
    return data

def get_proxy_settings():
    """Retrieves the HTTP/S proxy settings from system environment variables."""
    proxies = {
        'HTTP_PROXY': os.environ.get('HTTP_PROXY') or os.environ.get('http_proxy'),
        'HTTPS_PROXY': os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy')
    }
    
    # Extract just the port if possible, otherwise return the full value
    proxy_info = {}
    for key, value in proxies.items():
        if value:
            # Simple attempt to find the port number
            try:
                # Value format is typically: http://host:port or user:pass@host:port
                if ':' in value:
                    parts = value.split(':')
                    port = parts[-1]
                    proxy_info[key] = f"Enabled (Port: {port})"
                else:
                    proxy_info[key] = f"Enabled ({value})"
            except Exception:
                proxy_info[key] = f"Enabled ({value})"
        else:
            proxy_info[key] = "Not Set"
            
    return proxy_info

def send_email_authorized(recipient, subject, body):
    """
    Sends an email using authenticated SMTP. Requires correct SMTP server setup
    and App Password/secure credentials.
    """
    if 'example.com' in SENDER_EMAIL or 'your_app_password' in SENDER_PASSWORD:
        return f"EMAIL FAILED: Please update SMTP settings in hud.py before trying to send."

    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure the connection
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        return "EMAIL SUCCESS: Message sent successfully."
    except Exception as e:
        return f"EMAIL ERROR: Could not send email. Check credentials/port. Error: {e}"


def display_hud(ip_data, proxy_data, message=""):
    """Renders the main HUD to the terminal."""
    os.system('cls' if os.name == 'nt' else 'clear') # Clear screen for HUD effect
    
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("\033[92m" + "="*50)
    print("= \033[1mLOCAL SYSTEM DIAGNOSTIC HUD\033[0m\033[92m " + " "*17 + "=")
    print("= "*25)
    print(f"= \033[96mCURRENT TIME:\033[0m {now} " + " "*(50 - 20 - len(now)) + "=")
    print(f"= \033[96mHOST NAME:   \033[0m {socket.gethostname()} " + " "*(50 - 20 - len(socket.gethostname())) + "=")
    print("= "*25)
    
    # Network Status
    print("= \033[93mNETWORK INTERFACE (eth0/Wi-Fi):\033[0m" + " "*12 + "=")
    print(f"=   \033[94mIP Address:\033[0m {ip_data['ip']} " + " "*(50 - 16 - len(ip_data['ip'])) + "=")
    print(f"=   \033[94mNetmask:   \033[0m {ip_data['netmask']} " + " "*(50 - 16 - len(ip_data['netmask'])) + "=")
    print(f"=   \033[94mMAC Address:\033[0m {ip_data['mac']} " + " "*(50 - 16 - len(ip_data['mac'])) + "=")
    
    # Proxy Status
    print("= "*25)
    print("= \033[93mPROXY CONFIGURATION (Environment Vars):\033[0m" + " "*5 + "=")
    print(f"=   \033[94mHTTP Proxy:\033[0m {proxy_data['HTTP_PROXY']} " + " "*(50 - 16 - len(proxy_data['HTTP_PROXY'])) + "=")
    print(f"=   \033[94mHTTPS Proxy:\033[0m {proxy_data['HTTPS_PROXY']} " + " "*(50 - 16 - len(proxy_data['HTTPS_PROXY'])) + "=")
    
    print("= "*25)
    
    # Status/Message Box
    print("= \033[95mSTATUS/OUTPUT:\033[0m" + " "*33 + "=")
    if message:
        print(f"=   \033[91m{message}\033[0m" + " "*(50 - 4 - len(message)) + "=")
    else:
        print("=   Awaiting command..." + " "*30 + "=")
        
    print("="*50 + "\033[0m")
    
    # Menu
    print("\n--- COMMANDS ---")
    print("1: Refresh Status")
    print("2: Send Test Email")
    print("q: Quit")
    print("----------------")


# --- Main Loop ---
if __name__ == "__main__":
    current_message = "Welcome! Remember to check your interface name (e.g., 'eth0', 'wlan0') if IP is 'N/A'."
    interface_name = 'eth0' # You may need to change this to 'wlan0', 'Wi-Fi', etc., depending on your OS

    while True:
        try:
            # 1. Gather data
            ip_info = get_local_ip_and_mac(interface_name)
            proxy_info = get_proxy_settings()
            
            # 2. Display HUD
            display_hud(ip_info, proxy_info, current_message)
            
            # 3. Get user input
            choice = input("Enter command: ").strip().lower()
            
            if choice == 'q':
                print("\nExiting HUD. Goodbye!")
                break
            
            elif choice == '1':
                current_message = "Status refreshed."
                
            elif choice == '2':
                # Example usage of the secure email function
                test_recipient = input("Enter recipient email for test: ")
                email_subject = "Python HUD Test Email"
                email_body = f"This email was successfully sent from your Python HUD on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}."
                
                print("\nAttempting to send email...")
                current_message = send_email_authorized(test_recipient, email_subject, email_body)
            
            else:
                current_message = f"Invalid command: '{choice}'. Please use 1, 2, or q."
            
        except KeyboardInterrupt:
            print("\nExiting HUD. Goodbye!")
            break
        except Exception as e:
            current_message = f"An unexpected error occurred: {e}"
            time.sleep(2)

# Placeholder note for SMS/Call functionality:
# To make calls or send texts, you would need to integrate with a service like Twilio or Signal's API,
# which requires setting up an account and using their authenticated tokens.

