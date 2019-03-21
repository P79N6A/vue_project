import json

from . import auth_handler

class TestCommon():
    route_list = [
        "/query_parts/",
        "/query_suppliers/",
        "/query_transactions/",
        "/query_customers/",
        "/query_sales/",
        "/query_categories/",
        "/query_reviews/"
    ]

    active_routes = ["/query_sales/", "/query_categories/"]

    """ _int tests pass ints for limit and offset. _string tests pass strings. """
    
    def test_standard_response_int(self, test_client, test_db):
        with auth_handler(test_client):
            for route in self.route_list:
                test_json = {
                    "query": {
                        "search": "",
                        "sort_by": "id",
                        "limit": 10,
                        "offset": 0
                    }
                }
                if route in self.active_routes:
                    test_json["query"]["active"] = False

                response = test_client.post(
                    route,
                    json=test_json
                )
                assert response.status_code == 200

                # Should return results
                assert len(json.loads(response.data.decode("utf-8"))["result"]["query_result"]) > 0

    def test_standard_response_string(self, test_client, test_db):
        with auth_handler(test_client):
            for route in self.route_list:
                test_json = {
                    "query": {
                        "search": "",
                        "sort_by": "id",
                        "limit": "10",
                        "offset": "0"
                    }
                }
                if route in self.active_routes:
                    test_json["query"]["active"] = False

                response = test_client.post(
                    route,
                    json=test_json
                )
                assert response.status_code == 200

                # Should return results
                assert len(json.loads(response.data.decode("utf-8"))["result"]["query_result"]) > 0

    """ Query variations that should result in success """
    def test_positive_offset_int(self, test_client, test_db):
        with auth_handler(test_client):
            for route in self.route_list:
                test_json = {
                    "query": {
                        "search": "",
                        "sort_by": "id",
                        "limit": 1,
                        "offset": 1
                    }
                }
                if route in self.active_routes:
                    test_json["query"]["active"] = False

                response = test_client.post(
                    route,
                    json=test_json
                )
                assert response.status_code == 200

                # Should return results
                assert len(json.loads(response.data.decode("utf-8"))["result"]["query_result"]) > 0

    def test_negative_limit_int(self, test_client, test_db):
        # Also tests zero, as a matter of QuerySchema functionality. The assert at the bottom depends on this functionality.
        with auth_handler(test_client):
            for route in self.route_list:
                test_json = {
                    "query": {
                        "search": "",
                        "sort_by": "id",
                        "limit": -10,
                        "offset": 0
                    }
                }
                if route in self.active_routes:
                    test_json["query"]["active"] = False

                response = test_client.post(
                    route,
                    json=test_json
                )
                assert response.status_code == 200
                
                # Should return no results
                assert len(json.loads(response.data.decode("utf-8"))["result"]["query_result"]) == 0

    def test_negative_offset_int(self, test_client, test_db):
        with auth_handler(test_client):
            for route in self.route_list:
                test_json = {
                    "query": {
                        "search": "",
                        "sort_by": "id",
                        "limit": 10,
                        "offset": -1
                    }
                }
                if route in self.active_routes:
                    test_json["query"]["active"] = False

                response = test_client.post(
                    route,
                    json=test_json
                )
                assert response.status_code == 200

                # Should return results
                assert len(json.loads(response.data.decode("utf-8"))["result"]["query_result"]) > 0

    def test_positive_offset_string(self, test_client, test_db):
        with auth_handler(test_client):
            for route in self.route_list:
                test_json = {
                    "query": {
                        "search": "",
                        "sort_by": "id",
                        "limit": "1",
                        "offset": "1"
                    }
                }
                if route in self.active_routes:
                    test_json["query"]["active"] = False

                response = test_client.post(
                    route,
                    json=test_json
                )
                assert response.status_code == 200

                # Should return results
                assert len(json.loads(response.data.decode("utf-8"))["result"]["query_result"]) > 0

    def test_negative_limit_string(self, test_client, test_db):
        with auth_handler(test_client):
            for route in self.route_list:
                test_json = {
                    "query": {
                        "search": "",
                        "sort_by": "id",
                        "limit": "-10",
                        "offset": "0"
                    }
                }
                if route in self.active_routes:
                    test_json["query"]["active"] = False

                response = test_client.post(
                    route,
                    json=test_json
                )
                assert response.status_code == 200
                
                # Should return no results
                assert len(json.loads(response.data.decode("utf-8"))["result"]["query_result"]) == 0

    def test_negative_offset_string(self, test_client, test_db):
        with auth_handler(test_client):
            for route in self.route_list:
                test_json = {
                    "query": {
                        "search": "",
                        "sort_by": "id",
                        "limit": "10",
                        "offset": "-1"
                    }
                }
                if route in self.active_routes:
                    test_json["query"]["active"] = False

                response = test_client.post(
                    route,
                    json=test_json
                )
                assert response.status_code == 200

                # Should return results
                assert len(json.loads(response.data.decode("utf-8"))["result"]["query_result"]) > 0

    def test_id_sort(self, test_client, test_db):
        with auth_handler(test_client):
            for route in self.route_list:
                test_json = {
                    "query": {
                        "search": "",
                        "sort_by": "id",
                        "limit": 10,
                        "offset": 0
                    }
                }
                if route in self.active_routes:
                    test_json["query"]["active"] = False

                response = test_client.post(
                    route,
                    json=test_json
                )
                assert response.status_code == 200

                # Sort by id manually, compare
                query_result = json.loads(response.data.decode("utf-8"))["result"]["query_result"]
                sorted_result = sorted(query_result, key=lambda x: x["id"]["value"])

                assert query_result == sorted_result

    """ Query variations that should result in failure """
    def test_no_search(self, test_client, test_db):
        with auth_handler(test_client):
            for route in [x for x in self.route_list if x != "/query_reviews/"]:
                test_json = {
                    "query": {
                        "sort_by": "id",
                        "limit": 10,
                        "offset": 0
                    }
                }
                if route in self.active_routes:
                    test_json["query"]["active"] = False

                response = test_client.post(
                    route,
                    json=test_json
                )
                assert response.status_code == 400

    def test_no_sort(self, test_client, test_db):
        with auth_handler(test_client):
            for route in self.route_list:
                test_json = {
                    "query": {
                        "search": "",
                        "limit": 10,
                        "offset": 0
                    }
                }
                if route in self.active_routes:
                    test_json["query"]["active"] = False

                response = test_client.post(
                    route,
                    json=test_json
                )
                assert response.status_code == 400

    def test_no_limit(self, test_client, test_db):
        with auth_handler(test_client):
            for route in self.route_list:
                test_json = {
                    "query": {
                        "search": "",
                        "sort_by": "id",
                        "offset": 0
                    }
                }
                if route in self.active_routes:
                    test_json["query"]["active"] = False

                response = test_client.post(
                    route,
                    json=test_json
                )
                assert response.status_code == 400

    def test_no_offset(self, test_client, test_db):
        with auth_handler(test_client):
            for route in self.route_list:
                test_json = {
                    "query": {
                        "search": "",
                        "sort_by": "id",
                        "limit": 10
                    }
                }
                if route in self.active_routes:
                    test_json["query"]["active"] = False

                response = test_client.post(
                    route,
                    json=test_json
                )
                assert response.status_code == 400

    def test_invalid_search(self, test_client, test_db):
        with auth_handler(test_client):
            for route in self.route_list:
                test_json = {
                    "query": {
                        "search": 5,
                        "sort_by": "id",
                        "limit": 10,
                        "offset": 0
                    }
                }
                if route in self.active_routes:
                    test_json["query"]["active"] = False

                response = test_client.post(
                    route,
                    json=test_json
                )
                assert response.status_code == 400

    def test_invalid_sort(self, test_client, test_db):
        with auth_handler(test_client):
            for route in self.route_list:
                test_json = {
                    "query": {
                        "search": "",
                        "sort_by": 5,
                        "limit": 10,
                        "offset": 0
                    }
                }
                if route in self.active_routes:
                    test_json["query"]["active"] = False

                response = test_client.post(
                    route,
                    json=test_json
                )
                assert response.status_code == 400

    def test_invalid_limit(self, test_client, test_db):
        with auth_handler(test_client):
            for route in self.route_list:
                test_json = {
                    "query": {
                        "search": "",
                        "sort_by": "id",
                        "limit": "bread",
                        "offset": 0
                    }
                }
                if route in self.active_routes:
                    test_json["query"]["active"] = False

                response = test_client.post(
                    route,
                    json=test_json
                )
                assert response.status_code == 400

    def test_invalid_offset(self, test_client, test_db):
        with auth_handler(test_client):
            for route in self.route_list:
                test_json = {
                    "query": {
                        "search": "",
                        "sort_by": "id",
                        "limit": 10,
                        "offset": "bread"
                    }
                }
                if route in self.active_routes:
                    test_json["query"]["active"] = False

                response = test_client.post(
                    route,
                    json=test_json
                )
                assert response.status_code == 400


