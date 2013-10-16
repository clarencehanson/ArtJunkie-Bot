'''
Created on Sep 4, 2013

@author: vostro
'''
import time
import re
import praw
master =["cityporn","Cyberpunk",'ImaginaryBattlefields','ImaginaryCityscapes','ImaginaryCityscapes','ImaginaryWastelands','IncredibleIndia',
         'ITookAPicture','IWishIWasThere','MattePainting','RoadPorn','Skyscrapers','SpecArt','StreetViewExplorers','UrbanDesign',
         'UrbanPlanning','Wallpaper','Wallpapers','WorldCities','Infrastructureporn']
posted = 0
posts = 20
done=[]
colorDict = {"earth":"a",
             "water":"b",
             "sky":"c",
             "space":"d",
             "fire":"e",
             "destruction":"f",
             "geology":"g",
             "winter":"a",
             "autumn":"b",
             "city":"c",
             "village":"d",
             "abandoned":"e",
             "infrastructure":"f",
             "machine":"g",
             "military":"a",
             "cemetery":"b",
             "architecture":"c",
             "car":"d",
             "gun":'e',
             "boat":"f",
             'streetart':'street',
             'aerial':'g',
             'f1':'a',
             'rural':'b',
             'animal':'c',
             'botanical':'d',
             'human':'e',
             'adrenaline':'f',
             'climbing':'g',
             'culinary':'a',
             'food':'b',
             'dessert':'c',
             'agriculture':'d',
             'design':'c',
             'albumart':'d',
             'movieposter':'g',
             'ad':'a',
             'geek':'b',
             'instrument':'c',
             'macro':'d',
             'art':'e',
             'fractal':'f',
             'exposure':'g',
             'micro':'a',
             'metal':'b',
             'street':'c',
             'history':'d',
             'map':'e',
             'book':'f',
             'news':'g',
             'quotes':'a',
             "future":'b',
             "room":'room'}
buildDone = True
master = "earthporn+waterporn+skyporn+spaceporn+fireporn+destructionporn+geologyporn+winterporn+autumnporn+cityporn+villageporn+abandonedporn+infrastructureporn+machineporn+militaryporn+cemeteryporn+architectureporn+carporn+gunporn+boatporn+aerialporn+F1porn+ruralporn+animalporn+botanicalporn+humanporn+adrenalineporn+climbingporn+culinaryporn+foodporn+dessertporn+agricultureporn+designporn+albumartporn+movieposterporn+adporn+geekporn+instrumentporn+macroporn+fractalporn+exposureporn+microporn+metalporn+streetartporn+historyporn+mapporn+bookporn+newsporn+quotesporn+futureporn+artporn+roomporn"
master2 = "earthporn+animalporn+cityporn+militaryporn+historyporn"

keywordDict = {"chicago":"imagesofchicago"}

subsToClone = [('adporn','ImagesOfAds',3),
               ('militaryporn','ImagesOfMilitary',10),
               ("foodporn","imagesoffood",10),
               (master,"artjunkie",20),
               ("humanporn","imagesofhumanity",posts),
               ("infrastructureporn","imagesofinfrastruct",posts),
               ("historyporn","imagesofhistory",posts),
               ("earthporn","imagesofearth",posts),
               ("cityporn","imagesofcities",posts),
               ("spaceporn","imagesofspace",posts),
               ("fireporn","imagesoffire",posts)]

introComment = """Here is a link to the original submission


"""
additionalComment = """


*Here is a comment by the original submitter*


"""
shortenComment = """Had to shorten


"""
r = praw.Reddit(user_agent='multifunctionbot')
print("logging in")
r.login()
print("logged in")
startTime = time.clock()



if buildDone:
    for a in subsToClone:
        placeToPost = a[1]
        submissions = r.get_subreddit(placeToPost).get_hot(limit = 2000)
        for s in submissions:
            done.append(s.url+placeToPost)
    timeEl = time.clock() - startTime
    print("That took %d seconds and we checked %d"%(timeEl,len(done)))

while True:
    try:
        for t in subsToClone:
            [subreddit,placeToPost,numPosts] = t
            try:
                hotGen = r.get_subreddit(subreddit).get_hot(limit=numPosts)
            except:
                print("failed to get posts from subreddit")
            for h in hotGen:
                id = str(h.url) + str(placeToPost)
                if id in done:
                    pass
                   # print("already did it")
                else:
                    if len(h.title.replace("porn","")) > 200:
                        title = h.title.replace("porn","")[:200] + "..."
                        print(shortenComment)
                    else:
                        title = h.title
                    if placeToPost == "artjunkie":
                        title= str(title) + " " + (h.subreddit.display_name.lower().replace("porn","art")) + " /u/" + str(h.author)
                    else:
                        title= str(title) + " " + " /u/" + str(h.author)
                    po=False
                    try:
                        
                        idd = r.submit(placeToPost, title.replace("porn",""), url=h.url)
                        print("posted",h.url)
                        po = True
                        posted+=1
                        done.append(h.url+placeToPost)
                        
                    except:
                        print("unable to submit",placeToPost)
                        try:
                            print(h.url)
                        except:
                            pass
                    if po: 
                        coms = h.comments
                        Comment = introComment + str(h.permalink)
                        for c in coms:
                            if type(c) is praw.objects.MoreComments:
                                print("lotta comments here...")
                            else:
                                if c.author == h.author: 
                                    Comment+=additionalComment + c.body
                        try:
                            idd.add_comment(Comment)
                        except:
                            print("Unable to comment")
                        if placeToPost == "artjunkie":
                                idd.set_flair(h.subreddit.display_name.lower().replace("porn","").capitalize(), colorDict[h.subreddit.display_name.lower().replace("porn","")])
                    if h.title.lower() in keywordDict:
                        idd = r.submit(keywordDict[h.title.lower()], title, url=h.url)
                        idd.add_comment(h.permalink)
                        
            hoursRun = (time.clock()-startTime)/60.0/60.0
            splitMaster = master.split("+")
            splitMaster = []
            for m in splitMaster:
                print("starting ",m)
                try:
                    hotGen = r.get_subreddit(m).get_hot(limit=30)
                except:
                    print("failed to get posts from subreddit")
                for h in hotGen:
                    if "chicago" in h.title.lower():
                        url = h.url
                        try:
                            id = r.submit("imagesofchicago", h.title, url=h.url)
                            id.add_comment(h.permalink)
                            print("posted",h.permalink)
                            posted+=1
                        except:
                            print("failed!")
            
            
    
        print("we have been running %.1f hours and posted %d things"%(hoursRun,posted))
        time.sleep(60*15)
    except:
        print('oops!')

                    










print("all done")
