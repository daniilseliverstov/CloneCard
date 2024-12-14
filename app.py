from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Замените на ваш секретный ключ


api_stores = []


@app.route('/')
def index():
    return render_template('index.html', api_stores=api_stores)


@app.route('/add_store', methods=['POST'])
def add_store():
    api_url = request.form['api_url']
    api_stores.append(api_url)
    flash('API магазина добавлен!')
    return redirect(url_for('index'))


@app.route('/copy_products', methods=['POST'])
def copy_products():
    api_url = request.form['selected_api']
    skus = request.form['skus'].split(',')
    skus = [sku.strip() for sku in skus if sku.strip()]

    if len(skus) > 50:
        flash('Вы можете указать не более 50 артикулов одновременно.')
        return redirect(url_for('index'))

    results = []
    for sku in skus:
        try:
            product_data = get_product_data(sku)
            if product_data:
                create_product_in_store(api_url, product_data)
                results.append(f'Товар {sku} успешно скопирован.')
            else:
                results.append(f'Не удалось получить данные для товара {sku}.')
        except Exception as e:
            results.append(f'Ошибка при обработке товара {sku}: {str(e)}')

    return render_template('results.html', results=results)


def get_product_data(sku):
    """ Здесь вы должны указать API конкурента для получения данных о товаре"""
    competitor_api_url = f'https://competitor.api/products/{sku}'
    response = requests.get(competitor_api_url)
    if response.status_code == 200:
        return response.json()
    return None


def create_product_in_store(api_url, product_data):
    """Здесь вы должны указать API магазина для создания товара"""

    response = requests.post(f'{api_url}/products', json=product_data)
    if response.status_code != 201:
        raise Exception('Ошибка при создании товара в магазине.')


if __name__ == '__main__':
    app.run(debug=True)
