from sourcefile.User import user
from sourcefile import get_config
# d=user.register("Eswaraprasath","random_password","random_password")
try:
    user.login("Eswaraprasath","random_password")
    print("Login access")
except Exception as e:
    print("Login denied",e)