class TestParts():
    def test_search_with_results(self, test_client, test_db):
        with auth_handler(test_client):
            response = test_client.post(
                "/query_parts/",
                json={
                    "query": {
                        "search": "Tech",
                        "sort_by": "id",
                        "limit": 10,
                        "offset": 0
                    }
                }
            )
            assert response.status_code == 200

            # Should return results
            assert len(json.loads(response.data.decode("utf-8"))["result"]["query_result"]) > 0

    def test_search_with_no_results(self, test_client, test_db):
        with auth_handler(test_client):
            response = test_client.post(
                "/query_parts/",
                json={
                    "query": {
                        "search": "zzzzzzzzzzzzzzzzz",
                        "sort_by": "id",
                        "limit": 10,
                        "offset": 0
                    }
                }
            )
            assert response.status_code == 200

            # Should return no results
            assert len(json.loads(response.data.decode("utf-8"))["result"]["query_result"]) == 0

    def test_alpha_sort(self, test_client, test_db):
        with auth_handler(test_client):
            response = test_client.post(
                "/query_parts/",
                json={
                    "query": {
                        "search": "",
                        "sort_by": "alpha",
                        "limit": 10,
                        "offset": 0
                    }
                }
            )
            assert response.status_code == 200

            # Sort by alpha manually, compare
            query_result = json.loads(response.data.decode("utf-8"))["result"]["query_result"]
            sorted_result = sorted(query_result, key=lambda x: x["name"]["value"])

            assert query_result == sorted_result


