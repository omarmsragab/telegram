from telethon import functions


# class for user object
class UserAnalyzer:

    # "run" function that takes info from the user and uses it to setup the "summarize" function which will be used later on
    def run(self, client):
        self.client = client
        while True:
            self.id = input("Please enter user's username: ")
            try:
                self.userFull = self.client(functions.users.GetFullUserRequest(self.id))
                break
            except (TypeError, ValueError):
                print('Entered ID does not exist or is not a username, please try again')
        self.user = self.client.get_entity(self.id)
        self.summarize()
    
    # "summarize" function that prints important information about the specified user
    def summarize(self):
        print()
        print(self.user.stringify())
        print(f'ID: {self.user.id}')
        print(f'Username: {self.user.username}')
        print(f'Phone: {self.user.phone}')
        print(f'First Name: {self.user.first_name}')
        print(f'Last Name: {self.user.last_name}')
        print(f'Bio: {self.userFull.about}')
        if self.user.contact:
            print('This user is in my contacts')
        else:
            print('This user is not in my contacts')