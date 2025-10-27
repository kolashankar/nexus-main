"""Stress testing for API endpoints"""

import pytest
import asyncio
import time


@pytest.mark.asyncio
async def test_rapid_fire_requests(client):
    """Test system under rapid-fire requests"""
    num_requests = 500

    async def make_request():
        try:
            response = await client.get("/api/leaderboards/karma")
            return response.status_code
        except Exception:
            return 0

    start = time.time()
    tasks = [make_request() for _ in range(num_requests)]
    status_codes = await asyncio.gather(*tasks)
    elapsed = time.time() - start

    success_count = sum(1 for code in status_codes if code == 200)
    success_rate = success_count / num_requests
    throughput = num_requests / elapsed

    print("\nRapid-fire test results:")
    print(f"Total requests: {num_requests}")
    print(f"Time elapsed: {elapsed:.2f}s")
    print(f"Success rate: {success_rate * 100:.1f}%")
    print(f"Throughput: {throughput:.2f} req/s")

    assert success_rate > 0.90, "Too many failures under stress"


@pytest.mark.asyncio
async def test_memory_leak_detection(client, auth_headers):
    """Test for potential memory leaks"""
    import psutil
    import os

    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss / 1024 / 1024  # MB

    # Make many requests
    for _ in range(100):
        await client.get("/api/player/profile", headers=auth_headers)

    final_memory = process.memory_info().rss / 1024 / 1024  # MB
    memory_increase = final_memory - initial_memory

    print("\nMemory usage:")
    print(f"Initial: {initial_memory:.2f} MB")
    print(f"Final: {final_memory:.2f} MB")
    print(f"Increase: {memory_increase:.2f} MB")

    # Memory increase should be reasonable
    assert memory_increase < 50, "Excessive memory usage detected"


@pytest.mark.asyncio
async def test_connection_pool_exhaustion(client):
    """Test behavior under connection pool exhaustion"""
    # Create many concurrent connections
    num_connections = 100

    async def long_running_request():
        try:
            response = await client.get("/api/player/profile")
            return response.status_code
        except Exception:
            return 0

    tasks = [long_running_request() for _ in range(num_connections)]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    successful = sum(1 for r in results if r == 200)
    print(f"\nSuccessful connections: {successful}/{num_connections}")

    # Should handle most connections even under stress
    assert successful > num_connections * 0.8


@pytest.mark.asyncio
async def test_database_concurrent_writes(test_db):
    """Test concurrent database writes"""
    num_writes = 100

    async def write_operation(index):
        try:
            await test_db["test_collection"].insert_one({
                "test_id": index,
                "data": f"test_data_{index}",
                "timestamp": time.time()
            })
            return True
        except Exception:
            return False

    start = time.time()
    tasks = [write_operation(i) for i in range(num_writes)]
    results = await asyncio.gather(*tasks)
    elapsed = time.time() - start

    success_count = sum(1 for r in results if r)
    print(
        f"\nConcurrent writes: {success_count}/{num_writes} successful in {elapsed:.2f}s")

    assert success_count == num_writes, "Some writes failed"


@pytest.mark.asyncio
async def test_rate_limiting(client, auth_headers):
    """Test rate limiting behavior"""
    # Make rapid requests to trigger rate limiting
    num_requests = 200
    responses = []

    for _ in range(num_requests):
        try:
            response = await client.get("/api/player/profile", headers=auth_headers)
            responses.append(response.status_code)
        except Exception:
            responses.append(0)
        await asyncio.sleep(0.01)  # Very short delay

    rate_limited = sum(1 for code in responses if code == 429)
    print(f"\nRate limited requests: {rate_limited}/{num_requests}")

    # Should have some rate limiting if implemented
    # This is informational rather than a hard requirement
    print(
        f"Rate limiting appears to be: {'active' if rate_limited > 0 else 'inactive'}")