class TestSuppliers():
    def test_search_with_results(self, test_client, test_db):
        with auth_handler(test_client):
            response = test_client.post(
                "/query_suppliers/",
                json={
                    "query": {
                        "search": "",
                        "sort_by": "id",
                        "limit": 10,
                        "offset": 0
                    }
                }
            )
            assert response.status_code == 200

            # Should return results
            assert len(json.loads(response.data.decode("utf-8"))["result"]["query_result"]) > 0

    def test_search_with_no_results(self, test_client, test_db):
        with auth_handler(test_client):
            response = test_client.post(
                "/query_suppliers/",
                json={
                    "query": {
                        "search": "zzzzzzzzzzzzzzzzz",
                        "sort_by": "id",
                        "limit": 10,
                        "offset": 0
                    }
                }
            )
            assert response.status_code == 200

            # Should return no results
            assert len(json.loads(response.data.decode("utf-8"))["result"]["query_result"]) == 0

    def test_alpha_sort(self, test_client, test_db):
        with auth_handler(test_client):
            response = test_client.post(
                "/query_suppliers/",
                json={
                    "query": {
                        "search": "",
                        "sort_by": "alpha",
                        "limit": 10,
                        "offset": 0
                    }
                }
            )
            assert response.status_code == 200

            # Sort by alpha manually, compare
            query_result = json.loads(response.data.decode("utf-8"))["result"]["query_result"]
            sorted_result = sorted(query_result, key=lambda x: x["name"]["value"])

            assert query_result == sorted_result


