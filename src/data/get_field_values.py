# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path

from bs4 import BeautifulSoup
import lxml
import os


class Codes:
    def __init__(self):
        self.na_code = ""

def main():
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """

    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')

    # TEST functions
    # Try to extract fields from all files in a directory and report success/failure
    extract_fields_test_all()
    # Try to extact fields from a specific page_source
    extract_fields_test("../../data/raw/page_sources/page_source4781")


    print(os.getcwd())


def extract_fields_test_all():
    num_errors = 0
    total = len(os.listdir("../../data/raw/page_sources/"))
    for myfile in os.listdir("../../data/raw/page_sources/"):
        try:
            out = extract_fields("../../data/raw/page_sources/" + myfile)
            # print(out)
        except Exception as e:
            print(myfile)
            print(e)
            num_errors += 1
    print(total, num_errors)
    return out

def extract_fields_test(myfile: str):
    out = extract_fields(myfile)
    for k, v in out.items():
        print(k, v)


def extract_fields(myfile):
    soup = make_soup(myfile)
    div_grind_container, section_main_content = get_main_sections(soup)


    # info at the top: price, # of bed & bath, sqft etc.
    price = get_price(soup)
    bed = get_num_beds(soup)
    bath = get_num_baths(soup)
    sqft = get_sqft(soup)
    if div_grind_container is not None:
        area = get_area(div_grind_container)
        zipcode = get_zipcode(div_grind_container)
        address = get_address(div_grind_container)
    else:
        area, zipcode, address = [Codes().na_code] * 3
    date_sold = get_date_sold(soup)
    # info in the bottom: home_type, sqft, lot_size, year_built
    home_type, lot_size, sqft_price, year_built, hoa_fee, all_home_features = get_home_features(section_main_content)
    # get tax_amount, and text
    tax_amount = get_tax_amount(soup)
    description = get_description(soup)
    realtor_description = get_realtor_description(soup)

    features = {"price": price,
                "bed": bed,
                "bath": bath,
                "sqft": sqft,
                "area": area,
                "zipcode": zipcode,
                "address": address,
                "date_sold": date_sold,
                "home_type": home_type,
                "sqft_price": sqft_price,
                "lot_size": lot_size,
                "year_built": year_built,
                "hoa_fee": hoa_fee,
                "all_home_features": all_home_features,
                "tax_amount": tax_amount,
                "description": description,
                "realtor_description": realtor_description
                }
    return features


def get_realtor_description(soup):
    realtor_description_obj = soup.find('div',
 {'data-testid': 'home-description-text-description-text'})
    realtor_description = get_text_if_obj_defined(realtor_description_obj)
    return realtor_description


def get_description(soup):
    description_obj = soup.find('div', {'data-testid': 'home-description-text-description-sub-header'})
    description = get_text_if_obj_defined(description_obj)
    return description


def get_tax_amount(soup):
    tax_obj = soup.find(text='Tax')
    if tax_obj is not None:
        tax = get_text_if_obj_defined(tax_obj.findNext())
    else:
        tax = Codes().na_code
    return tax


def get_home_features(section_main_content):
    home_type, lot_size, sqft_price, year_built, hoa_fee = [Codes().na_code] * 5
    all_home_features = []
    if section_main_content is not None:
        home_features_list = section_main_content.find('ul', {'data-testid': 'home-features'})

        if home_features_list is not None:
            home_feature_list_items = home_features_list.find_all('li',
                                                                  {'class': 'FeatureList__FeatureListItem-iipbki-0 '
                                                                            'fKDDGQ'})
            for home_feature in home_features_list:
                feature = get_text_if_obj_defined(home_feature)
                all_home_features.append(feature)
                if "Lot Size" in feature:
                    lot_size = feature
                elif "Built in" in feature:
                    year_built = feature
                # TODO: Get the list of possible home types
                elif any(elem in feature for elem in ["Single Family Home", "Condo"]):
                    home_type = feature
                elif "/sqft" in feature:
                    sqft_price = feature
                elif "HOA" in feature:
                    hoa_fee = feature

    return home_type, lot_size, sqft_price, year_built, hoa_fee, all_home_features


def get_date_sold(soup):
    date_sold_obj = soup.find('div',
                              {'class': 'Text__TextBase-sc-1i9uasc-0-div Text__TextContainerBase-sc-1i9uasc-1 cERLyX'})
    date_sold = get_text_if_obj_defined(date_sold_obj)
    return date_sold


def get_address(div_grind_container):
    find_all = div_grind_container.find_all('span')
    address_obj = get_element_or_none(find_all, element=1)
    address = get_text_if_obj_defined(address_obj)
    return address


def get_zipcode(div_grind_container):
    find_all = div_grind_container.find_all('span')
    zipcode_obj = get_element_or_none(find_all, element=1)
    zipcode = get_text_if_obj_defined(zipcode_obj)
    return zipcode


def get_area(div_grind_container):
    area_obj = div_grind_container.find('a')
    area = get_text_if_obj_defined(area_obj)
    return area


def get_sqft(soup):
    find_all = soup.find_all('li', {'data-testid': 'floor'})
    sqft_obj = get_element_or_none(find_all, element=1)
    sqft = get_text_if_obj_defined(sqft_obj)
    return sqft


def get_num_baths(soup):
    find_all = soup.find_all('li', {'data-testid': 'bath'})
    bath_obj = get_element_or_none(find_all)
    bath = get_text_if_obj_defined(bath_obj)
    return bath


def get_element_or_none(find_all, element=1):
    if len(find_all) > 0:
        bath_obj = find_all[element]
    else:
        bath_obj = None
    return bath_obj


def get_num_beds(soup):
    find_all = soup.find_all('li', {'data-testid': 'bed'})
    bed_obj = get_element_or_none(find_all, element=1)
    bed = get_text_if_obj_defined(bed_obj)
    return bed


def get_price(soup):
    price_obj = soup.find('div',
                          {'class': 'Text__TextBase-sc-1i9uasc-0-div Text__TextContainerBase-sc-1i9uasc-1 qAaUO'})
    price = get_text_if_obj_defined(price_obj)
    return price


def get_text_if_obj_defined(obj, na_code: str =Codes().na_code):
    if obj is not None:
        extracted_text = obj.text
    else:
        extracted_text = na_code
    return extracted_text


def get_main_sections(soup):
    div_grind_container = soup.find('div', {'class': 'Grid__GridContainer-sc-5ig2n4-1 eVbKXM'})
    section_main_content = soup.find('section', {'id': 'main-content'})
    return div_grind_container, section_main_content


def make_soup(myfile):
    with open(myfile, "r") as file:
        page = file.read()
    soup = BeautifulSoup(page, 'lxml')
    return soup


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables

    main()
