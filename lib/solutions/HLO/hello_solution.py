
class HelloSolution:

    # friend_name = unicode string
    def hello(self, friend_name):
        if not friend_name:
            raise ValueError("friend_name cannot be empty")
        if not isinstance(friend_name, str):
            raise TypeError("friend_name parameter must be a string")
        try:
            friend_name.encode('utf-8')
            print("friend_name is a valid unicode string")
        except UnicodeEncodeError:
            raise UnicodeEncodeError("friend_name must be a unicode string")

        return f"Hello, {friend_name}!"

