def name_cleaner(email: str):
    """
    Getting the name from email
    Example:
    - username@gmail.com => username
    - user.name@gmail.com => user name
    """
    email_char = ['.', '_', '-']
    sliced_name = email[:email.find("@")]
    for char in email_char:
        sliced_name = sliced_name.replace(char, " ")
    sliced_name = "".join([i for i in sliced_name if not i.isdigit()])
    return sliced_name
