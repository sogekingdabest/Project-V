import json
import re


def find_word_in_text(text, word):
    return re.compile(r'\b({0})\b'.format(word), flags=re.IGNORECASE).search(text)


def get_article_categories(articleBody, category_dict):
    categories = []
    for category, words in category_dict.items():
        for word in words:
            if find_word_in_text(articleBody, word):
                categories.append(category)
                break
    return categories


if __name__ == "__main__":
    articles_file = open('articles.json')
    articles_data = json.load(articles_file)

    categories_file = open('categories.json')
    categories_data = json.load(categories_file)


    for article in articles_data:
        print(article['description'])
        articleBody = article['articleBody']

        for category_name, category_elements in categories_data.items():
            elements_found = get_article_categories(articleBody, category_elements)
            article[category_name] = elements_found

    with open('articles_post.json', 'w') as output:
        json.dump(articles_data, output)