class TestTransactions():
    def test_search_with_results(self, test_client, test_db):
        with auth_handler(test_client):
            response = test_client.post(
                "/query_transactions/",
                json={
                    "query": {
                        "search": "a",
                        "sort_by": "id",
                        "limit": 10,
                        "offset": 0
                    }
                }
            )
            assert response.status_code == 200

            # Should return results
            assert len(json.loads(response.data.decode("utf-8"))["result"]["query_result"]) > 0

    def test_search_with_no_results(self, test_client, test_db):
        with auth_handler(test_client):
            response = test_client.post(
                "/query_transactions/",
                json={
                    "query": {
                        "search": "zzzzzzzzzzzzzzzzz",
                        "sort_by": "id",
                        "limit": 10,
                        "offset": 0
                    }
                }
            )
            assert response.status_code == 200

            # Should return no results
            assert len(json.loads(response.data.decode("utf-8"))["result"]["query_result"]) == 0

    def test_alpha_sort(self, test_client, test_db):
        with auth_handler(test_client):
            response = test_client.post(
                "/query_transactions/",
                json={
                    "query": {
                        "search": "",
                        "sort_by": "alpha",
                        "limit": 10,
                        "offset": 0
                    }
                }
            )
            assert response.status_code == 200

            # Sort by alpha manually, compare
            query_result = json.loads(response.data.decode("utf-8"))["result"]["query_result"]
            sorted_result = sorted(query_result, key=lambda x: x["email"]["value"])

            assert query_result == sorted_result

    def test_date_sort(self, test_client, test_db):
        with auth_handler(test_client):
            response = test_client.post(
                "/query_transactions/",
                json={
                    "query": {
                        "search": "",
                        "sort_by": "date",
                        "limit": 10,
                        "offset": 0
                    }
                }
            )
            assert response.status_code == 200

            # Sort by id manually, compare
            query_result = json.loads(response.data.decode("utf-8"))["result"]["query_result"]
            sorted_result = sorted(query_result, key=lambda x: x["timestamp_created"]["value"], reverse=True)

            assert query_result == sorted_result


class TestCustomers():
    def test_search_with_results(self, test_client, test_db):
        with auth_handler(test_client):
            response = test_client.post(
                "/query_customers/",
                json={
                    "query": {
                        "search": "a",
                        "sort_by": "id",
                        "limit": 10,
                        "offset": 0
                    }
                }
            )
            assert response.status_code == 200

            # Should return results
            assert len(json.loads(response.data.decode("utf-8"))["result"]["query_result"]) > 0

    def test_search_with_no_results(self, test_client, test_db):
        with auth_handler(test_client):
            response = test_client.post(
                "/query_customers/",
                json={
                    "query": {
                        "search": "zzzzzzzzzzzzzzzzz",
                        "sort_by": "id",
                        "limit": 10,
                        "offset": 0
                    }
                }
            )
            assert response.status_code == 200

            # Should return no results
            assert len(json.loads(response.data.decode("utf-8"))["result"]["query_result"]) == 0

    def test_alpha_sort(self, test_client, test_db):
        with auth_handler(test_client):
            response = test_client.post(
                "/query_customers/",
                json={
                    "query": {
                        "search": "",
                        "sort_by": "alpha",
                        "limit": 10,
                        "offset": 0
                    }
                }
            )
            assert response.status_code == 200

            # Sort by alpha manually, compare
            query_result = json.loads(response.data.decode("utf-8"))["result"]["query_result"]
            sorted_result = sorted(query_result, key=lambda x: x["email"]["value"])

            assert query_result == sorted_result


