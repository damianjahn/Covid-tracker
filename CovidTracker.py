from selenium import webdriver
import pandas as pd
from time import sleep
from twilio.rest import Client


# sms function
def send_sms(total_cases, new_cases, total_deaths, new_deaths, active_cases, total_recovered, serious_critical):
    account_sid = 'your account_sid'
    auth_token = 'your auth_token'
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
            body=f"The today report of COVID-19 in Poland. Total Cases: {total_cases}, New Cases: {new_cases}, Total "
                 f"deaths: {total_deaths}, New deaths: {new_deaths}, Active cases: {active_cases}, Total recove"
                 f"red: {total_recovered}, Serious critical cases: {serious_critical}",
            from_='Twilio number',
            to='number'
        )


# start up the webdriver and create a dataframe
class VirusBot:
    def __init__(self):
        self.driver = webdriver.Chrome()
        # define csv file columns
        columns = ['total_cases', 'new_cases', 'total_deaths', 'new_deaths', 'active_cases', 'total_recovered',
                   'serious_critical']
        self.df = pd.DataFrame(columns=columns)

    # tracker function to locate elements
    def tracker(self):
        # telling the driver what web page to open
        website = self.driver.get('https://worldometers.info/coronavirus/')
        sleep(5)
        # storing the table element in a variable
        table = self.driver.find_element_by_xpath('//*[@id="main_table_countries_today"]')
        # specifying what country you want to analyze
        country = table.find_element_by_xpath("//td[contains(., 'Poland')]")
        # specifying the country row
        row = country.find_element_by_xpath("./..")
        # formatting the columns
        cell = row.text.split(" ")

        # scraping each row cell for "Poland"
        self.total_cases = cell[2]
        self.new_cases = cell[3]
        self.total_deaths = cell[4]
        self.new_deaths = cell[5]
        self.active_cases = cell[6]
        self.total_recovered = cell[7]
        self.serious_critical = cell[8]

        # append results to columns in dataframe
        self.df = self.df.append(
            {'total_cases': self.total_cases,
             'new_cases': self.new_cases,
             'total_deaths': self.total_deaths,
             'new_deaths': self.new_deaths,
             'active_cases': self.active_cases,
             'total_recovered': self.total_recovered,
             'serious_critical': self.serious_critical}, ignore_index=True)

    # export function to create the CSV file
    def scrape_to_csv(self):
        self.df.to_csv('scraped_data.csv')

        send_sms(self.total_cases, self.new_cases, self.total_deaths, self.new_deaths, self.active_cases,
                 self.total_recovered, self.serious_critical)

        # close the web driver when results are reported
        self.driver.close()


# calling functions
bot = VirusBot()
bot.tracker()
bot.scrape_to_csv()
