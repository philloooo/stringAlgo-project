# matt.joyce@gmail.com
# April 2007
#


def gradient((r1,g1,b1),(r2,g2,b2),steps):
    colour_list=[]
    for i in range(0,int(steps),1):
        amount=i/float(steps)
        colour_list.append(RGBinterpolate((r1,g1,b1),(r2,g2,b2),amount))
    return colour_list

def RGBinterpolate((r1,g1,b1),(r2,g2,b2),f_amount):
    """ take two rgb tuples, interpolate and return an rgb tuple"""
    rn=int(r1+(f_amount * (r2-r1)))
    gn=int(g1+(f_amount * (g2-g1)))
    bn=int(b1+(f_amount * (b2-b1)))
    return (rn,gn,bn)

def RGBToHTMLColor(rgb_tuple):
    """ convert an (R, G, B) tuple to #RRGGBB """
    hexcolor = "#%02x%02x%02x" % rgb_tuple
    return hexcolor

def RGBtoFloat((r,g,b)):
    return ((r/float(255),g/float(255),b/float(255)))

def HTMLColorToRGB(colorstring):
    """ convert #RRGGBB to an (R, G, B) tuple """
    colorstring = colorstring.strip() 
    if colorstring[0] == '#':
	colorstring = colorstring[1:]
    if len(colorstring) != 6:
        raise ValueError, "input #%s is not in #RRGGBB format" % colorstring     
    r, g, b = colorstring[:2], colorstring[2:4], colorstring[4:]
    r, g, b = [int(n, 16) for n in (r, g, b)]
    return (r, g, b)
