from telethon import functions
from telethon.errors import ChannelPrivateError, InviteHashExpiredError, InviteHashInvalidError, UserAlreadyParticipantError, ChatAdminRequiredError


# class for group object
class GroupAnalyzer:

    # "run" function that takes info from the user and uses it to setup the "summarize" function which will be used later on
    def run(self, client):
        self.client = client
        self.chatFull = ''

        # while loop to get username or invite link of group from user, joins the group, get info about the group, and handle possible errors
        while True:
            self.id = input("Please enter group's username or invite link: ")
            # if the user uses an invite link
            if 'https://t.me/joinchat/' in self.id:
                try:
                    self.client(functions.messages.ImportChatInviteRequest(self.id.replace('https://t.me/joinchat/', '')))
                    participants = []
                    for participant in self.client.iter_participants(self.id):
                        participants.append(participant)
                        if len(participants) == 1:
                            break
                    print("Group successfully joined!")
                    break
                except ChatAdminRequiredError:
                        print("Entered invite link is not a group link, please try again")
                except (InviteHashExpiredError, InviteHashInvalidError):
                    print("Invite link invalid or expired, please try again.")
                except UserAlreadyParticipantError:
                    print("You are a member of this group.")
                    break
            # if the user usee a username
            else:
                try:
                    self.chatFull = self.client(functions.channels.GetFullChannelRequest(self.id))
                    try:
                        participants = []
                        for participant in self.client.iter_participants(self.id):
                            participants.append(participant)
                            if len(participants) == 1:
                                break
                        self.client(functions.channels.JoinChannelRequest(self.id))
                        print("Group successfully joined!")
                        break
                    except ChatAdminRequiredError:
                        print("Entered username is not a group username, please try again")
                    except ChannelPrivateError:
                        print("Group is private, try entering an invite link.")
                except (TypeError, ValueError):
                    print("Entered username does not exist or is not a group username, please try again")
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
                print("Value must be a positive number or blank, please try again.")

        # calling the "summarize" function
        self.summarize()


    # "summarize" function that prints important information about the group and printing most recent messages
    def summarize(self):

        # printing important information about the channel
        print()
        print('Here are some information about the group:')
        print(f'ID: {self.chat.id}')
        print(f'Group Name: {self.chat.title}')
        if self.chatFull != '':
            print(f'Bio: {self.chatFull.full_chat.about}')
        print(f'Number of Members: {self.chat.participants_count}')
        print(f'Date Created: {self.chat.date}')

        # printing n most recent messsages in the channel
        print()
        if self.limit == 0:
            print('Here are all the messages in the group:')
        elif self.limit == 1:
            print('Here is the most recent message in the group:')
        else:
            print(f'Here are the {self.limit} most recent messages in the group:')
        message_count = 0
        for message in self.client.iter_messages(self.id):
            print(message.sender_id, ':', message.text)
            message_count += 1
            if message_count == self.limit:
                break
        
        # printing IDs, names, and usernames of members of the group 
        print()
        for user in self.client.iter_participants(self.id):
            print(f'ID: {user.id}', end="")
            if user.first_name == '' and user.last_name == '':
                print(f' | Name: None', end="")
            else:
                print(f' | Name: {user.first_name}', end="")
            if user.last_name:
                print(f' {user.last_name}', end="")
            print(f' | Username: {user.username}')