import requests

def test_rank_query():
    response = requests.post("http://127.0.0.1:8000/query?q=What is Aryan's rank in GATE?")
    # print(response.text)
    
    if response.status_code != 200:
        raise Exception(f"Server returned {response.status_code}: {response.text}")
    
    answer = response.json()["answer"]

    # Check for key concepts
    assert "5042" in answer.lower(), "Missing '5042' keyword"
    assert "gate" in answer.lower(), "Missing 'gate' keyword"

    print("✅ Kubernetes query test passed")

if __name__ == "__main__":
    test_rank_query()
    print("All semantic tests passed!")
