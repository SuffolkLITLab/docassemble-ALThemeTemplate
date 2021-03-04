#####################################
# Package for a very simple / MVP list of courts that is mostly signature compatible w/ MACourts for now

from docassemble.base.util import path_and_mimetype, Address, LatitudeLongitude, DAStaticFile, markdown_to_html, prevent_dependency_satisfaction, DAObject, DAList, DADict, log, space_to_underscore
from docassemble.base.legal import Court
import pandas as pd
import os
#import io, json, sys, requests, bs4, re, os
# from docassemble.webapp.playground import PlaygroundSection
#import usaddress
#from uszipcode import SearchEngine
#from collections.abc import Iterable

class ALCourt(Court):
    """Object representing a court in Massachusetts.
    TODO: it could be interesting to store a jurisdiction on a court. But this is non-trivial. Should it be geo boundaries?
    A list of cities? A list of counties? Instead, we use a function on the CourtList object that filters courts by
    address and can use any of those three features of the court to do the filtering."""
    def init(self, *pargs, **kwargs):
        super(ALCourt, self).init(*pargs, **kwargs)
        if 'address' not in kwargs:
            self.initializeAttribute('address', Address)
        if 'jurisdiction' not in kwargs: # This attribute isn't used. Could be a better way to handle court locating
            self.jurisdiction = list()
        if 'location' not in kwargs:
            self.initializeAttribute('location', LatitudeLongitude)

    def __str__(self):
        return str(self.name)
      
    def _map_info(self)->str:
        the_info = str(self.name)
        the_info += "  [NEWLINE]  " + self.address.block()
        result = {'latitude': self.location.latitude, 'longitude': self.location.longitude, 'info': the_info}
        if hasattr(self, 'icon'):
            result['icon'] = self.icon
        return [result]
      
    def short_label(self)->str:
      """
      Returns a string that represents a nice, disambiguated label for the court.
      This may not match the court's name. If the name omits city, we
      append city name to the court name. This is good for a drop-down selection
      list.
      """
      if self.address.city in str(self.name):
        return str(self.name)
      else:
        return str(self.name) + ' (' + self.address.city + ')'
    
    def short_label_and_address(self)->str:
      """
      Returns a markdown formatted string with the name and address of the court.
      More concise version without description; suitable for a responsive case.
      """
      return '**' + self.short_label() + '**' + '[BR]' + self.address.on_one_line()
    
    def short_description(self)->str:
      """
      Returns a Markdown formatted string that includes the disambiguated name and 
      the description of the court, for inclusion in the results page with radio
      buttons.
      """
      return '**' + self.short_label() + '**' + '[BR]' + self.address.on_one_line() + '[BR]' + self.description
  
    def from_row(self, df_row)->None:
      """
      Loads data from a single Pandas Dataframe into a court object.
      Note: It will try to convert column names that don't make valid
      attributes. Best practice is to use good attribute names (no spaces) that don't interfere
      with existing attributes or methods of DAObject
      """
      # A few columns we expect to see:
      # name
      # address_address
      # address_city. Optionally: address_unit, address_zip, address_county, etc. Follow Address object
      # attribute conventions, but with address_ as prefix.
      # Optional:
      # location_latitude and location_latitude will fill the location.latitude/longitude attributes
      # Other columns will be turned into arbitrary attributes if possible, followed by transforming
      # underscores.
      if 'location_latitude' in df_row:
        self.location.latitude = df_row['location_latitude']
      if 'location_longitude' in df_row:        
        self.location.longitude = df_row['location_longitude']
      for attribute_candidate in set(df_row.keys()) - {'location_latitude','location_longitude'}:
        if attribute_candidate.startswith('address_') and attribute_candidate.isidentifier():
          setattr(self.address, attribute_candidate[8:], df_row[attribute_candidate])
        else:
          if attribute_candidate.isidentifier():
            setattr(self, attribute_candidate, df_row[attribute_candidate])
          else:
            try:
              setattr(self, space_to_underscore(attribute_candidate), df_row[attribute_candidate])
            except:
              log('Skipping invalid column name in court list: ' + attribute_name)
              pass # People really need to use sensical column names that can be converted to attributes
                   # but we don't need to throw an exception about it.
                  
      
class ALCourtLoader(DAObject):
  """
  Object to hold some methods surrounding loading/filtering courts.
  
  Built around Pandas dataframe.
  """

  def filter_courts(self, court_types):
    """
    Return a subset of courts. 
    """
    df = self._load_courts()
    return df['name'].items()
    
  def as_court(self, intrinsicName, index):
    court = ALCourt(intrinsicName)
    df = self._load_courts()    
    #try:
    row = df.loc[int(index)]
    #except:
    #  return None
    court.from_row(row)
    return court    
  
  def _load_courts(self):
    """
    Return list of courts 
    """
    if "/" in self.file_name:
      to_load = path_and_mimetype(self.file_name)[0]
    else:
      to_load = path_and_mimetype(os.path.join("data/sources", self.file_name))[0]
    
    # TODO: this could be a place to allow handling other data formats, like JSON or CSV
    df = pd.read_excel(to_load)
    return df
    