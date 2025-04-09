from GoogleNews import GoogleNews

googlenews = GoogleNews(period='1d')
googlenews.set_time_range('04/08/2025', '04/08/2025')
googlenews.search('tesla')
for i in range(1, 10):
    googlenews.getpage(i)
    for result in googlenews.results():
        print(result['title'], '-', result['media'])