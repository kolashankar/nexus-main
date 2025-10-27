"""Load testing for API endpoints"""

import pytest
import asyncio
import time
from statistics import mean, median


@pytest.mark.asyncio
async def test_profile_endpoint_load(client):
    """Test profile endpoint under load"""
    num_requests = 100
    response_times = []

    async def make_request():
        start = time.time()
        response = await client.get("/api/player/profile")
        elapsed = time.time() - start
        return elapsed, response.status_code

    tasks = [make_request() for _ in range(num_requests)]
    results = await asyncio.gather(*tasks)

    response_times = [r[0] for r in results]
    status_codes = [r[1] for r in results]

    # Assertions
    avg_response_time = mean(response_times)
    median_response_time = median(response_times)
    success_rate = sum(1 for code in status_codes if code ==
                       200) / num_requests

    print(f"\nAverage response time: {avg_response_time:.3f}s")
    print(f"Median response time: {median_response_time:.3f}s")
    print(f"Success rate: {success_rate * 100:.1f}%")

    assert avg_response_time < 0.5, "Average response time too high"
    assert success_rate > 0.95, "Success rate too low"


@pytest.mark.asyncio
async def test_concurrent_users(client):
    """Test system with concurrent users"""
    num_users = 50
    requests_per_user = 10

    async def simulate_user():
        results = []
        for _ in range(requests_per_user):
            start = time.time()
            response = await client.get("/api/player/profile")
            elapsed = time.time() - start
            results.append((elapsed, response.status_code))
            await asyncio.sleep(0.1)  # Simulate user think time
        return results

    tasks = [simulate_user() for _ in range(num_users)]
    user_results = await asyncio.gather(*tasks)

    # Flatten results
    all_results = [result for user in user_results for result in user]
    response_times = [r[0] for r in all_results]

    avg_response_time = mean(response_times)
    print(
        f"\nConcurrent users test: {num_users} users, {requests_per_user} req/user")
    print(f"Average response time: {avg_response_time:.3f}s")

    assert avg_response_time < 1.0, "Response time under load too high"


@pytest.mark.asyncio
async def test_api_throughput(client):
    """Test API throughput (requests per second)"""
    duration = 10  # seconds
    num_requests = 0

    start_time = time.time()

    while time.time() - start_time < duration:
        await client.get("/api/leaderboards/karma")
        num_requests += 1

    elapsed = time.time() - start_time
    throughput = num_requests / elapsed

    print(f"\nThroughput: {throughput:.2f} requests/second")

    assert throughput > 10, "Throughput too low"


@pytest.mark.asyncio
async def test_database_query_performance(test_db):
    """Test database query performance"""
    # Insert test data
    test_players = [
        {"username": f"perf_test_{i}", "karma_points": i * 10}
        for i in range(1000)
    ]
    await test_db["players"].insert_many(test_players)

    # Test query performance
    start = time.time()
    results = await test_db["players"].find().sort("karma_points", -1).limit(100).to_list(100)
    elapsed = time.time() - start

    print(f"\nDatabase query time: {elapsed:.3f}s for 1000 documents")

    assert elapsed < 0.1, "Database query too slow"
    assert len(results) == 100
