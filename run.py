from analyzers.channel import *
from analyzers.group import *
from analyzers.user import *
from telethon.sync import TelegramClient
import json


# main function
def main():

    # setting up the user client which will be used in the rest of the program
    f = open('Credentials.json')
    client_info = json.load(f)
    client = TelegramClient(None, client_info["api_id"], client_info["api_hash"])
    client.start()

    # getting job type from user (channel/group/user) and running the job
    while True:
        job_type = input("Enter Job Type(channel/group/user): ")
        if job_type.lower() == 'channel':
            channel = ChannelAnalyzer()
            channel.run(client)
            break
        elif job_type.lower() == 'group':
            group = GroupAnalyzer()
            group.run(client)
            break
        elif job_type.lower() == 'user':
            user = UserAnalyzer()
            user.run(client)
            break
        else:
            print("Job type not defined, please try again.")
    
    # logging out of client account after job is done
    client.log_out()
if __name__ == '__main__':
    main()