import os
import pandas as pd
from utilities.utility_functions import json_file_get
def make_local_paths():
  """The directory structure for the repo. Returns the directory locations as variables
  """
  survey_data = os.path.join('resources', 'surveydata')
  location_data = os.path.join('resources', 'locationdata')
  code_defs = os.path.join('resources', 'mlwcodedefs')
  stat_ent = os.path.join('resources', 'statentpop')
  geo_data = os.path.join('resources', 'geodata')
  output = os.path.join('output')
  most_recent = os.path.join('resources', 'most_recent')

  return most_recent, survey_data, location_data, code_defs, stat_ent, geo_data, output

def m_ap_code_to_description(data, key, func):
  """Creates an 'item' column in a data frame. Uses specified key and method
  to assign value to 'item'.

  Args:
    data: pandas data frame
    key: dictionary or array
    func: method

  returns:
    dataframe
  """
  new_data = data.copy()
  new_data['item'] = new_data.index.map(lambda x: func(x, key))
  new_data.set_index('item', inplace=True)
  return new_data

def get_the_file_extension(x):
  """Splits a string by the '.' , returns everything after the '.'"""
  split = x.split('.')[-1]
  return split

def get_data_from_most_recent(data_sources, check_ext=get_the_file_extension, data_methods={},
                                a_dir="resources/most_recent"):
    """Retrieves files from specified directories using specified methods

    Checks the extension of the requested file and applies the the requested method.

    Args:
      data: dict
      check_ext: dict of methods for each file extension
      data_methods: methods to handle data sources

    Returns:
      The requested data stored in an array
    """
    a_list = []
    for key in data_sources:
      ext = check_ext(data_sources[key])
      method = data_methods[ext]
      my_file = method(F"{a_dir}/{data_sources[key]}")
      a_list.append(my_file)

    return a_list


def add_a_grouping_column(x, a_dict, column_to_match="", new_column_name='river_bassin'):
  """Adds a new column to a dataframe. Matches values in column_to_match to values in a_dict

  Args:
    x: dataframe
    a_dict: dict k=desired value, v=list of membership
    column_to_match: str: column name
    new_column_name:str
  Returns:
    The original data frame with a new column
  """
  for k, v in a_dict.items():
    x.loc[x[column_to_match].isin(v), new_column_name] = k
  return x

def fo_rmat_date_column(x, a_format="%Y-%m-%d"):
    """Takes in a data frame and converts the date column to timestamp."""
    x['date'] = pd.to_datetime(x['date'], format=a_format)
    return x.copy()


def slic_eby_date(x, start_date, end_date):
  """ slices a data frame by the start and end date inclusive"""
  return x[(x.date >= start_date) & (x.date <= end_date)].copy()


def fo_rmat_and_slice_date(x, a_format="", start_date="", end_date=""):
  """Formats a date column in a dataframe and slices the data frame"""
  new_df = fo_rmat_date_column(x, a_format=a_format)
  new_df = slic_eby_date(new_df, start_date, end_date)
  return new_df

