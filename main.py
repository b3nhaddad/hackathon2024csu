import os
import numpy as np
from PIL import Image
import csv
from scipy.stats import norm

select_score = 425.6630682
prime_score = 601.7
choice_score = 535.7205937
low_score = 501.3157895
def calculate_meat_score(similarity_score, grade_score):
    # Calculate the z-score corresponding to the similarity score
    z_score = norm.ppf(similarity_score)
    # Calculate the meat score based on the z-score
    meat_score = grade_score + (z_score * 50)  # Adjust the scaling factor as needed
    # Ensure meat score is within the valid range
    return min(max(meat_score, 100), 1100)

fixed_images = [
    Image.open('/Users/couchroomkid/Desktop/meatExamples/selectgrade1.tif'),
    Image.open('/Users/couchroomkid/Desktop/meatExamples/selectgrade2.tif'),
    Image.open('/Users/couchroomkid/Desktop/meatExamples/selectgrade3.tif'),
    Image.open('/Users/couchroomkid/Desktop/meatExamples/selectgrade4.tif'),
    Image.open('/Users/couchroomkid/Desktop/meatExamples/selectgrade5.tif'),
    Image.open('/Users/couchroomkid/Desktop/meatExamples/selectgrade6.tif'),
    Image.open('/Users/couchroomkid/Desktop/meatExamples/selectgrade7.tif'),
    Image.open('/Users/couchroomkid/Desktop/meatExamples/selectgrade8.tif'),
    Image.open('/Users/couchroomkid/Desktop/meatExamples/selectgrade9.tif'),
    Image.open('/Users/couchroomkid/Desktop/meatExamples/lowchoice.tif'),
    Image.open('/Users/couchroomkid/Desktop/meatExamples/choicegrade1.tif'),
    Image.open('/Users/couchroomkid/Desktop/meatExamples/choicegrade2.tif'),
    Image.open('/Users/couchroomkid/Desktop/meatExamples/choicegrade3.tif'),
    Image.open('/Users/couchroomkid/Desktop/meatExamples/choicegrade4.tif'),
    Image.open('/Users/couchroomkid/Desktop/meatExamples/primegrade1.tif'),
    Image.open('/Users/couchroomkid/Desktop/meatExamples/primegrade2.tif'),
    Image.open('/Users/couchroomkid/Desktop/meatExamples/primegrade3.tif')
]

fixed_data = [np.array(img.convert('RGB')) for img in fixed_images]

results = []
total_similarity_score = 0
num_images = 0

for filename in os.listdir('/Users/couchroomkid/Desktop/meatPictures'):
    if filename.endswith('.tif'):
        changing_image = Image.open(os.path.join('/Users/couchroomkid/Desktop/meatPictures', filename)).convert('RGB')
        changing_data = np.array(changing_image)

        ssid_results = [np.abs(fixed_data[i] - changing_data).sum() for i in range(len(fixed_data))]
        most_similar_index = np.argmin(ssid_results)
        similarity_score = 1 - (ssid_results[most_similar_index] / np.sum(ssid_results))

        if most_similar_index < 9:
            grade_score = select_score
        elif most_similar_index < 13:
            grade_score = choice_score
        elif most_similar_index < 14:
            grade_score = low_score
        else:
            grade_score = prime_score

        meat_score = calculate_meat_score(similarity_score, grade_score)

        result = (filename, os.path.basename(fixed_images[most_similar_index].filename), most_similar_index, meat_score, similarity_score)
        results.append(result)
        total_similarity_score += similarity_score
        num_images += 1

for result in results:
    print(
        f"The image '{result[0]}' is most similar to image '{result[1]}' (index {result[2]}) with a meat score of {result[3]} and a similarity score of {result[4]}.")

with open('results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Changing Image', 'Most Similar Image', 'Index', 'Meat Score', 'Similarity Score'])
    for result in results:
        writer.writerow(result)

average_similarity_score = total_similarity_score / num_images
print(f"The average similarity score across all images is: {average_similarity_score:.2f}")
