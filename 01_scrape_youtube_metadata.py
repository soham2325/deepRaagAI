from selenium import webdriver
import pandas as pd
import time
import logging
logging.basicConfig(filename='YT_scraping_log.log',level=logging.DEBUG,format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',datefmt='%Y-%m-%d %H:%M',)

def prepare_dataframe(a,b,c,d):
    df = pd.DataFrame({'urls':c,'title':a,'details':b, 'channel':d})
    #df['duration'] = df['details'].str.extract('([0-9]* hour{1}s{0,1}| [0-9]* hour{1}s{0,1}, [0-9]* minute{1}s{0,1} |[0-9]* minute{1}s{0,1})')
    df['ytkey'] = df['urls'].str[-11:]
    df['hours'] = df['details'].str.extract('([0-9]*) hour{1}s{0,1}').fillna(0).astype('int')
    df['minutes'] = df['details'].str.extract('([0-9]*) minute{1}s{0,1}').fillna(0).astype('int')
    df['views'] = df['details'].str.extract('([0-9]*,*[0-9]*) views')
    df['views'] = df['views'].str.replace(',',"").astype('int')
    df['age_years']=df['details'].str.extract('([0-9]*) year{1}s{0,1} ago').fillna(0).astype('int')
    df['age_months']=df['details'].str.extract('([0-9]*) month{1}s{0,1} ago').fillna(0).astype('int')
    return df

def scrape_metadata_from_youtube(textToSearch='Ahir Bhairav', maxheight=15000):
    textToSearch = textToSearch.replace(" ", "+")
    print("Quering ", textToSearch)
    url = "https://www.youtube.com/results?search_query={}&sp=EgIQAQ%253D%253D".format(textToSearch)
    print("URL to fetch: ", url)
    t0 = time.time()
    driver = webdriver.Chrome()
    driver.get(url)
    height = driver.execute_script("return document.documentElement.scrollHeight")
    lastheight = 0
    while True:
        if lastheight > maxheight:
            break
        lastheight = height
        driver.execute_script("window.scrollTo(0, " + str(height) + ");")
        time.sleep(4)
        height = driver.execute_script("return document.documentElement.scrollHeight")

    user_data = driver.find_elements_by_xpath('//*[@id="video-title"]')
    channel_data = driver.find_elements_by_xpath('//*[@id="text"]/a')
    channel_list = [x.text for x in channel_data][1::2]

    details_list = [i.get_attribute('aria-label') for i in user_data]
    url_list = [i.get_attribute('href') for i in user_data]
    title_list = [i.get_attribute('title') for i in user_data]
    logging.debug(f'Search Key: {textToSearch}')
    logging.debug('Total Time taken:{}s'.format(time.time() - t0))
    logging.debug('No. of Records scraped: ', len(user_data))
    data = prepare_dataframe(title_list, details_list, url_list, channel_list)
    # [title_list, details_list, url_list, channel_list]
    return data

#text = 'GMAT Sentence correction'
query = ['raag yaman', 'raag malakauns']
df = pd.DataFrame()
for text in query:
    df_temp = scrape_metadata_from_youtube(text,20000)
    df = pd.concat([df,df_temp],axis=0)

#df = scrape_metadata_from_youtube(text,20000)
df.to_csv('{}_youtube_scrape_metadata.csv'.format(text),index = False)