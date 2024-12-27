from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('form.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.form['url']
    element_tag = request.form['element_tag']
    class_name = request.form['class_name']

    options = Options()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)

    output_file = 'scraped_data.csv'

    try:
        # Read the existing file to gather previous data
        data = []
        if os.path.exists(output_file):
            with open(output_file, mode='r', encoding='utf-8') as read_file:
                reader = csv.reader(read_file)
                data = list(reader)

        # Ensure the header row exists and prepare for new column
        column_counter = len(data[0]) if data else 0
        new_column_header = f"Column-{column_counter + 1}"

        # Scrape data
        driver.get(url)

        # Define the wait condition
        wait_condition = (
            (By.CLASS_NAME, class_name) if class_name else (By.TAG_NAME, element_tag)
        )

        # Wait for the elements to be present
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(wait_condition))
        
        # Find the elements
        elements = (
            driver.find_elements(By.CLASS_NAME, class_name)
            if class_name else driver.find_elements(By.TAG_NAME, element_tag)
        )

        # Extract text content from elements
        scraped_data = [element.text.strip() if element.text else "N/A" for element in elements]

        # Adjust the data structure for side-by-side columns
        max_rows = max(len(data), len(scraped_data) + 1)  # Include the header row
        for i in range(max_rows):
            if i == 0:  # Header row
                if i < len(data):
                    data[i].append(new_column_header)
                else:
                    data.append(["" for _ in range(column_counter)] + [new_column_header])
            else:  # Data rows
                if i < len(data):
                    data[i].append(scraped_data[i - 1] if i - 1 < len(scraped_data) else "")
                else:
                    data.append(["" for _ in range(column_counter)] + [scraped_data[i - 1] if i - 1 < len(scraped_data) else ""])

        # Write the updated data back to the CSV file
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(data)

        return render_template('result.html', filename=output_file)
    except Exception as e:
        return render_template('result.html', error=str(e))
    finally:
        driver.quit()

if __name__ == '__main__':
    app.run(debug=True) 