from telethon import functions
from telethon.errors import ChatAdminRequiredError

# class for Channel object
class ChannelAnalyzer:

    # "run" function that takes info from the user and uses it to setup the "summarize" function which will be used later on
    def run(self, client):
        self.client = client

        # while loop to get username of channel from user, get info about the channel. and handle possible errors
        while True:
            self.id = input("Please enter channel's username: ")
            try:
                self.chatFull = client(functions.channels.GetFullChannelRequest(self.id))
                try:
                    participants = []
                    for participant in self.client.iter_participants(self.id):
                        participants.append(participant)
                        if len(participants) == 1:
                            break
                    print("Entered username is not a channel username, please try again")
                except ChatAdminRequiredError:
                    break
            except (TypeError, ValueError):
                print('Entered username does not exist or is not a channel username, please try again')
        self.chat = client.get_entity(self.id)
        
        # while loop to get limit of messages to print from user and handle possible errors
        while True:
            self.limit = input("Enter number of messages to show (type '0' for all messages): ")
            if self.limit.isnumeric():
                self.limit = int(self.limit)
                if self.limit < 0:
                        print("Value must be a 0 or more, please try again.")
                else:
                    break
            else:
                print("Value must be a positive number equal to or above 0, please try again.")

        # calling the "summarize" function
        self.summarize()


    # "summarize" function that prints important information about the channel and printing most recent messages
    def summarize(self):

        # printing important information about the channel
        print()
        print('Here are some information about the channel:')
        print(f'ID: {self.chatFull.full_chat.id}')
        print(f'Channel Name: {self.chat.title}')
        print(f'Bio: {self.chatFull.full_chat.about}')
        print(f'Number of Subscribers: {self.chatFull.full_chat.participants_count}')
        print(f'Date Created: {self.chat.date}')

        # printing n most recent messsages in the channel
        print()
        if self.limit == 0:
            print('Here are all the messages in the channel:')
        elif self.limit == 1:
            print('Here is the most recent message in the channel:')
        else:
            print(f'Here are the {self.limit} most recent messages in the channel:')
        message_count = 0
        for message in self.client.iter_messages(self.id):
            print(message.sender_id, ':', message.text)
            message_count += 1
            if message_count == self.limit:
                break