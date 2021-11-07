
# dummy autentification, always accept
def got_user(username, session, sessions):
    return 230, "Welcome, user!", username, "", 1, 1
        
def got_pass(username, password, session, sessions):
    return 202, "You think I care about passwords?", 1, 1