class SurveyData:
    """preprocesses data"""

    def __init__(self, data, beaches, these_cols=['loc_date', 'location', 'water_name_slug', 'type', 'date'],
                 foams={'G82': ['G82', 'G912'], 'G81': ['G81', 'G911'], 'G74': ['G74', 'G910', 'G909']}, **kwargs):
      self.data = data
      self.these_cols = these_cols
      self.foams = foams
      self.beaches = beaches
      self.levels = kwargs['levels']
      self.exp_variables = kwargs['exp_variables']
      self.locations_in_use = data.location.unique()
      self.river_bassins = kwargs['river_bassins']
      self.code_maps = self.make_code_maps(self.data, self.these_cols, self.foams)
      self.codes_in_use = data.code.unique()
      self.group_names_locations = kwargs['code_group_data']
      self.code_groups = self.make_code_groups()
      self.code_group_map = self.make_group_map(self.code_groups)
      self.processed = self.add_exp_group_pop_locdate()
      self.survey_data = self.assign_code_groups_to_results(self.processed, self.code_group_map)
      self.daily_totals_all = self.survey_total_pcsm_q()
      self.median_daily_total = self.daily_totals_all.pcs_m.median()
      self.code_totals = self.survey_data.groupby('code').quantity.sum()
      self.code_pcsm_med = self.survey_data.groupby('code').pcs_m.median()

    def make_code_maps(self, data, these_cols, these_codes):
      """Returns a dictionary of the aggregated values of these_codes, grouped by these_cols.

      Args:
        data: dataframe
        these_cols: array: the columns to aggregate by
        these_codes: dict: keys=labels, values:list
      Returns:
        A dict of dataframes. Example based on the default value for foams:

        {"G82":dataframe of aggregated values, "G81":data frame of aggregated values}

      """
      wiw = {}
      for code in these_codes:
        a_map = data[data.code.isin(these_codes[code])].groupby(these_cols, as_index=False).agg(
          {'pcs_m': 'sum', 'quantity': 'sum'})
        a_map['code'] = code
        wiw.update({code: a_map})

      return wiw

    def agg_foams(self):
      """Combines the different code values for foams into the parent MLW code

      Aggregates each group of codes separately, removes original values from data and concatenates
      new values. Returns a new data frame.

      Args:
        self.foams: dict: the labels and codes to be aggregated.

      Returns:
        A new dataframe

      """
      accounted = [v for k, v in self.foams.items()]
      accounted = [item for a_list in accounted for item in a_list]
      remove_foam = self.data[~self.data.code.isin(accounted)].copy()
      foam = [v for k, v in self.code_maps.items()]
      newdf = pd.concat([remove_foam, *foam])
      # print("agg foams complet")
      return newdf

    def add_exp_group_pop_locdate(self):
      anewdf = self.agg_foams()
      anewdf['groupname'] = 'groupname'
      for beach in anewdf.location.unique():
        for variable in self.exp_variables:
          anewdf.loc[anewdf.location == beach, variable] = self.beaches.loc[beach][variable]
      anewdf['string_date'] = anewdf.date.dt.strftime('%Y-%m-%d')
      anewdf['loc_date'] = list(zip(anewdf.location, anewdf.string_date))
      this_df = self.assign_regional_labels_to_data(anewdf)

      # print("added exp vs")
      return this_df

    def make_code_groups(self):
      these_groups = {k: json_file_get(F"output/code_groups/{v}") for k, v in self.group_names_locations.items()}
      accounted = [v for k, v in these_groups.items()]
      accounted = [item for a_list in accounted for item in a_list]
      the_rest = [x for x in self.codes_in_use if x not in accounted]
      these_groups.update({'not classified': the_rest})
      # print('made code groups')
      return these_groups

    def make_group_map(self, a_dict_of_lists):
      wiw = {}
      for group in a_dict_of_lists:
        keys = a_dict_of_lists[group]
        a_dict = {x: group for x in keys}
        wiw.update(**a_dict)
      # print('making group map')
      return wiw

    def assign_code_groups_to_results(self, data, code_group_map):
      data = data.copy()
      for code in data.code.unique():
        # print(code)
        data.loc[data.code == code, 'groupname'] = code_group_map[code]
      # print('assigned results to code groups')
      return data

    def tag_regional_label(self, x, beaches):
      try:
        a_label = beaches[x]
      except:
        a_label = "no data"
      return a_label

    def assign_regional_labels_to_data(self, data):
      data = data.copy()
      for k, v in self.river_bassins.items():
        data.loc[data.water_name_slug.isin(v), 'river_bassin'] = k
      for beach in self.locations_in_use:
        data.loc[data.location == beach, 'city'] = self.beaches.loc[beach].city

      # print('assigned regional labels')
      return data

    def survey_total_pcsm_q(self):
      anewdf = self.survey_data.groupby(self.these_cols, as_index=False).agg({'pcs_m': 'sum', 'quantity': 'sum'})
      anewdf['string_date'] = anewdf.date.dt.strftime('%Y-%m-%d')
      anewdf['loc_date'] = list(zip(anewdf.location, anewdf.string_date))

      return anewdf
