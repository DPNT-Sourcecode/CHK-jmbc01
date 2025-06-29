
class HelloSolution:

    # friend_name = unicode string
    def hello(self, friend_name):
        if not friend_name:
            raise ValueError("friend_name cannot be empty")
        if not isinstance(friend_name, str):
            raise TypeError("friend_name parameter must be a string")
        try:
            friend_name.decode('utf-8')
        except UnicodeDecodeError:
            raise TypeError("friend_name must be a unicode string")
        return f"Hello, {friend_name}!"





