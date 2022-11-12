# InvestiDor: um aplicativo para controle financeiro para investimentos

Criei essa aplicação com o objetivo de entender mais sobre o mercado financeiro e sobre investimentos


### Primeiro acesso para ambiente linux

```
git clone https://github.com/LUCASRENAA/Luner.git
cd Luner
echo "export SECRET_KEY='$(openssl rand -hex 40)'" > .DJANGO_SECRET_KEY
source .DJANGO_SECRET_KEY
sudo apt-get install libpq-dev python3-dev
sudo pip install psycopg2
pip3 install -r requirements.txt 
python3 manage.py migrate
python3 manage.py createsuperuser 
python3 manage.py runserver
```