class TestSales():
    def test_search_with_results(self, test_client, test_db):
        with auth_handler(test_client):
            response = test_client.post(
                "/query_sales/",
                json={
                    "query": {
                        "search": "Tech",
                        "sort_by": "id",
                        "limit": 10,
                        "offset": 0,
                        "active": False
                    }
                }
            )
            assert response.status_code == 200

            # Should return results
            assert len(json.loads(response.data.decode("utf-8"))["result"]["query_result"]) > 0

    def test_search_with_no_results(self, test_client, test_db):
        with auth_handler(test_client):
            response = test_client.post(
                "/query_sales/",
                json={
                    "query": {
                        "search": "zzzzzzzzzzzzzzzzz",
                        "sort_by": "id",
                        "limit": 10,
                        "offset": 0,
                        "active": False
                    }
                }
            )
            assert response.status_code == 200

            # Should return no results
            assert len(json.loads(response.data.decode("utf-8"))["result"]["query_result"]) == 0

    def test_alpha_sort(self, test_client, test_db):
        with auth_handler(test_client):
            response = test_client.post(
                "/query_sales/",
                json={
                    "query": {
                        "search": "",
                        "sort_by": "alpha",
                        "limit": 10,
                        "offset": 0,
                        "active": False
                    }
                }
            )
            assert response.status_code == 200

            # Sort by alpha manually, compare
            query_result = json.loads(response.data.decode("utf-8"))["result"]["query_result"]
            sorted_result = sorted(query_result, key=lambda x: x["name"]["value"])

            assert query_result == sorted_result

    def test_date_sort(self, test_client, test_db):
        with auth_handler(test_client):
            response = test_client.post(
                "/query_sales/",
                json={
                    "query": {
                        "search": "",
                        "sort_by": "date",
                        "limit": 10,
                        "offset": 0,
                        "active": False
                    }
                }
            )
            assert response.status_code == 200

            # Sort by id manually, compare
            query_result = json.loads(response.data.decode("utf-8"))["result"]["query_result"]
            sorted_result = sorted(query_result, key=lambda x: x["timestamp_created"]["value"], reverse=True)

            assert query_result == sorted_result

    def test_active_true_and_false(self, test_client, test_db):
        with auth_handler(test_client):
            true_response = test_client.post(
                "/query_sales/",
                json={
                    "query": {
                        "search": "",
                        "sort_by": "id",
                        "limit": 10000,
                        "offset": 0,
                        "active": True
                    }
                }
            )
            assert true_response.status_code == 200

            false_response = test_client.post(
                "/query_sales/",
                json={
                    "query": {
                        "search": "",
                        "sort_by": "id",
                        "limit": 10000,
                        "offset": 0,
                        "active": False
                    }
                }
            )
            assert false_response.status_code == 200

            # Active filter should return less
            assert len(json.loads(true_response.data.decode("utf-8"))["result"]["query_result"]) < len(json.loads(false_response.data.decode("utf-8"))["result"]["query_result"])

    def test_no_active(self, test_client, test_db):
        with auth_handler(test_client):
            response = test_client.post(
                "/query_sales/",
                json={
                    "query": {
                        "search": "",
                        "sort_by": "id",
                        "limit": 10,
                        "offset": 0
                    }
                }
            )
            assert response.status_code == 400

    def test_invalid_active(self, test_client, test_db):
        with auth_handler(test_client):
            response = test_client.post(
                "/query_sales/",
                json={
                    "query": {
                        "search": "",
                        "sort_by": "id",
                        "limit": 10,
                        "offset": 0,
                        "active": "bread"
                    }
                }
            )
            assert response.status_code == 400

class TestCategories():
    def test_search_with_results(self, test_client, test_db):
        with auth_handler(test_client):
            response = test_client.post(
                "/query_categories/",
                json={
                    "query": {
                        "search": "RAM",
                        "sort_by": "id",
                        "limit": 10,
                        "offset": 0,
                        "active": False
                    }
                }
            )
            assert response.status_code == 200

            # Should return results
            assert len(json.loads(response.data.decode("utf-8"))["result"]["query_result"]) > 0

    def test_search_with_no_results(self, test_client, test_db):
        with auth_handler(test_client):
            response = test_client.post(
                "/query_categories/",
                json={
                    "query": {
                        "search": "zzzzzzzzzzzzzzzzz",
                        "sort_by": "id",
                        "limit": 10,
                        "offset": 0,
                        "active": False
                    }
                }
            )
            assert response.status_code == 200

            # Should return no results
            assert len(json.loads(response.data.decode("utf-8"))["result"]["query_result"]) == 0

    def test_alpha_sort(self, test_client, test_db):
        with auth_handler(test_client):
            response = test_client.post(
                "/query_categories/",
                json={
                    "query": {
                        "search": "",
                        "sort_by": "alpha",
                        "limit": 10,
                        "offset": 0,
                        "active": False
                    }
                }
            )
            assert response.status_code == 200

            #import pdb; pdb.set_trace()

            # Sort by alpha manually, compare
            query_result = json.loads(response.data.decode("utf-8"))["result"]["query_result"]
            sorted_result = sorted(query_result, key=lambda x: x["name"]["value"].lower())

            assert query_result == sorted_result

    def test_active_true_and_false(self, test_client, test_db):
        with auth_handler(test_client):
            true_response = test_client.post(
                "/query_categories/",
                json={
                    "query": {
                        "search": "",
                        "sort_by": "id",
                        "limit": 10000,
                        "offset": 0,
                        "active": True
                    }
                }
            )
            assert true_response.status_code == 200

            false_response = test_client.post(
                "/query_categories/",
                json={
                    "query": {
                        "search": "",
                        "sort_by": "id",
                        "limit": 10000,
                        "offset": 0,
                        "active": False
                    }
                }
            )
            assert false_response.status_code == 200

            # Active filter should return less
            assert len(json.loads(true_response.data.decode("utf-8"))["result"]["query_result"]) < len(json.loads(false_response.data.decode("utf-8"))["result"]["query_result"])

    def test_no_active(self, test_client, test_db):
        with auth_handler(test_client):
            response = test_client.post(
                "/query_categories/",
                json={
                    "query": {
                        "search": "",
                        "sort_by": "id",
                        "limit": 10,
                        "offset": 0
                    }
                }
            )
            assert response.status_code == 400

    def test_invalid_active(self, test_client, test_db):
        with auth_handler(test_client):
            response = test_client.post(
                "/query_categories/",
                json={
                    "query": {
                        "search": "",
                        "sort_by": "id",
                        "limit": 10,
                        "offset": 0,
                        "active": "bread"
                    }
                }
            )
            assert response.status_code == 400


