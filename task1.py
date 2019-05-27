import requests 
import pprint
import json
import time
import random
from bs4 import BeautifulSoup 
import pathlib
URL = "https://www.imdb.com/india/top-rated-indian-movies/"
res = requests.get(URL)
soup = BeautifulSoup(res.text,"html.parser")
div = soup.find('div', class_='lister')
tbody = div.find('tbody', class_='lister-list')
trs = tbody.find_all('tr')
def scrape_top_list():
    dic_list = []
    i = 0
    for tr in trs: 
        dic = {}
        i = i + 1
        name = tr.find('td', class_= 'titleColumn').a.get_text()
        year = tr.find('td', class_= 'titleColumn').span.get_text()
        url_movies = tr.find('td', class_='titleColumn').a['href']
        link =  'https://www.imdb.com' + url_movies
        rate = tr.find('td', class_= 'ratingColumn imdbRating').strong.get_text()
        dic['year']= int(year[1:5])
        dic['rATE'] = float(rate)
        dic['POSTION'] = int(i)
        dic['name'] = str(name)
        dic['url']= str(link)
        # print (dic)
        dic_list.append(dic)
    return dic_list
top_movies = (scrape_top_list()) 
# pprint.pprint (top_movies)

# task2
def group_by_year(movie):
    dat = {}
    for i in movie :
        year = i["year"]
        if(not i.get(year)):
            dat[year] = []
        dat[year].append(i)
    return dat
movies_by_year  = (group_by_year(top_movies))
pprint .pprint (movies_by_year )

# task 12
def scrape_movie_cast(movie_caste_url, id):
        # print (movie_caste_url)
        # print (id)
        filename = 'movie_cast/' +id + '_cast.json'
        filepath =  pathlib.Path(filename)
        if filepath.exists():
            with open (filename, 'r') as f:
            # with open('/home/rupa/Documents/we_screping/movie_cast/'+ filename, 'r') as f:
                # print ("file exsits hai")os.path.exists('/home/rupa/Documents/we_screping/movie_cast/'+
                file_read = f.read()
                # print (f)
                print ("file hai")
                data= json.loads(file_read)
            return  data
        else:
            # print ("file nahi exsits hai")
            list1 = []
            resp = requests.get(url)
            soup = BeautifulSoup(resp.text,"html.parser")
            table = soup.find('table', class_='cast_list')
            aTag = table.find_all('td', class_='')
            for actor in aTag:
                dic = {}
                id = actor.find('a').get('href')[6:15]
                name = actor.find('a').get_text().strip()
                dic['imbd id'] = id
                dic['imbd name'] = name
                list1.append(dic)
            with open(filename, 'w') as f:
                f.write(json.dumps(list1, f,indent=1))
            return list1

for data in top_movies:
    url = data['url'] 
    movieId = ''
    for j in url[27:]:
        if '/' not in j:
            movieId += j
        else:
            break 
    # url_cast = url+'fullcredits?ref_=tt_cl_sm#cast' 
    scrape_movie_cast_call = (scrape_movie_cast(url,movieId))     

# task 4 
def movie_list_details_10(movie_list):
        dic = {}  
        # task8
        movieId = ''
        for j in movie_list[27:]:
            if '/' not in j:
                movieId += j
            else:
                break    
        fileName = 'MovieName/'+movieId + '.json'
        filepath =  pathlib.Path(fileName)
        # print (filepath)
        if filepath:
            print ("file hai")
            with open(fileName, 'r') as f:
                f = f.read()
                data= json.loads(f)
                print(f)
            return f
                
        else:
            print  ("nahi hai")  
            resp = requests.get(movie_list)
            soup1 = BeautifulSoup(resp.text,"html.parser")
            name = soup1.find('div', class_='title_wrapper').h1.get_text()
            empty_str = ''
            for i in name:
                if "(" not in i:
                    empty_str = (empty_str+i).strip()
                else:
                    break
            gerne = soup1.find('div' , class_='subtext')
            a_tag = gerne.find_all('a')
            a_tag.pop()
            gerne_list = [ i.get_text() for i in  a_tag]
            print (gerne_list)   
            summary = soup1.find('div', class_= 'plot_summary')
            bio = summary.find('div', class_= 'summary_text').get_text().strip()
            director = summary.find('div', class_="credit_summary_item")
            directorList =   director.find('a')
            directorLists = [directorList.get_text()  for dir in  directorList ] 
            main_div = soup1.find('div', attrs={"class" :'article', "id" :'titleDetails'})
            div = main_div.find_all('div')
            for div1 in div:
                tag_h4 = div1.find_all('h4')
                for tag in tag_h4:
                    if "Country:" in tag:
                        acho = div1.find_all('a')
                        moviesCountry = ([country.get_text() for country in acho])
                    elif "Language:" in tag:
                        lan = div1.find_all('a')
                        moviesLanguage = ([language.get_text() for language in lan])
                    elif "Runtime:"  in tag:
                        run = div1.find('time').get_text().strip()
                        dic['runtime'] = run
            poster = soup1.find('div', class_='poster').a['href']
            movie_poster = "https://www.imdb.com" + poster
        
            dic['name'] = empty_str
            dic['director'] = directorLists 
            dic['country'] = div
            dic['language'] = moviesLanguage
            dic['country'] =  moviesCountry
            dic['bio'] = bio
            dic['poster'] = movie_poster
            dic['genre'] =  gerne_list 
            # task13
            caste = scrape_movie_cast(url,movieId)
            dic['caste'] = caste
            # task 8
            with open(fileName, 'w') as file1:
                file1.write(json.dumps(dic, indent=1))  
            return dic 
