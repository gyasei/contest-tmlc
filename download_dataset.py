import requests

auth=('akovskiboy@gmail.com', 'e19bd2f5234ab55170a1b0bcdb0aee02')


if __name__ == '__main__':
    x = 7
    resp = requests.get('http://challenges.tmlc1.unpossib.ly/api/datasets/tmlc1-scoring-00%d.json'%x, auth=auth)
    print resp.status_code
    with open('../data/score/tmlc1-scoring-00%d.json'%x, 'w') as f:
        f.write(resp.content)
    #for i in range(1, 2):
        #resp = requests.get('http://challenges.tmlc1.unpossib.ly/api/datasets/tmlc1-training-%02d.tar.gz'%i, auth=auth)
        #print i, resp.status_code
        #with open('train-%02d.tar.gz'%i, 'wb') as f:
            #f.write(resp.content)

    #for i in range(1, 5):
        #resp = requests.get('http://challenges.tmlc1.unpossib.ly/api/datasets/tmlc1-testing-%02d.tar.gz'%i, auth=auth)
        #print i, resp.status_code
        #with open('test-%02d.tar.gz'%i, 'wb') as f:
            #f.write(resp.content)

    #for i in range(1, 9):
        #resp = requests.get('http://challenges.tmlc1.unpossib.ly/api/datasets/tmlc1-testing-full-%02d.tar.gz'%i, auth=auth)
        #print i, resp.status_code
        #with open('test-full-%02d.tar.gz'%i, 'wb') as f:
            #f.write(resp.content)



