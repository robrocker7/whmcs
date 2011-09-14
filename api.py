#!/usr/bin/python

from clients import WHMCSClient
from connection import APIConn

class WHMCS:
    
    data = {}

    def send_call(self):
        # this function should handle all errors
        conn = APIConn()
        resp = conn.request(self.data)
        return resp

    # CLIENT API CALLS
    def client_get_set(self, limitstart=0, limitnum=25, search=None):

        self.data['action'] = 'getclients'
        self.data['limitnum'] = limitnum
        self.data['limitstart'] = limitstart
        if search is not None:
            self.data['search'] = search

        data = self.send_call()
        clients = data['clients']['client']

        client_list = []
        for client in clients:
            client_list.append(WHMCSClient(data=client))
        return client_list

    def client_get_details(self, client_id, email=None):
        
        self.data['action'] = 'getclientsdetails'
        self.data['clientid'] = client_id
        if email is not None:
            self.data['email'] = email

        data = self.send_call()
        return WHMCSClient(data=data)