class TestReviews():
    def test_search_with_results(self, test_client, test_db):
        with auth_handler(test_client):
            response = test_client.post(
                "/query_reviews/",
                json={
                    "query": {
                        "sort_by": "id",
                        "limit": 10,
                        "offset": 0
                    }
                }
            )
            assert response.status_code == 200

            # Should return results
            assert len(json.loads(response.data.decode("utf-8"))["result"]["query_result"]) > 0

    def test_search_with_no_results(self, test_client, test_db):
        with auth_handler(test_client):
            response = test_client.post(
                "/query_reviews/",
                json={
                    "query": {
                        "product_id": 1000000000,
                        "sort_by": "id",
                        "limit": 10,
                        "offset": 0
                    }
                }
            )
            assert response.status_code == 200

            # Should return no results
            assert len(json.loads(response.data.decode("utf-8"))["result"]["query_result"]) == 0

    def test_date_sort(self, test_client, test_db):
        with auth_handler(test_client):
            response = test_client.post(
                "/query_reviews/",
                json={
                    "query": {
                        "sort_by": "date",
                        "limit": 10,
                        "offset": 0
                    }
                }
            )
            assert response.status_code == 200

            # Sort by id manually, compare
            query_result = json.loads(response.data.decode("utf-8"))["result"]["query_result"]
            sorted_result = sorted(query_result, key=lambda x: x["timestamp_created"]["value"], reverse=True)

            assert query_result == sorted_result

    def test_product_id_valid(self, test_client, test_db):
        with auth_handler(test_client):
            response = test_client.post(
                "/query_reviews/",
                json={
                    "query": {
                        "product_id": 37,
                        "sort_by": "id",
                        "limit": 10,
                        "offset": 0
                    }
                }
            )
            assert response.status_code == 200

            # Should return results
            assert len(json.loads(response.data.decode("utf-8"))["result"]["query_result"]) > 0

    def test_product_id_invalid(self, test_client, test_db):
        with auth_handler(test_client):
            response = test_client.post(
                "/query_reviews/",
                json={
                    "query": {
                        "product_id": "bread",
                        "sort_by": "id",
                        "limit": 10,
                        "offset": 0
                    }
                }
            )
            assert response.status_code == 400

    def test_customer_id_valid(self, test_client, test_db):
        with auth_handler(test_client):
            response = test_client.post(
                "/query_reviews/",
                json={
                    "query": {
                        "customer_id": 24,
                        "sort_by": "id",
                        "limit": 10,
                        "offset": 0
                    }
                }
            )
            assert response.status_code == 200

            # Should return results
            assert len(json.loads(response.data.decode("utf-8"))["result"]["query_result"]) > 0

    def test_customer_id_invalid(self, test_client, test_db):
        with auth_handler(test_client):
            response = test_client.post(
                "/query_reviews/",
                json={
                    "query": {
                        "customer_id": "bread",
                        "sort_by": "id",
                        "limit": 10,
                        "offset": 0
                    }
                }
            )
            assert response.status_code == 400

    def test_product_and_customer_query(self, test_client, test_db):
        with auth_handler(test_client):
            response = test_client.post(
                "/query_reviews/",
                json={
                    "query": {
                        "customer_id": 24,
                        "product_id": 37,
                        "sort_by": "id",
                        "limit": 10,
                        "offset": 0
                    }
                }
            )
            assert response.status_code == 200

            # Should return results
            assert len(json.loads(response.data.decode("utf-8"))["result"]["query_result"]) > 0
