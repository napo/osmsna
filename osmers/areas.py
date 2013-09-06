from shapely.geometry.polygon import LinearRing
import requests

class HDYC():
    BASEURL = "http://hdyc.neis-one.org/user/"
    def decode(self,a, c):
      #a= a.replace("\\\\","\\")
      c = pow(10,-c)
      e = len(a)
      f = 0
      l = 0
      polygon = []
      d = 0
      while(d<e):
        b = 0
        g = 0
        while True:
            h = ord(a[d]) - 63
            d += 1
            g |= (h&31) <<b
            b += 5
            if(g & 1):
                f += ~ (g >> 1)
            else: 
                f += g >> 1
            if (h<32):
                break
        g = 0
        b = 0
    
        while True:
            h = ord(a[d]) - 63
            d += 1
            g |= (h&31) <<b
            b += 5
            if(g & 1):
               l += ~ (g >> 1)
            else: 
               l += g >> 1
            if (h<32):
                break
    
        polygon.append(((f * c), (l * c)))
      return polygon
      
    def center(self,polygon):
        polygon = list(polygon)
        ring = LinearRing(polygon)
        center = ring.centroid
        return ([center.x,center.y])

    def user_data(self,username):
        url = self.BASEURL + username
        res = requests.get(url)
        
        if res.ok:
            data = res.json()
    
        return data


    def centroid(self,username):
    
        data = self.user_data(username)
    
        activityarea = data.get('activtyarea', None)
    
        polygon = None
        if activityarea:
            try:
                polygon = self.decode(activityarea)
            except:
                pass
    
        if polygon:
            return self.center(polygon)
        else:
            return []

if __name__ == '__main__':
    hdyc = HDYC()
    print "Get centroid for user 'Roman Fischer'"
    print hdyc.centroid("Roman Fischer")
    userdata = hdyc.user_data("Cesare")
    print userdata
    print userdata['changesets']
    YEAR=2013
    days_years = {}
    for yd in range(2004,YEAR+1):
         days_years[str(yd)] = 0

    if userdata.has_key('changesets'):      
         mapping_days = userdata['changesets']['mapping_days']
         years = mapping_days.split(";")
         tmp_years = {}
         for year in years:
             y,d = year.split("=")
             tmp_years[y]=d
         for yd in range(2004,YEAR+1):
              try:
                 days_years[str(yd)]=tmp_years[str(yd)]
              except Exception:
                 pass
         for yd in range(2004,YEAR+1):
                 #g.node[uid][str(yd)]=days_years[str(yd)]
                 print days_years[str(yd)]


