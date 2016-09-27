import pnrapi
p = pnrapi.PnrApi("1234567890") #10-digit PNR Number
if p.request() == True:
    response = p.get_json()
    print response
else:
    print "Service unavailable"