
import flask
from app import app
from models import Article, User, db

app.secret_key = b'a\xdb\xd2\x13\x93\xc1\xe9\x97\xef2\xe3\x004U\xd1Z'

class TestApp:
    '''Flask API in app.py'''
    
    def test_can_only_access_member_only_while_logged_in(self):
        '''allows logged in users to access member-only article index at /members_only_articles.'''
        with app.test_client() as client:
            client.get('/clear')

            user = User.query.first()
            client.post('/login', json={
                'username': user.username
            })

            response = client.get('/members_only_articles')
            assert response.status_code == 200

            client.delete('/logout')

            response = client.get('/members_only_articles')
            assert response.status_code == 401

    def test_member_only_articles_shows_member_only_articles(self):
        '''only shows member-only articles at /members_only_articles.'''
        with app.test_client() as client:
            client.get('/clear')

            user = User.query.first()
            client.post('/login', json={
                'username': user.username
            })

            # Create a member-only article for testing
            member_only_article = Article(title='Member Only Article', content='This is a member-only article.', is_member_only=True)
            db.session.add(member_only_article)
            db.session.commit()

            response_json = client.get('/members_only_articles').get_json()
            for article in response_json:
                assert article['is_member_only'] == True

    def test_can_only_access_member_only_article_while_logged_in(self):
        '''allows logged in users to access full member-only articles at /members_only_articles/<int:id>.'''
        with app.test_client() as client:
            client.get('/clear')

            user = User.query.first()
            client.post('/login', json={
                'username': user.username
            })

            # Create a member-only article for testing
            member_only_article = Article(title='Member Only Article', content='This is a member-only article.', is_member_only=True)
            db.session.add(member_only_article)
            db.session.commit()

            article_id = member_only_article.id  # Use the ID of the created article

            response = client.get(f'/members_only_articles/{article_id}')
            assert response.status_code == 200

            client.delete('/logout')

            response = client.get(f'/members_only_articles/{article_id}')
            assert response.status_code == 401
