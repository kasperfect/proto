__author__ = 'Thomas Kaland'
# _*_ coding: utf-8 _*_

def PiEmu (input, check):

    Relations = [[1],[5,6],[],[],[],[9],[],[10],[]]

    if(check in Relations[input]):
        return True
    else:
        return False

