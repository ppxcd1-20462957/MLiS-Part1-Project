import pandas as pd


class Preprocess():
    def __init__(self):
        sea_ice_data = pd.read_csv('D:/OneDrive/Desktop/N_seaice_extent_daily_v3.0.csv')
        sea_ice_data = sea_ice_data.drop(index = 0, axis = 0)
        sea_ice_data = sea_ice_data.rename(columns = lambda x: x.strip())
        sea_ice_data = sea_ice_data.drop(columns = ['Month', 'Day', 'Missing', 'Source Data'], axis = 1)
        sea_ice_data = self.sea_ice_averages(sea_ice_data)

        co2_data = pd.read_csv('D:/OneDrive/Desktop/co2_mm_mlo.csv')
        co2_data = co2_data.rename(columns = lambda x: x.strip())
        co2_data = co2_data.drop(columns = ['month', 'decimal date', 'de-seasonalized', '#days', 'st.dev of days', 'unc. of mon mean'], axis = 1)
        co2_data = self.co2_averages(co2_data)
        co2_data = co2_data.loc[co2_data['year'] > 1977]
        co2_data = co2_data.reset_index()

        celsius_data = pd.read_csv('D:/OneDrive/Desktop/graph.csv')
        celsius_data = celsius_data.rename(columns = lambda x: x.strip())
        celsius_data = celsius_data.drop(columns = ['Lowess(5)'], axis = 1)
        celsius_data = celsius_data.loc[celsius_data['Year'] > 1977]
        celsius_data = celsius_data.append(pd.DataFrame({'Year': [2022],
                                          'No_Smoothing': [0.84] #interpolated as 2021 value, assuming the data follows a trend
                                         }))
        celsius_data = celsius_data.reset_index()                             

        all_data = sea_ice_data
        all_data['Global CO2'] = co2_data['monthly average']
        all_data['Temp Diff From Average'] = celsius_data['No_Smoothing']
        
        #min max normalisation
        all_data['Extent'] = (all_data['Extent'] - all_data['Extent'].min()) / (all_data['Extent'].max() - all_data['Extent'].min()) 
        all_data['Global CO2'] = (all_data['Global CO2'] - all_data['Global CO2'].min()) / (all_data['Global CO2'].max() - all_data['Global CO2'].min())
        all_data['Temp Diff From Average'] = (all_data['Temp Diff From Average'] - all_data['Temp Diff From Average'].min()) / (all_data['Temp Diff From Average'].max() - all_data['Temp Diff From Average'].min()) 

        print(sea_ice_data.head)
        print(all_data.head)
    
    def sea_ice_averages(self, sea_ice_data):
        sea_ice_data['Year'] = pd.to_numeric(sea_ice_data['Year'])
        sea_ice_data['Extent'] = pd.to_numeric(sea_ice_data['Extent'])
        
        unique_vals = pd.unique(sea_ice_data['Year'])

        yearly_averages = []
        for i in unique_vals:
            x = 0
            y = 0
            for index, row in sea_ice_data.iterrows():
                if row['Year'] == i:
                    x += row['Extent']
                    y += 1
                    sea_ice_data = sea_ice_data.drop(index, axis = 0)
                else:
                    break
            yearly_averages.append(x / y)

        sea_ice_data['Year'] = unique_vals
        sea_ice_data['Extent'] = yearly_averages

        return sea_ice_data

    def co2_averages(self, co2_data):
        co2_data['year'] = pd.to_numeric(co2_data['year'])
        co2_data['monthly average'] = pd.to_numeric(co2_data['monthly average'])
        
        unique_vals = pd.unique(co2_data['year'])

        yearly_averages = []
        for i in unique_vals:
            x = 0
            y = 0
            for index, row in co2_data.iterrows():
                if row['year'] == i:
                    x += row['monthly average']
                    y += 1
                    co2_data = co2_data.drop(index, axis = 0)
                else:
                    break
            yearly_averages.append(x / y)

        co2_data['year'] = unique_vals
        co2_data['monthly average'] = yearly_averages

        return co2_data

def main():
    Preprocess()

if __name__ == '__main__':
    main()
