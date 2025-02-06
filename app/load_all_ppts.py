from PPT_Manager import PPTManager
from records import CDB
import time

cdb = CDB()
cdb.db.delete_collection('ppts')
ppt_manager = PPTManager()


# ppt_manager.pdf_files = ['../Econ_301_PPT/Chapter 2 PPT.pdf', '../Econ_301_PPT/Chapter 3 & 4 PPT.pdf']


start = time.time()
ppt_manager.populate_ppts()
end = time.time()
print(end - start)

metas = ppt_manager.cdb.ppts.get()['metadatas']
docs = ppt_manager.cdb.ppts.get()['documents']
print(ppt_manager.cdb.db.get_collection('ppts').count())

print(metas[34]['title'])
print(metas[34]['page_num'])
print(docs[34])