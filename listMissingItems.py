import sys, json, collections

def printif(txt,hd): #{{{
     #print type(txt),txt
     if isinstance(txt, unicode) or isinstance(txt, str):
         if len(txt) == 0 or txt[0] == "?" or txt[0] == "_":
             print hd+": '"+txt+"'"
#}}}

  
def decoder(ix1,head): #{{{
    for j,rk in enumerate(ix1): 
        rv = ix1[rk]
        if isinstance(rv, collections.OrderedDict): 
            decoder(rv, head+rk+"::")
        elif isinstance(rv, unicode) or isinstance(rv, str):
            printif(rv,"        "+head+rk)
        elif isinstance(rv, list):
            for k,rvv in enumerate(rv): 
                printif(rvv,"        "+head+"::"+rk+"["+str(int(k))+"]")
        else:
            print rk, type(rv), rv
#            decoder(rv, head+"|"+rk+"["+str(int(k))+"]")
            sys.exit(1)
#}}}
    

inp = json.loads(sys.stdin.read(), object_pairs_hook=collections.OrderedDict)

for i,ix in enumerate(inp):
    print i+1,":  "+ix["varname"]
    decoder(ix, "")

sys.exit(0)
