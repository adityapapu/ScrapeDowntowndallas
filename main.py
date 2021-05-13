import urllib.request
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True
driver = webdriver.Chrome(executable_path="chromedriver.exe", options=options)


def downloadImage(url, filename):
    """
    Methods to download the image
    :param url: image URL
    :param filename: File name of the image
    """
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(url, "images/" + filename + ".jpg")


def getAllHotels(url):
    """
    Method to get all hotels links
    :param url: Home page url
    """
    hotels = []
    driver.get(url)
    # identify elements with tagname <a>
    lnks = driver.find_elements_by_tag_name("a")
    # traverse list
    for lnk in lnks:
        # get_attribute() to get all href
        a = lnk.get_attribute("href")
        if "places" in a:
            hotels.append(a)
    print("All hotels links Scraped Successfully")
    return hotels


def getHotelDetails(url):
    """
    Method to scrape all details of hotel.
    :param url: link of the hotel
    """
    driver.get(url)
    img_url = driver.find_element_by_xpath("/html/body/main/div/img").get_attribute("src")
    name = driver.find_element_by_xpath("/html/body/main/article/header/h1").text
    address = driver.find_element_by_xpath("/html/body/main/article/div/div[1]/div[1]/a").text

    # Check phone number is available or not
    try:
        phone = driver.find_element_by_xpath("/html/body/main/article/div/div[1]/div[2]/div/a").text
        area = driver.find_element_by_xpath("/html/body/main/article/div/div[1]/div[3]/a").text
    except:
        phone = ""
        area = driver.find_element_by_xpath("/html/body/main/article/div/div[1]/div[2]/a").text
    downloadImage(img_url, name)
    write(name, img_url, address, phone, area)
    print(img_url + " " + name + " " + address + " " + phone + " " + area)


def write(name, img_url, address, phone, area):
    """
    Method to write the Hotel details in CSV file
    :param name: Name of the hotel
    :param img_url: Hotel image url
    :param address: Address of the hotel
    :param phone: phone number of the hotel
    :param area: area of the hotel
    :return: None
    """
    with open('Hotels.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, img_url, address, phone, area])


if __name__ == "__main__":
    url = "https://downtowndallas.com/experience/stay/"
    hotels = getAllHotels(url)

    # write the heading of the csv file
    write("Name", "Image URL", "Address", "Phone", "Area")

    for i in hotels:
        getHotelDetails(i)
    print("All Hotels details scrape Successfully")
    driver.quit()
