import os
import sqlite3

class DatabaseHandler():
    
    def __init__(self, database_name : str):
        self.connection = sqlite3.connect(f"{os.path.dirname(os.path.abspath(__file__))}/{database_name}")
        self.connection.row_factory = sqlite3.Row


    def updateFreq(self, freq : str):
        cursor = self.connection.cursor()
        query = f"INSERT INTO Letters (freq) VALUES (?);"
        cursor.execute(query, (freq))
        cursor.close()
    
        self.connection.commit()
        
        
    def getFreqNum(self):
        cursor = self.connection.cursor()
        query = f"SELECT freq_num FROM Letters WHERE freq_num = ?;"
        cursor.execute(query, (url,))
        result = cursor.fetchall()
        cursor.close()
    
        return result
        
        
    def getFreq(self):
        cursor = self.connection.cursor()
        query = f"SELECT freq FROM Letters WHERE freq = ?;"
        cursor.execute(query, (url,))
        result = cursor.fetchall()
        cursor.close()
    
        return result


    def checkUrlToVisit(self, url : str):
        cursor = self.connection.cursor()
        query = f"SELECT url FROM URLS_TO_VISIT WHERE url = ?;"
        cursor.execute(query, (url,))
        result = cursor.fetchall()
        cursor.close()

        try:
            #return dict(result[0])['url']
            return len(result) > 0
        except:
            return None
        
        
    def get1UrlsToVisitAndDeleteIt(self):
        cursor = self.connection.cursor()
        query = f"SELECT url FROM URLS_TO_VISIT;"
        cursor.execute(query)
        result = cursor.fetchall()
        try:
            query = f"DELETE FROM URLS_TO_VISIT WHERE url = '{dict(result[0])['url']}';"
            cursor.execute(query)
        except:
            print("Erreur : DELETE FROM URLS_TO_VISIT WHERE url = '{dict(result[0])['url']}';")
        cursor.close()
        
        url = ""
        
        try:
            url = str(dict(result[0])['url'])
            # print(dict(result[0])['url'])
        except:
            pass
            
        return url

    
#     def checkUrl(self, url : str):
#         cursor = self.connection.cursor()
#         query = f"SELECT url FROM Urls WHERE url = ?;"
#         cursor.execute(query, (url))
#         result = cursor.fetchall()
#         cursor.close()
# 
#         try:
#             #return dict(result[0])['url']
#             return len(result) > 0
#         except:
#             return None
#     
#     def showUrls(self):
#         cursor = self.connection.cursor()
#         query = f"SELECT url FROM Urls;"
#         cursor.execute(query)
#         result = cursor.fetchall()
#         cursor.close()
# 
#         for m in range(0, 20):
#             try:
#                 print(dict(result[m])['url'])
#             except:
#                 pass
