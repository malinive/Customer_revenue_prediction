# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd 
import numpy as np
import streamlit as st
from PIL import Image
import os
import pickle

#pickle.dump(model, open('model.pkl', 'wb'))

#pickled_model = pickle.load(open('model.pkl', 'rb'))
#pickled_model.predict(x_valid)


class StreamlitApp:
    
    def __init__(self):
        self.model = pickle.load(open(r'C:\Users\malin\dat158ml-customer-revenue\model.pkl', 'rb')) 
        self.save_fn = 'path.csv' 

        
    def predict(self, input_data): 
        return predict_model(self.model, data=input_data)
    
    def store_prediction(self, output_df): 
        if os.path.exists(self.save_fn):
            save_df = pd.read_csv(self.save_fn)
            save_df = save_df.append(output_df, ignore_index=True)
            save_df.to_csv(self.save_fn, index=False)
            
        else: 
            output_df.to_csv(self.save_fn, index=False)  
            
    
    def run(self):
        #image = Image.open('assets/human-heart.jpg')
        #st.image(image, use_column_width=False)
    
    
        add_selectbox = st.sidebar.selectbox('How would you like to predict?', ('Online', 'Batch')) #bruke batch for aa predikere paa alle bildene. 
        st.sidebar.info('This app is created to predict customer revenue at Google stores.' )
        st.sidebar.success('DAT158')
        st.title('Customer revenue predicitons')
        
       
        if add_selectbox == 'Online':             
            date = st.number_input('date', min_value=1, max_value=20300101, value=100)
            visitId = st.number_input('visitId')
            totals_transactionRevenue = st.number_input('totals.transactionRevenue', min_value=0, max_value=100, value=10)
            totals_hits = st.number_input('hits', min_value=1, max_value=70000, value=1000)
            geoNetwork_subContinent = st.selectbox('geoNetwork.subContinent', ['Northern America', 'Southeast Asia', 'Southern Asia', 'Western Europe', 'Northern Europe', 'Eastern Asia', 'Eastern Europe',
                                                                               'South America', 'Southern Europe', 'Western Asia', 'Central America', 'Australasia', 'Northern Africa', 
                                                                               'Western Africa', 'Sothern Africa', 'Eastern Africa', 'Caribbean', '(not set)', 'Central Asia', 'Middle Africa', 'Micronesian Region',
                                                                               'Melanesia', 'Polynesia'])
            geoNetwork_networkDomain = st.selectbox('geoNetwork.networkDomain', ['(not set)', 'unknown.unknown', 'comcast.net', 'rr.com', 'verizon.net',
                                                                                    'dkit.ie', 'alfaisal.edu', 'bisping.de', 'wosimrwcmm.net', 'state.mn.us'])
            geoNetwork_continent = st.selectbox('geoNetwork.continent', ['Americas', 'Asia', 'Europe', 'Africa', 'Oceania', '(not set)'])
            fullVisitorId = st.number_input('fullVisitorId')
            trafficSource_source = st.selectbox('trafficSource.source', ['(direct)', 'google', 'youtube.com', 'analytics.google.com', 'Partners', 
                                                                         'search.incredibar.com', 'feedly.com', 'google.com.tw', 'my.uclaextension.edu', 'mail.aol.com'])
            
        

            

            
            output=''
            
            input_dict = {'date':date, 'visitId':visitId, 'totals.transactionRevenue':totals_transactionRevenue, 'totals.hits':totals_hits,
                          'geoNetwork.subContinent':geoNetwork_subContinent, 'geoNetwork.networkDomain':geoNetwork_networkDomain, 
                          'geoNetwork.continent':geoNetwork_continent, 'fullVisitorId':fullVisitorId, 'trafficSource.source':trafficSource_source,
                          'channelGrouping':"null", 'customDimensions':"null", 'visitNumber':0, 'visitStartTime':0, 'device.browser':"null", 
                          'device.operatingSystem':"null", 'device.isMobile':'false', 'device.deviceCategory':"null", 'geoNetwork.country':"null", 
                          'geoNetwork.region':"null", 'geoNetwork.metro':"null", 'geoNetwork.city':"null", 'totals.pageviews':"null", 
                          'trafficSource.campaign':"null", 'trafficSource.medium':"null"}
            
            input_df = pd.DataFrame(input_dict, index=[0])
        
            if st.button('Predict'): 
                output = self.predict(input_df)
                self.store_prediction(output)
                
                #output = 'Heart disease' if output['Label'][0] == 1 else 'Normal'
                #output = str(output['Label'])
                
            
            st.success('Predicted output: {}'.format(output))
            
        if add_selectbox == 'Batch': 
            fn = st.file_uploader("Upload csv file for predictions") #st.file_uploader('Upload csv file for predictions, type=["csv"]')
            if fn is not None: 
                input_df = pd.read_csv(fn)
                predictions = self.predict(input_df)
                st.write(predictions)
            
sa = StreamlitApp()
sa.run()
