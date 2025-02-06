from PPT_Manager import PPTManager

ppt_manager = PPTManager()

results = ppt_manager.query('What is an indifference curve?')
for i in range(len(results['titles'])):
    print(results['titles'][i])
    print(results['page_nums'][i])
    print(results['texts'][i])
    