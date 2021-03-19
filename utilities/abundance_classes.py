import pandas as pd
import utilities.utility_functions as ut

class PreprocessData:
    """preprocesses data"""
    def __init__(self, data, beaches, these_cols=[], foams=[], start_date="", end_date=""):
        self.data = data
        self.these_cols=these_cols
        self.foams=foams        
        self.beaches = beaches
        self.code_maps = self.make_code_maps(self.data, self.these_cols, self.foams)
        self.processed = self.add_exp_group_pop_locdate()
        self.daily_totals_all = data.groupby(these_cols, as_index=False).agg({'pcs_m':'sum', 'quantity':'sum'})
        self.median_daily_total = self.daily_totals_all.pcs_m.median()
        self.code_totals = self.data.groupby('code').quantity.sum()
        self.code_pcsm_med = self.data.groupby('code').pcs_m.median()
        
    def make_code_maps(self, data, these_cols, these_codes):
        wiw = {}
        for code in these_codes:
            a_map = data[data.code.isin(these_codes[code])].groupby(these_cols, as_index=False).agg({'pcs_m':'sum', 'quantity':'sum'})
            a_map['code']=code
            wiw.update({code:a_map})
        return wiw
    def agg_foams(self):
        accounted = [v for k,v in self.foams.items()]
        accounted = [item for a_list in accounted for item in a_list]
        remove_foam = self.data[~self.data.code.isin(accounted)].copy()
        foam = [v for k,v in self.code_maps.items()]        
        newdf = pd.concat([remove_foam, *foam])        
        return newdf
    def add_exp_group_pop_locdate(self):
        anewdf = self.agg_foams()
        anewdf['groupname'] = 'groupname'
        anewdf['population']=anewdf.location.map(lambda x: self.beaches.loc[x]['population'])
        anewdf['loc_date'] = list(zip(anewdf.location, anewdf.date))
        return anewdf

class CatchmentArea:
    """aggregates survey results"""
    def __init__(
        self,
        data,
        these_beaches,
        **kwargs):
        self.data = data
        self.beaches = these_beaches
        self.start_date = kwargs['start_date']
        self.end_date = kwargs['end_date']
        self.levels = kwargs['levels']
        self.catchment = self.levels['catchment']
        self.muni = self.levels['muni']
        self.locations_in_use = self.data.location.unique()
        self.muni_beaches = self.get_locations_by_region(self.locations_in_use, self.beaches[self.beaches.city == self.muni].index)
        self.catchment_features = kwargs['catchment_features']
        self.bassin_beaches = self.get_locations_by_region(self.locations_in_use, self.beaches[self.beaches.water_name.isin(self.catchment_features)].index)        
        self.codes_in_use = data.code.unique()
        self.group_names_locations = kwargs['code_group_data']
        self.new_code_group = kwargs['new_code_group']
        self.code_groups = self.make_code_groups()
        self.code_group_map = self.make_group_map(self.code_groups)
        self.bassin_data = self.assign_regional_labels_to_data(self.assign_code_groups_to_results(data[data.location.isin(self.bassin_beaches)].copy(), self.code_group_map), self.levels, these_beaches)
        self.muni_data = self.assign_regional_labels_to_data(self.assign_code_groups_to_results(data[data.location.isin(self.muni_beaches)].copy(), self.code_group_map), self.levels, these_beaches)
        self.bassin_code_totals = self.code_totals_regional(self.bassin_data)
        self.muni_code_totals = self.code_totals_regional(self.muni_data)
        self.bassin_code_pcsm_med = self.bassin_data.groupby('code').pcs_m.median()
        self.muni_code_pcsm_med = self.muni_data.groupby('code').pcs_m.median()
        self.bassin_pcsm_day = self.bassin_data.groupby(kwargs['catchment_cols'], as_index=False).agg({'pcs_m':'sum', 'quantity':'sum'})
        self.muni_pcsm_day = self.muni_data.groupby(kwargs['catchment_cols'], as_index=False).agg({'pcs_m':'sum', 'quantity':'sum'})        
           
    def make_group_map(self,a_dict_of_lists):
        wiw = {}
        for group in a_dict_of_lists:
            keys = a_dict_of_lists[group]
            a_dict = {x:group for x in keys}
            wiw.update(**a_dict)
        return wiw
    
    def make_code_groups(self):
        these_groups ={k:ut.json_file_get(F"output/code_groups/{v}") for k,v in self.group_names_locations.items()}
        these_groups.update(self.new_code_group)
        accounted = [v for k,v in these_groups.items()]
        accounted = [item for a_list in accounted for item in a_list]
        the_rest = [x for x in self.codes_in_use if x not in accounted]
        these_groups.update({'the rest':the_rest})
        return these_groups
    
    def assign_code_groups_to_results(self, data, code_group_map):
        data = data.copy()
        data['groupname'] = data.code.map(lambda x: code_group_map[x])
        return data
    
    def tag_regional_label(self,x, levels):
        if x in self.muni_beaches:
            a_label = self.muni
        else:
            a_label = self.catchment
        return a_label
    
    def assign_regional_labels_to_data(self, data, levels, these_beaches):
        data = data.copy()
        data['region'] = data.location.map(lambda x: self.tag_regional_label(x, self.levels))
        data['city'] = data.location.map(lambda x: these_beaches.loc[x]['city'])
        return data
    
    def code_totals_regional(self, data):
        data = data.groupby('code', as_index=False).quantity.sum()
        a_total = data.quantity.sum()
        data['% of total'] = data.quantity/a_total
        return data
    
    def get_locations_by_region(self, locations_in_use, locations_of_interest):        
        return [x for x in locations_of_interest if x in locations_in_use]