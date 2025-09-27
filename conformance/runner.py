import argparse, json, requests

def post(base, path, payload=None, stream=False):
    url = base.rstrip('/') + path
    r = requests.post(url, json=payload, stream=stream, timeout=15)
    r.raise_for_status()
    return r

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="http://127.0.0.1:8000")
    args = ap.parse_args()

    # health
    import requests as rq
    h = rq.get(args.base + "/healthz", timeout=5).json()
    print("healthz:", h)

    # 001
    with open("conformance/tests/001_store_recall.json") as f:
        t = json.load(f)
    rid = post(args.base, "/store", t["store"]).json()["id"]
    print("store id:", rid)
    res = post(args.base, "/recall", t["recall"]).json()
    assert any(x["id"] == rid for x in res["items"]), "RECALL missing stored record"
    print("recall ok, items:", len(res["items"]))

    # 002
    with open("conformance/tests/002_forget_export.json") as f:
        t2 = json.load(f)
    rid2 = post(args.base, "/store", t2["store"]).json()["id"]
    post(args.base, "/forget", {"id": rid2})
    r = post(args.base, "/export", {"subject_id":"user_123"}, stream=True)
    cnt = 0
    for line in r.iter_lines():
        if not line: continue
        cnt += 1
    assert cnt > 0, "EXPORT returned 0 lines"
    print("export ok, lines:", cnt)

    print("ALL TESTS PASSED")

if __name__ == "__main__":
    main()