# task5
def get_all_movie_list_details(moviesList):
    # task9
    ramdom_time = random.randint(1,3)
    print (ramdom_time)
    t = time.sleep(ramdom_time)
    listOFmovie = []
    for i in moviesList[:250]:
        url = i['url']
        movieDetailCall = movie_list_details_10(url)  
        listOFmovie .append(movieDetailCall)
    return  listOFmovie 
data=get_all_movie_list_details(top_movies)
# pprint.pprint(data)

# task6
def analyse_movies_language(movies_language_list):
    language_list = []
    for movie in movies_language_list:
        json_lang =  json.loads(movie)
        lang =  json_lang['language']
        language_list.extend(lang)
        language_dic = {}
        for langu in language_list:
            if langu not in language_dic:
                language_dic[langu] = 1
            else:
                language_dic[langu] += 1
    return language_dic

movies_language_count = analyse_movies_language(data)
# pprint.pprint (movies_language_count )

# #  task7
def  analyse_movies_directors(movies_detail_list):
    movie_directors_list=[]
    for movieDirector in movies_detail_list:
            json_dir = json.loads(movieDirector)
            direct = json_dir['director'] 
            movie_directors_list.extend(direct)
            movie_directors_dic = {}
            for direc in  movie_directors_list:
                if direc not in  movie_directors_dic:
                    movie_directors_dic[direc]= 1
                else:
                    movie_directors_dic[direc] +=1
            
    return movie_directors_dic

movieDirectorCount =  analyse_movies_directors(data)  
# pprint.pprint (movieDirectorCount)
# task10
def analyse_language_and_directors(movie_list):
    detailDirector = {}
    for movie in movie_list:
        json_dir = json.loads(movie)
        for dirtecor in json_dir['director']:
            detailDirector[dirtecor] ={}
    for movie in movie_list:
        json_direc = json.loads(movie)
        for dirtecor in json_direc['director']:  
            for lang in json_direc['language']:
                if dirtecor in detailDirector:
                    detailDirector[dirtecor][lang] = 0
    for movie in movie_list:
        json_direct = json.loads(movie)
        for dirtecor in json_direct['director']:  
            for lang in json_direct['language']:
                if dirtecor in  detailDirector:
                    detailDirector[dirtecor][lang] += 1                
    return  detailDirector 
pprint.pprint (analyse_language_and_directors(data))


# task 11
def analyse_movies_genre(movie_list):
    gerne_list = []
    for movie in movie_list:
        json_dic = json.loads(movie)
        gerne = json_dic['genre'] 
        gerne_list .extend(gerne)
        gerne_dic = {}
        for data in gerne_list:
            if data not in  gerne_dic :
                gerne_dic [data] = 1
            else:
                gerne_dic [data] += 1 
    return  gerne_dic 
pprint.pprint (analyse_movies_genre(data))  
     
# task15
def analyse_actors(movies_detail_list):
    actors_total_movie = {}
    for i in movies_detail_list:
        jso_load = json.loads(i)
        jso_caste = jso_load['caste']
        for j in jso_caste:
            caste_id = j['imbd id']
            caste_name = j['imbd name']
            if caste_id in actors_total_movie:
                dic['num_movie'] +=  1
            else:
                actors_total_movie[caste_id] = {}
                dic =  actors_total_movie[caste_id]
                dic['name'] = caste_name
                dic['num_movie'] = 1
    return  actors_total_movie     
pprint. pprint (analyse_actors(data))




























