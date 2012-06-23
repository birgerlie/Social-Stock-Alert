import datasift


DATASIFT_USERNAME = "birgerlie"
DATASIFT_API_KEY = "2037314f05036b9b1805c91b7eeda220"

dsl = open('dsl_definition.txt', 'r').read

user = datasift.User(DATASIFT_USERNAME, DATASIFT_API_KEY)
print usr

definition = usr.create_definition(csdl)





