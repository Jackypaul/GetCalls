from selenium import webdriver                                                                          
from selenium.common.exceptions import NoSuchElementException                                           
from selenium.webdriver.common.keys import Keys                                                         
from bs4 import BeautifulSoup                                                                           
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

binary = FirefoxBinary('/usr/bin/firefox')                                                              
browser = webdriver.Firefox(firefox_binary=binary)                                                      
                                                                                                        
browser.get('http://ec.europa.eu/research/participants/portal/desktop/en/opportunities/h2020/topics/dt-transformations-11-2019.html')                                                                                       
html_source = browser.page_source                                                                       
browser.quit()
soup = BeautifulSoup(html_source,'html.parser')
print(soup.prettify())
