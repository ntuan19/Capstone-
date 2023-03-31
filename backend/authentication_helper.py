from app import clientCollection
#check account duplicates.
from dao.crud import Crud
from flask import flash, redirect, url_for
from collections import defaultdict

list_numbers = ["1","2","3","4","5","6","7","8","9","0"]
special_characters = ["!","@","#","$","%","^","&","*","~","_","-","+","="]

def check_email_duplicates(email):
    dic_info = {"email":email}
    dic = Crud(dic_info)
    result = dic.find()
    flash("Duplicates")
    if not result:
        return True
    return False 

    

#check if the password has enough special char, 
def check_sign_up(password,password_retype):
    special_char = False
    numeric_val = False 
    if password != password_retype:
        flash("Password not matching")
        raise Exception("Password does not match")
    elif len(password) <8:
        flash("Password needs to have more than 8 characters")
        raise Exception("Password needs to have more than 8 characters")
    for char in password:
        if char in list_numbers:
            numeric_val = True
        if char in special_characters:
            special_char = True
    if numeric_val == False:
        flash("Missing at least numeric value")
        raise Exception("Missing at least numeric value")
    if special_char == False:
        flash("Special character missing for password")
        raise Exception("Special char missing")
    if special_char and numeric_val:
        return True 


class Solution:
    def accountsMerge(self, accounts):
        #create a adjacent lists that have connections 
        dic = defaultdict(set)
        email_to_name={}
        visited = set()
        ans = []
        for account in accounts:
            name = account[0]
            for email in account[1:]:
                dic[email].add(account[1])
                dic[account[1]].add(email)
                email_to_name[email] = name

        def dfs(intial_email,dic,visited):
            if intial_email in visited:
                return 
            stack = [intial_email]
            visited.add(intial_email)
            lst = []
            lst.append(intial_email)
            while stack:
                sub_email = stack.pop()
                if dic[sub_email]:
                    for other_email in dic[sub_email]:
                        if other_email not in visited:
                            lst.append(other_email)
                            stack.append(other_email)
                            visited.add(other_email)
            result = sorted(lst)
            return result
        for email in dic:
            result = dfs(email,dic,visited)
            if result:
                ans.append([email_to_name[email]]+result)
        return ans




