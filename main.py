from __future__ import print_function
import re
import time
import datetime
import vk_api, requests
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import googleapiclient
from google.oauth2 import service_account
from googleapiclient.discovery import build

class GoogleCalendar(object):

    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/calendar']
        self.calendarId = '*google calendar id*'
        self.SERVICE_ACCOUNT_FILE = '*service account file path*'
        credentials = service_account.Credentials.from_service_account_file(self.SERVICE_ACCOUNT_FILE, scopes=self.SCOPES)
        self.service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)

    # создание события в календаре
    def create_event(self, summary, description, date):
        date_cal = date[4:]+'-'+date[2:4]+'-'+date[:2]+'T03:00:00+03:00'
        event = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': date_cal,
            },
            'end': {
                'dateTime': date_cal,
            }
        }
        e = self.service.events().insert(calendarId=self.calendarId,
                                         body=event).execute()
        print('Event created: %s' % (e.get('id')))

class Some_calculations:
    def find_the_dict_with_the_largest_value_by_keys_among_an_array_of_dictionaries_Nums(self,array=[],key=''):#только для чисел в значениях для ключа
        if array == []:
            raise Exception("The array is empty")
        if key == '':
            raise Exception("There is no key")
        max_value_of_the_key = 0
        index_of_searched_dictionary = -1
        for dict in array:
            if dict.get(key)>=max_value_of_the_key:
                max_value_of_the_key=dict.get(key)
                index_of_searched_dictionary = array.index(dict)
        if index_of_searched_dictionary == -1:
            raise Exception("Cant find")

        return index_of_searched_dictionary


    """
    [{'text':'txt','fwd':[{'text':'txt','fwd':[],'att':3}],'att':3},{'text':'txt','fwd':[{'text':'txt','fwd':[],'att':3}],'att':3}]
    """
    def find_data_or_time(self,text_buffer):#возвращает массив всех данных (текст+прикрепления к ним)
        time=''
        date=''
        for itms in text_buffer:
            datatime = (re.findall(r"\{\{(.*?)\}\}", itms) )
            if not datatime:
                continue
            else:
                for i in datatime:
                    if len(i)==8:
                        date=i
                    elif len(i)==4:
                        time=i
        return date,time

    def find_time_in_msg(self,msg_text):
        time = ''
        datatime = (re.findall(r"\{(.*?)\}", msg_text))
        if not datatime:
            return None
        for i in datatime:
            if len(i) == 4:
                time = i
                return time
        return 'u dk wgo {}'.format(datatime)

    def find_date_in_msg(self,msg_text):
        date = ''
        datatime = (re.findall(r"\{(.*?)\}", msg_text))
        if not datatime:
            return None
        for i in datatime:
            if len(i) == 8:
                date = i
                return date
        return False

    def recursive_any_list(self, array):
        lst = []
        for i in array:
            if isinstance(i, list):
                lst.extend(Some_calculations.recursive_any_list(i))
            else:
                pass
        return lst


    def recursive_txt(self, arraymsg):
        lst = []
        for array in arraymsg:
            for i in array:
                if i == 'fwd_messages' and any(array[i]):
                    lst.extend((Some_calculations.recursive_txt(self,array[i])))
                if i == 'text':
                    lst.append(array.get('text'))
        return lst

    def recursive_att(self, arraymsg):#поиск списков attachments в словаре с разной глубиной
        lst = []
        for array in arraymsg:
            for i in array:
                if i == 'fwd_messages' and any(array[i]):
                    lst.extend((Some_calculations.recursive_att(self, array[i])))
                if i == 'attachments':
                    lst.append(array.get('attachments'))
        return lst

    def Id_generator(self):
        id = int(round(time.time() * 1000))
        return id

    def Is_time(self, msg,type):#вернет тру если время напоминания пришло и оставшиесся время
        if 'RemindTimesD' in msg:
            if msg['RemindTimesD'] == []:
                return msg, False
        if 'RemindTimesH' in msg:
            if msg['RemindTimesH'] == []:
                return msg, False
        if type=='d':
            distan_time = datetime.datetime(int(msg['date'][4:]), int(msg['date'][2:4]), int(msg['date'][0:2]), 0, 0, 0, 0)
            current_time = datetime.datetime.now()
            delta_time = distan_time - current_time
            delta_time_days = delta_time.total_seconds() / 86400
            if delta_time_days <= msg['RemindTimesD'][0]:
                msg['RemindTimesD'].pop(0)
                remaining_time = delta_time_days
                return_msg = msg
                return return_msg, remaining_time
        if type=='h':
            distan_time = datetime.datetime(int(msg['date'][4:]), int(msg['date'][2:4]), int(msg['date'][0:2]), int(msg['time'][0:2]),int(msg['time'][2:4]), 0, 0)
            current_time = datetime.datetime.now()
            delta_time = distan_time - current_time
            delta_time_hours = delta_time.total_seconds() / 3600
            if delta_time_hours<=msg['RemindTimesH'][0]:
                msg['RemindTimesH'].pop(0)
                remaining_time = delta_time_hours
                return_msg = msg
                return return_msg, remaining_time
        return msg, False


    def text_constructor(self,msg,keys):#{'id':123112,'time':'1535','date':'09012020','text':'smth about msg','attachments':[url1,url2,url3,..],'RemindTimesH'/'RemindTimesD':[24,0.5]/[1]}
        text = Some_calculations.recursive_txt(self,[msg])
        reslt_msg = ''
        for i in text:
            reslt_msg+='{} \n'.format(i)
        for i in keys:
            reslt_msg=reslt_msg.replace(i,'')
        return reslt_msg

    def get_attachments_from_msg(self, msg):
        # urls = []
        attachs=[]
        attachments = Some_calculations.recursive_att(self,[msg])
        for i in attachments:
            for j in i:
                if j.get('type')=='photo':
                    dict = {}
                    dict = {'att_type':'photo',
                            'att_url':j.get('photo').get('sizes')[Some_calculations.find_the_dict_with_the_largest_value_by_keys_among_an_array_of_dictionaries_Nums(self,j.get('photo').get('sizes'), 'height')].get('url'),
                            'att_title':(str(Some_calculations.Id_generator(self)))}
                    attachs.append(dict)
                    # urls.append(j.get('photo').get('sizes')[Some_calculations.find_the_dict_with_the_largest_value_by_keys_among_an_array_of_dictionaries_Nums(self,j.get('photo').get('sizes'), 'height')].get('url'))
                if j.get('type')=='doc':
                    dict = {}
                    dict = {'att_type':'doc',
                            'att_url':j.get('doc').get('url'),
                            'att_title':j.get('doc').get('title')}
                    attachs.append(dict)
                    # urls.append(j.get('doc').get('url'))
        # return urls
        return attachs

    def msg_constructor(self,msg):

        return msg.get('text')



