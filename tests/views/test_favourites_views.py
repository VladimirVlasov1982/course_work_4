class TestFavouritesView:

    def test_get_favourites(self, client, user, token):
        response = client.get('/favorites/movies', headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200

    def test_add_movie_to_favourite(self, client, token, user):
        response = client.post('/favorites/movies/1', headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 201

    def test_delete_movie_from_favourites(self, client, token):
        response = client.delete('/favorites/movies/1', headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 204