class Bot_discor_vk():

    def __init__(self, vk_token, vk_groupID, web_hookURL_map={}):

        self.google_calendar = GoogleCalendar()

        self.msg_buffer = []

        self.current_msg = dict.fromkeys(
            ['id', 'text', 'attachments', 'whook_url'])

        self.vk_token = vk_token

        self.vk_groupID = vk_groupID

        self.whook_url_map = web_hookURL_map

        self.somecalcs = Some_calculations()

        self.vk_session = vk_api.VkApi(token=self.vk_token)

        self.longpoll = VkBotLongPoll(self.vk_session, group_id=self.vk_groupID)

        self.embed_color = 1973951

    def send_to_discord(self, msg):
        print('\n sending msg started \n')
        channels = list(self.whook_url_map.values())
        for i in channels:
            if i == msg.get('whook_url'):
                myembeds = []
                for j in msg.get('attachments'):
                    if (j.get('att_type') == 'photo'):
                        emb = {
                            "color": self.embed_color,
                            "image": {
                                "url": j.get('att_url')
                            }
                        }
                        myembeds.append(emb)
                    if (j.get('att_type') == 'doc'):
                        emb = {
                            "color": self.embed_color,
                            "description": "[{}]({})".format(j.get('att_title'), j.get('att_url'))
                        }
                        myembeds.append(emb)

                resultWhook = {
                    "content" : msg.get('text'),
                    "embeds" : myembeds
                }

                requests.post(i, json=resultWhook)



    def Vk_LISTENER(self):
        print('listening for VK \n')
        for event in self.longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat and event.message.get('text') != "":

                print(f'recived msg: \n {event.message}\n \n')

                if any(i in event.message.get('text') for i in list(self.whook_url_map.keys())):
                    current_tag = ''
                    for i in list(self.whook_url_map.keys()):
                        if i in event.message.get('text'):
                            current_tag = i
                            break
                    self.current_msg['whook_url'] = self.whook_url_map[current_tag]
                    self.current_msg['attachments'] = self.somecalcs.get_attachments_from_msg(event.message)
                    self.current_msg['text'] = self.somecalcs.text_constructor(event.message, list(
                        self.whook_url_map.keys()))  # DELETE TAGS
                    self.current_msg['id'] = self.somecalcs.Id_generator()

                    self.msg_buffer.append(self.current_msg)

                    print(f' {self.current_msg} appended to msg_buffer[] \n NOW BUFFER IS: \n {self.msg_buffer} \n \n ')

                    if current_tag == '/DIS_TIME':
                        if Some_calculations.find_date_in_msg(self, self.current_msg['text']):
                            self.google_calendar.create_event('Some group event',self.current_msg['text'],Some_calculations.find_date_in_msg(self, self.current_msg['text']))
                        Bot_discor_vk.send_to_discord(self, self.msg_buffer.pop(0))
                    else:
                        Bot_discor_vk.send_to_discord(self, self.msg_buffer.pop(0))





#starting bot:

textTags_chaneURLs = {'/DIS_MAJOR': '*URL of the corresponding webhook*',
                    '/DIS_BOOKS': '*URL of the corresponding webhook*',
                    '/DIS_MEME': '*URL of the corresponding webhook*',
                    '/DIS_TIME': '*URL of the corresponding webhook*'}

gBot1 = Bot_discor_vk(vk_token= '*vk bots token*',
                      vk_groupID='*vk group id*',
                      web_hookURL_map=textTags_chaneURLs)

gBot1.Vk_LISTENER()